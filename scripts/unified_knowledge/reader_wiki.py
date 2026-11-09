"""Publish human-readable, reviewed knowledge and cited excerpts without exporting the source graph."""
from collections import defaultdict
from html import escape
from pathlib import Path
import json
import os
import tempfile

from .knowledge import freshness
from .associations import collect as collect_associations
from . import role_context
from .store import atomic_write, canonical, digest, require
from .study import current


def page(title, content):
    return ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            '<title>'+escape(title)+'</title><style>body{max-width:64rem;margin:2rem auto;padding:0 1rem;font:16px/1.65 system-ui;color:#172637}'
            'a{color:#135b89}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f7;padding:1rem}small{color:#465a69}</style>'
            '<main><h1>'+escape(title)+'</h1>'+content+'</main></html>')


def _publish_views(out, store, units, plan, revision, projection):
    """Navigation and Agent JSON are derived from this exact accepted revision."""
    groups = {name: defaultdict(set) for name in ("module", "feature", "mainline")}
    owners = {asset: mid for mid, module in plan.get("modules", {}).items() for asset in module.get("files", [])}
    fresh = {}
    provenance = {}
    for uid, unit in units.items():
        state = freshness(store, unit, plan["snapshot"], plan["run"], units)
        if not state:
            fresh[uid] = unit
        provenance[uid] = {"binding": unit.get("_binding", {}), "review": unit.get("review", {}),
                           "content_hash": unit.get("content_hash"), "source_refs": unit.get("source_refs", []), "stale_reasons": state}
        for name in groups:
            values = list(unit.get(name + "_ids", []))
            if unit.get(name + "_id"):
                values.append(unit[name + "_id"])
            if name == "feature" and unit["kind"] == "feature":
                values.append(uid)
            if name == "module":
                for ref in unit.get("source_refs", []):
                    owner = owners.get(store.record("anchors", ref)["asset"])
                    if owner:
                        values.append(owner)
            for value in values:
                groups[name][value].add(uid)
    for kind, rows in projection["navigation"].items():
        for key, ids in rows.items():
            groups[kind][key].update(uid for uid in ids if uid in units)
    taxonomy = {kind: {key: sorted(ids) for key, ids in sorted(rows.items())} for kind, rows in groups.items()}
    atomic_write(out/"knowledge.json", canonical({"schema": "reader-knowledge/v1", "knowledge_revision": revision,
        "source_snapshot": plan["snapshot"], "build_profile": plan["profile"], "index_run": plan["run"],
        "projection_fingerprint": projection["fingerprint"], "reviewed_associations": projection,
        "units": [units[uid] for uid in sorted(units)], "provenance": provenance, "navigation": taxonomy,
        "runtime_validation": "not_run"}))
    root_h, root_md = [], []
    for kind, label in (("module", "按模块"), ("feature", "按特性"), ("mainline", "按执行主干")):
        content, lines = [], ["# " + label, "", "修订 " + revision, ""]
        if not taxonomy[kind]:
            content.append("<p>此修订尚未包含该类已审关联。</p>")
            lines.append("此修订尚未包含该类已审关联。")
        for key, ids in taxonomy[kind].items():
            content.append("<h2>" + escape(key) + "</h2><ul>")
            lines += ["", "## " + key, ""]
            for uid in ids:
                stem = digest(uid)[:24]
                content.append('<li><a href="../pages/' + stem + '.html">' + escape(units[uid]["title"]) + '</a></li>')
                lines.append("- [" + units[uid]["title"] + "](../pages/" + stem + ".md)")
            content.append("</ul>")
        atomic_write(out/"views"/(kind + ".html"), page(label, ''.join(content)))
        atomic_write(out/"views"/(kind + ".md"), '\n'.join(lines) + '\n')
        root_h.append('<a href="views/' + kind + '.html">' + label + '</a>')
        root_md.append("[" + label + "](views/" + kind + ".md)")
    # A role view never invents observations/remedies if the accepted knowledge
    # contains only implementation contracts. Missing slots remain explicit.
    pack = {"constraints": [], "paths": [], "test_obligations": []}
    for uid, unit in fresh.items():
        key = "paths" if unit["kind"] == "flow" else "test_obligations" if unit["kind"] == "test_obligation" else "constraints"
        pack[key].append({"id": uid, "body": unit["body"]})
    evidence_kinds = {ref: store.asset(plan["snapshot"], store.record("anchors", ref)["asset"])["kind"]
                      for unit in fresh.values() for ref in unit.get("source_refs", [])}
    for role, label in (("coding", "开发"), ("test_generation", "测试生成"), ("review", "代码评审"), ("operations", "运维")):
        view = role_context.compose(pack, fresh, role, evidence_kinds=evidence_kinds)
        view["knowledge_revision"] = revision
        view["scope"] = {"source_snapshot": plan["snapshot"], "build_profile": plan["profile"], "index_run": plan["run"]}
        atomic_write(out/"roles"/(role + ".json"), canonical(view))
        content = ["<p>同一已审修订的结构化视图；状态 " + escape(view["status"]) + "。</p>"]
        lines = ["# " + label + "知识视图", "", "修订 " + revision, "", "状态 " + view["status"], ""]
        for name in view["required"]:
            heading = role_context.LABELS[name]
            content.append("<h2>" + heading + "</h2>")
            lines += ["## " + heading, ""]
            if not view["sections"].get(name):
                content.append("<p>缺少已审知识，需要补充。</p>")
                lines += ["缺少已审知识，需要补充。", ""]
            for row in view["sections"].get(name, []):
                stem = digest(row["unit"])[:24]
                text = canonical(row["value"])
                content += ['<p><a href="../pages/' + stem + '.html">' + escape(fresh[row["unit"]]["title"]) + '</a> · ' + escape(row["field"]) + '</p><pre>' + escape(text) + '</pre>']
                lines += ["[" + fresh[row["unit"]]["title"] + "](../pages/" + stem + ".md) · " + row["field"], "", "```json", text, "```", ""]
        atomic_write(out/"roles"/(role + ".html"), page(label + "知识视图", ''.join(content)))
        atomic_write(out/"roles"/(role + ".md"), '\n'.join(lines) + '\n')
        root_h.append('<a href="roles/' + role + '.html">' + label + '视图</a>')
        root_md.append("[" + label + "视图](roles/" + role + ".md)")
    root_h.append('<a href="knowledge.json">结构化知识与来源 JSON</a>')
    root_md.append("[结构化知识与来源 JSON](knowledge.json)")
    return '<p>' + ' · '.join(root_h) + '</p>', ' · '.join(root_md)


def export_wiki(store):
    revision = store.get_meta("knowledge_head")
    require(revision,"还没有已审入库的知识。先提交一个特性，再完成研究审阅和知识审阅。")
    record, plan = store.record("revisions",revision), current(store)
    require((record["snapshot"],record["profile"]) == (plan["snapshot"],plan["profile"]),
            "当前计划与上次知识修订的源码或配置不同，请先复核并接受当前版本的知识。")
    projection = collect_associations(store, snapshot=plan["snapshot"], run=plan["run"], revision=revision)
    revdir = digest(["reader/v3",revision,plan["run"],projection["fingerprint"]])[:24]
    location = store.home/"wiki"
    location.mkdir(exist_ok=True)
    target = location/revdir
    title = "源码知识 Wiki"
    if not target.is_dir():
        units = store.units(revision)
        snapshot = store.record("snapshots",record["snapshot"])
        scope = f"{snapshot['product']} · {snapshot['revision']} · {record['profile']}"
        with tempfile.TemporaryDirectory(dir=location,prefix=".render-") as scratch:
            out = Path(scratch)/"wiki"
            groups, evidence = defaultdict(list), {}
            for uid,u in sorted(units.items()):
                stem = digest(uid)[:24]
                state = freshness(store,u,plan["snapshot"],plan["run"],units)
                status = "依赖已变化，待复核" if state else u["review"]["mode"]
                lines = ["# "+u["title"], "", scope, "", "审阅状态 "+status, "", u["body"]]
                html = ['<a href="../index.html">返回知识目录</a><p>'+escape(scope+" · "+status)+'</p><pre>'+escape(u["body"])+'</pre>']
                provenance = {"knowledge_id": uid, "knowledge_revision": revision, "binding": u.get("_binding", {}),
                              "review": u.get("review", {}), "content_hash": u.get("content_hash"), "stale_reasons": state}
                lines += ["", "## 知识来源与版本", "", "```json", canonical(provenance), "```"]
                html.append("<details><summary>知识来源与版本</summary><pre>" + escape(canonical(provenance)) + "</pre></details>")
                if u.get("level"):
                    key = u.get("parent")
                    label = f"L{u['level']}"
                    parent = units.get(key)
                    if parent:
                        stem_parent = digest(key)[:24]
                        lines += [label+" · 上级 ["+parent["title"]+"]("+stem_parent+".md)"]
                        html.append("<p>"+label+' · 上级 <a href="'+stem_parent+'.html">'+escape(parent["title"])+"</a></p>")
                    else:
                        lines.append(label)
                        html.append("<p>"+label+"</p>")
                for field,label in (("producers","提供方"),("consumers","消费者"),("conditions","适用条件"),("counterexamples","边界与反例"),("requires","前提"),("ensures","保证"),
                                    ("invariants","不变量"),("expected_from","测试预期来源"),("execution_status","执行状态"),
                                    ("module_id","模块"),("module_ids","关联模块"),("feature_id","特性"),("feature_ids","关联特性"),
                                    ("mainline_id","执行主干"),("mainline_ids","关联执行主干"),
                                    ("topic_extensions","专题知识"),("operations","运维依据")):
                    if u.get(field):
                        values = u[field] if isinstance(u[field],list) else [u[field]]
                        if field in {"producers","consumers"} and u['kind']=='contract':
                            labels = []
                            for ref in values:
                                found = store.lookup_symbols(plan["run"],ref,names=False,limit=1)
                                if found:
                                    symbol = json.loads(found[0]["data"])
                                    labels.append(f"{symbol['name']} · {symbol['asset']}:{symbol['start']}-{symbol['end']}")
                                else:
                                    labels.append(ref)
                            values = labels
                        values = [x if isinstance(x,str) else canonical(x) for x in values]
                        lines += ["","## "+label,"",*["- "+v for v in values]]
                        html += ["<h2>"+label+"</h2><ul>"+''.join("<li>"+escape(v)+"</li>" for v in values)+"</ul>"]
                html.append("<h2>证据</h2><ul>")
                lines += ["","## 证据",""]
                for ref in u.get("source_refs",[]):
                    if ref not in evidence:
                        a = store.read_evidence(ref,max_chars=16000)
                        label = f"{a['asset']}:{a['start']}-{a['end']}"
                        file = "evidence/"+digest(ref)[:24]+".html"
                        note = "显示前 16,000 字符，完整区间可用证据 ID 查询。" if a["truncated"] else "完整引用区间"
                        atomic_write(out/file,page(label,"<small>"+escape(scope+" · "+note)+"</small><pre>"+escape(a["text"])+"</pre><p>"+
                                                    escape(ref)+"</p><p>SHA-256 "+escape(a["quote_sha256"])+"</p>"))
                        evidence[ref]=(label,file)
                    label,file=evidence[ref]
                    html.append('<li><a href="../'+file+'">'+escape(label)+'</a></li>')
                    lines.append("- ["+label+"](../"+file+")")
                html.append("</ul>")
                links = list(u.get("knowledge_refs",[]))
                if u.get("kind")=="test_obligation" and u.get("expected_from",{}).get("ref") in units:
                    links.append({"target":u["expected_from"]["ref"],"relation":"测试预期依据"})
                if links:
                    html.append("<h2>相关知识</h2><ul>")
                    lines.extend(["","## 相关知识",""])
                    for edge in links:
                        other = units.get(edge["target"])
                        if other:
                            link=digest(other["id"])[:24]
                            label=edge["relation"]+" · "+other["title"]
                            html.append('<li><a href="'+link+'.html">'+escape(label)+'</a></li>')
                            lines.append("- ["+label+"]("+link+".md)")
                    html.append("</ul>")
                atomic_write(out/"pages"/(stem+".html"),page(u["title"],"".join(html)))
                atomic_write(out/"pages"/(stem+".md"),"\n".join(lines)+"\n")
                label = (f"L{u['level']} · " if u.get("level") else "")+u["title"]
                groups[u["kind"]].append((label,stem))
            h=["<p>"+escape(scope)+"</p><p>已审知识 "+str(len(units))+" 项，引用 "+str(len(evidence))+" 处。源码推导和运行验证分别记录。</p>"]
            md=["# "+title,"",scope,""]
            views_html, views_md = _publish_views(out, store, units, plan, revision, projection)
            h.append(views_html)
            md += [views_md, ""]
            for kind,items in sorted(groups.items()):
                label={"contract":"源码契约","claim":"已核对结论","test_obligation":"应测场景","feature":"特性节点",
                       "responsibility":"责任范围","flow":"调用与数据流程"}.get(kind,kind)
                h.append("<h2>"+escape(label)+"</h2><ul>")
                md += ["## "+label,""]
                for name,stem in items:
                    h.append('<li><a href="pages/'+stem+'.html">'+escape(name)+'</a></li>')
                    md.append("- ["+name+"](pages/"+stem+".md)")
                h.append("</ul>")
                md.append("")
            atomic_write(out/"index.html",page(title,"".join(h)))
            atomic_write(out/"README.md","\n".join(md))
            atomic_write(out/"revision.json",canonical({"revision":revision,"snapshot":plan["snapshot"],"run":plan["run"],
                         "projection_fingerprint":projection["fingerprint"],
                         "profile":plan["profile"],"units":len(units),"cited_ranges":len(evidence)}))
            try:
                os.rename(out,target)
            except OSError:
                if not (target/"revision.json").is_file():
                    raise
    with store.transaction():
        require(store.get_meta("knowledge_head")==revision and current(store)["id"]==plan["id"],"知识修订或计划已变化，请重试 wiki")
        require(collect_associations(store, snapshot=plan["snapshot"], run=plan["run"], revision=revision)["fingerprint"] == projection["fingerprint"],
                "已审特性或主干关联已变化，请重试 wiki")
        pointer = '<meta http-equiv="refresh" content="0;url='+revdir+'/index.html"><a href="'+revdir+'/index.html">打开已审知识</a>'
        atomic_write(location/"index.html",page(title,pointer))
    return {"wiki":str(location/"index.html"),"portable_wiki":str(target),"markdown":str(target/"README.md"),
            "revision":revision,"projection_fingerprint":projection["fingerprint"],"database":str(store.home/"knowledge.sqlite3"), "structured_knowledge": str(target/"knowledge.json"),
            "role_views": {role: str(target/"roles"/(role+".json")) for role in role_context.ROLES}}
