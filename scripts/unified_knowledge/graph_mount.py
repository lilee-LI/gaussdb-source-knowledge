"""Read an immutable ECS handoff through indexed SQLite lookups without copying its fact tables."""
import json
from pathlib import Path
import sqlite3

from .store import canonical, require

FACTS = {"symbols":"id,logical,name,asset,kind,data","relations":"id,source,target,kind,resolution,data"}
REQUIRED = {"runs":{"id","snapshot","profile","status","data"},"snapshots":{"id","data"},
            "documents":{"snapshot","data"}, "anchors":{"id","snapshot","asset","sha","start","end","data"},
            **{t:set(s.split(",")) | {"run"} for t,s in FACTS.items()}}


def readonly_uri(path):
    """A sealed one-file handoff also works in a read-only directory without WAL sidecars."""
    path = Path(path).resolve()
    wal = path.with_name(path.name+"-wal")
    journal = path.with_name(path.name+"-journal")
    active = any(p.exists() and p.stat().st_size for p in (wal,journal))
    return path.as_uri()+("?mode=ro" if active else "?mode=ro&immutable=1")


def inspect_input(path, requested=None, *, check_indexes=False):
    path = Path(path).expanduser().resolve()
    require(path.is_file(),"找不到 ECS SQLite 文件：" + str(path))
    from contextlib import closing
    with closing(sqlite3.connect(readonly_uri(path),uri=True)) as db:
        for table, fields in REQUIRED.items():
            have = {r[1] for r in db.execute("PRAGMA table_info("+table+")")}
            require(fields<=have,"ECS SQLite 格式不匹配，表 "+table+" 缺少 "+", ".join(sorted(fields-have))+"。请提供本工程的索引导出或按实际表结构映射。")
        if check_indexes:
            needed = {"symbols":[("run","id"),("run","logical"),("run","name"),("run","asset")],"relations":[("run","source"),("run","target")],
                      "anchors":[("id",),("snapshot","asset")]}
            for table, keys in needed.items():
                prefixes = [tuple(r[2] for r in db.execute("SELECT * FROM pragma_index_info(?)",(idx[1],))) for idx in db.execute("PRAGMA index_list("+table+")")]
                for key in keys:
                    require(any(cols[:len(key)]==key for cols in prefixes),"ECS 交付库缺少索引 "+table+str(key)+"。请在上游副本建立索引后重新交付。")
        rows = db.execute("SELECT id,profile,status,json_extract(data,'$.mode') FROM runs WHERE status IN ('ready','partial') "
                          "AND length(json_extract(data,'$.facts_digest'))>0 ORDER BY id")
        choices = [{"run_id":r[0],"profile":r[1],"status":r[2]} for r in rows if r[3] not in {"inventory","ecs_module","source_only","ecs"}]
        ids = [r["run_id"] for r in choices]
        if requested:
            require(requested in ids,"ECS run_id was not found among completed ECS runs with facts_digest: "+str(requested)+"；可选 "+str(choices[:12]))
        else:
            require(len(ids)==1,"请在 paths.json 填写 run_id，可选的已完成分析为 "+str(choices[:12]))
    return {"path":str(path),"bytes":path.stat().st_size,"run_id":requested or ids[0]}


def attach(store, path):
    path = Path(path).resolve()
    if getattr(store,"graph_path",None):
        require(store.graph_path==path,"该工作区已绑定另一份 ECS 图。请为不同图建立独立工作区。")
        return
    require(path.is_file(),"ECS 只读调用图路径不可用："+str(path)+"。请恢复图文件或使用原工作区配置重新绑定同一份交付件。")
    db = store.db
    db.execute("ATTACH DATABASE ? AS source_graph",(readonly_uri(path),))
    try:
        for row in db.execute("SELECT DISTINCT upstream,snapshot,digest FROM main.graph_bindings"):
            check = db.execute("SELECT snapshot,json_extract(data,'$.facts_digest') FROM source_graph.runs WHERE id=?",(row[0],)).fetchone()
            require(check and tuple(check)==(row[1],row[2]),"ECS 图的 run/快照/摘要已变化，请使用原交付件或开新工作区。")
        for table, fields in FACTS.items():
            external = ",".join("g."+n for n in fields.split(","))
            db.execute("CREATE TEMP VIEW "+table+" AS SELECT * FROM main."+table+" UNION ALL SELECT b.study,"+external+
                       " FROM main.graph_bindings b JOIN source_graph."+table+" g ON g.run=b.upstream")
        db.execute("CREATE TEMP VIEW anchors AS SELECT * FROM main.anchors UNION ALL SELECT g.* FROM source_graph.anchors g "
                   "WHERE g.snapshot IN (SELECT DISTINCT snapshot FROM main.graph_bindings) "
                   "AND NOT EXISTS (SELECT 1 FROM main.anchors a WHERE a.id=g.id)")
        store.graph_path = path
    except BaseException:
        for table in (*FACTS,"anchors"):
            db.execute("DROP VIEW IF EXISTS temp."+table)
        db.execute("DETACH DATABASE source_graph")
        raise


def register(store, path, index, snapshot, rid):
    attach(store,path)
    with store.transaction():
        run = store.db.execute("SELECT data FROM main.runs WHERE id=?",(rid,)).fetchone()
        if run:
            store.set_meta("external_graph",str(path))
            return json.loads(run[0])
        origin = index.origin
        attached = store.db.execute("SELECT snapshot,json_extract(data,'$.facts_digest') FROM source_graph.runs WHERE id=?",(origin["run_id"],)).fetchone()
        require(attached and tuple(attached)==(origin["snapshot"],origin["facts_digest"]),"ECS 交付发生变化，请重试。")
        store.db.execute("INSERT INTO main.graph_bindings VALUES(?,?,?,?)",(rid,origin["run_id"],origin["snapshot"],origin["facts_digest"]))
        store.set_meta("external_graph",str(path))
        from .store import digest, now
        data = {"id":rid,"snapshot":snapshot,"profile":origin["profile"],"profile_digest":origin["profile_digest"],
                "mode":"ecs","graph_storage":"reference","source_index":origin,"status":index.run["status"],
                "created":now(),"facts_digest":digest(["ecs-reference/v1",origin]),"coverage":index.run["coverage"],
                "tu_results":[],"cache_hits":0,"frontend_invocations":0,"database_execution":"not_run"}
        store.db.execute("INSERT INTO runs VALUES(?,?,?,?,?,?)",(rid,snapshot,data["profile"],data["created"],data["status"],canonical(data)))
    return data
