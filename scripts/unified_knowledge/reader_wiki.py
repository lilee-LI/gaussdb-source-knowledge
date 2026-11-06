"""Publish human-readable, reviewed knowledge and cited excerpts without exporting the source graph."""
from collections import defaultdict
from html import escape
from pathlib import Path
import json
import os
import tempfile

from .knowledge import freshness
from .store import atomic_write, canonical, digest, require
from .study import current


def page(title, content):
    return ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            '<title>'+escape(title)+'</title><style>body{max-width:64rem;margin:2rem auto;padding:0 1rem;font:16px/1.65 system-ui;color:#172637}'
            'a{color:#135b89}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f7;padding:1rem}small{color:#465a69}</style>'
            '<main><h1>'+escape(title)+'</h1>'+content+'</main></html>')


def export_wiki(store):
    revision = store.get_meta("knowledge_head")
    require(revision,"还没有已审入库的知识。先提交一个特性，再完成研究审阅和知识审阅。")
    record, plan = store.record("revisions",revision), current(store)
    require((record["snapshot"],record["profile"]) == (plan["snapshot"],plan["profile"]),
            "当前计划与上次知识修订的源码或配置不同，请先复核并接受当前版本的知识。")
    revdir = digest(["reader/v1",revision,plan["run"]])[:24]
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
                for field,label in (("producers","提供方符号"),("consumers","使用方符号"),("conditions","适用条件"),("counterexamples","边界与反例"),("requires","前提"),("ensures","保证"),
                                    ("invariants","不变量"),("expected_from","测试预期来源"),("execution_status","执行状态")):
                    if u.get(field):
                        values = u[field] if isinstance(u[field],list) else [u[field]]
                        if field in {"producers","consumers"}:
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
                         "profile":plan["profile"],"units":len(units),"cited_ranges":len(evidence)}))
            try:
                os.rename(out,target)
            except OSError:
                if not (target/"revision.json").is_file():
                    raise
    with store.transaction():
        require(store.get_meta("knowledge_head")==revision and current(store)["id"]==plan["id"],"知识修订或计划已变化，请重试 wiki")
        pointer = '<meta http-equiv="refresh" content="0;url='+revdir+'/index.html"><a href="'+revdir+'/index.html">打开已审知识</a>'
        atomic_write(location/"index.html",page(title,pointer))
    return {"wiki":str(location/"index.html"),"portable_wiki":str(target),"markdown":str(target/"README.md"),
            "revision":revision,"database":str(store.home/"knowledge.sqlite3")}
