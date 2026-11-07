"""Append native TU memberships; materialize each symbol's JSON once at the end."""
from collections import OrderedDict
import itertools
import json
from functools import lru_cache

from .store import canonical, digest, identity, require


SCHEMA = """
CREATE TABLE IF NOT EXISTS native_contexts(id INTEGER PRIMARY KEY,run TEXT NOT NULL,context TEXT NOT NULL,UNIQUE(run,context));
CREATE TABLE IF NOT EXISTS native_symbols(id INTEGER PRIMARY KEY,run TEXT NOT NULL,symbol TEXT NOT NULL,UNIQUE(run,symbol));
CREATE TABLE IF NOT EXISTS native_types(id INTEGER PRIMARY KEY,value TEXT NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS native_memberships(symbol INTEGER NOT NULL,context INTEGER NOT NULL,type INTEGER NOT NULL,
 PRIMARY KEY(symbol,context)) WITHOUT ROWID;
CREATE INDEX IF NOT EXISTS native_membership_context ON native_memberships(context,symbol);
CREATE TABLE IF NOT EXISTS native_edges(context INTEGER NOT NULL,relation TEXT NOT NULL,PRIMARY KEY(context,relation)) WITHOUT ROWID;
"""


def prepare(store):
    store.db.executescript(SCHEMA)


def prune(store, run, contexts):
    """Remove exactly the retried TUs, including memberships from an interrupted build."""
    db = store.db
    ids = [r[0] for r in db.execute("SELECT id FROM native_contexts WHERE run=? AND context IN "
        "(SELECT value FROM json_each(?))", (run,canonical(sorted(contexts))))]
    values = canonical(ids)
    db.execute("DELETE FROM relations WHERE run=? AND id IN (SELECT relation FROM native_edges WHERE context IN "
        "(SELECT value FROM json_each(?)))", (run,values))
    db.execute("DELETE FROM native_edges WHERE context IN (SELECT value FROM json_each(?))", (values,))
    db.execute("DELETE FROM native_memberships WHERE context IN (SELECT value FROM json_each(?))", (values,))
    db.execute("DELETE FROM native_contexts WHERE id IN (SELECT value FROM json_each(?))", (values,))
    db.execute("DELETE FROM symbols WHERE run=? AND id IN (SELECT n.symbol FROM native_symbols n WHERE n.run=? "
        "AND NOT EXISTS (SELECT 1 FROM native_memberships m WHERE m.symbol=n.id))", (run,run))
    db.execute("DELETE FROM native_symbols WHERE run=? AND NOT EXISTS "
        "(SELECT 1 FROM symbols s WHERE s.run=native_symbols.run AND s.id=native_symbols.symbol)", (run,))


class NativeWriter:
    def __init__(self, store, run, snapshot, profile):
        self.store, self.db, self.run, self.snapshot, self.profile = store, store.db, run, snapshot, profile
        self.assets = {a["key"]:a for (raw,) in self.db.execute("SELECT data FROM assets WHERE snapshot=?",(snapshot,))
                       for a in [json.loads(raw)]}
        self.symbols = {row[1]:row[0] for row in self.db.execute("SELECT id,symbol FROM native_symbols WHERE run=?",(run,))}
        self.definitions = {r[0]:bool(r[1]) for r in self.db.execute("SELECT id,json_extract(data,'$.definition') FROM symbols WHERE run=?",(run,))}
        self.types = {row[1]:row[0] for row in self.db.execute("SELECT id,value FROM native_types")}
        self.anchors = {(r[0],r[1],r[2]):r[3] for r in self.db.execute(
            "SELECT asset,start,end,id FROM main.anchors WHERE snapshot=?", (snapshot,))}
        self.lines, self.line_cost = OrderedDict(), 0
        self.line_counts = {}
        self.instance_id = lru_cache(maxsize=262144)(lambda logical:identity("symbol-instance",[snapshot,profile,logical]))
        self.stats = {"symbol_base_inserts":0,"symbol_context_memberships":0,"symbol_json_finalizations":0,
                      "relations_inserted":0,"anchors_inserted":0,"symbol_base_upgrades":0,"format":"append-memberships/v1"}

    def source_lines(self, asset):
        if asset not in self.lines:
            item = self.assets[asset]
            require(item["status"] == "frozen", "Unavailable native source: " + asset)
            raw = self.store.blob(item["sha"])
            lines = raw.decode("utf-8",errors="replace").splitlines(keepends=True)
            self.line_counts[asset] = len(lines)
            cost = len(raw) + 64*len(lines)
            self.lines[asset] = (lines,cost)
            self.line_cost += cost
            while len(self.lines)>1 and self.line_cost>96*1024**2:
                _, (_,old) = self.lines.popitem(last=False)
                self.line_cost -= old
        self.lines.move_to_end(asset)
        return self.lines[asset][0]

    def anchor(self, asset, start, end):
        asset = self.assets[asset]["key"]
        cached = self.anchors.get((asset,start,end))
        if cached:
            return cached,end
        lines = self.source_lines(asset)
        end = min(end,len(lines))
        require(1<=start<=end, "Out-of-range native source evidence: "+asset+
                " lines "+str(start)+".."+str(end)+" / "+str(len(lines)))
        key = (asset,start,end)
        if key not in self.anchors:
            sha = self.assets[asset]["sha"]
            value = {"snapshot":self.snapshot,"asset":asset,"sha":sha,"asset_sha":sha,"start":start,"end":end,
                     "quote_sha256":digest("".join(lines[start-1:end]).encode("utf-8")),"view":"source"}
            value["id"] = identity("evidence",value)
            self.db.execute("INSERT INTO main.anchors VALUES(?,?,?,?,?,?,?)",
                            (value["id"],self.snapshot,asset,sha,start,end,canonical(value)))
            self.anchors[key] = value["id"]
            self.stats["anchors_inserted"] += 1
        return self.anchors[key],end

    def persist(self, payload, context):
        for include in payload.get("includes",[]):
            if include.get("asset"):
                asset = self.assets.get(include["asset"])
                require(asset and asset["status"]=="frozen" and asset["sha"]==include["sha"],
                        "Compiler read a file outside the frozen input contract: "+include["asset"])
        cursor = self.db.execute("INSERT INTO native_contexts(run,context) VALUES(?,?)", (self.run,context))
        context_id = cursor.lastrowid
        memberships = []
        for value in sorted(payload["symbols"],key=lambda s:(s["asset"],s["start"],s["logical"])):
            item = dict(value)
            item["id"] = self.instance_id(item["logical"])
            item["evidence"],item["end"] = self.anchor(item["asset"],item["start"],item["end"])
            symbol = self.symbols.get(item["id"])
            if symbol is None:
                item.update(snapshot=self.snapshot,profile=self.profile,contexts=[])
                self.db.execute("INSERT INTO symbols VALUES(?,?,?,?,?,?,?)", (self.run,item["id"],item["logical"],item["name"],
                    item["asset"],item["kind"],canonical(item)))
                symbol = self.db.execute("INSERT INTO native_symbols(run,symbol) VALUES(?,?)",(self.run,item["id"])).lastrowid
                self.symbols[item["id"]] = symbol
                self.definitions[item["id"]] = bool(item.get("definition"))
                self.stats["symbol_base_inserts"] += 1
            elif item.get("definition") and not self.definitions[item["id"]]:
                item.update(snapshot=self.snapshot,profile=self.profile,contexts=[])
                self.db.execute("UPDATE symbols SET data=? WHERE run=? AND id=?",(canonical(item),self.run,item["id"]))
                self.definitions[item["id"]] = True
                self.stats["symbol_base_upgrades"] += 1
            kind = canonical(item.get("type"))
            if kind not in self.types:
                self.types[kind] = self.db.execute("INSERT INTO native_types(value) VALUES(?)",(kind,)).lastrowid
            memberships.append((symbol,context_id,self.types[kind]))
        self.db.executemany("INSERT INTO native_memberships VALUES(?,?,?)", memberships)
        self.stats["symbol_context_memberships"] += len(memberships)
        rows, associations = [], []
        seen = set()
        for value in sorted(payload["relations"],key=lambda e:(e.get("asset") or "",e["start"])):
            edge = dict(value)
            if edge.get("asset") not in self.assets:
                continue
            if edge["asset"] not in self.line_counts:
                self.source_lines(edge["asset"])
            if not 1<=edge["start"]<=self.line_counts[edge["asset"]]:
                continue
            edge["evidence"],_ = self.anchor(edge["asset"],edge["start"],max(edge["start"],edge["end"]))
            edge["source_logical"],edge["target_logical"] = edge["source"],edge["target"]
            edge["source"] = self.instance_id(edge["source"])
            edge["target"] = self.instance_id(edge["target"])
            edge.update(context=context,snapshot=self.snapshot,profile=self.profile)
            edge["id"] = identity("relation",edge)
            if edge["id"] in seen:
                continue
            seen.add(edge["id"])
            rows.append((self.run,edge["id"],edge["source"],edge["target"],edge["kind"],edge["resolution"],canonical(edge)))
            associations.append((context_id,edge["id"]))
        self.db.executemany("INSERT INTO relations VALUES(?,?,?,?,?,?,?)",rows)
        self.db.executemany("INSERT INTO native_edges VALUES(?,?)",associations)
        self.stats["relations_inserted"] += len(rows)

    def finish(self):
        contexts = dict(self.db.execute("SELECT id,context FROM native_contexts WHERE run=?",(self.run,)))
        types = {r[0]:json.loads(r[1]) for r in self.db.execute("SELECT id,value FROM native_types")}
        symbols = {v:k for k,v in self.symbols.items()}
        rows = self.db.execute("SELECT m.symbol,m.context,m.type FROM native_memberships m JOIN native_symbols s "
            "ON s.id=m.symbol WHERE s.run=? ORDER BY m.symbol,m.context",(self.run,))
        for sid, group in itertools.groupby(rows,key=lambda row:row[0]):
            observations = {}
            for _,context,kind in group:
                observations.setdefault(types[kind],[]).append(contexts[context])
            item = json.loads(self.db.execute("SELECT data FROM symbols WHERE run=? AND id=?",(self.run,symbols[sid])).fetchone()[0])
            item["contexts"] = sorted(itertools.chain.from_iterable(observations.values()))
            item.pop("type_observations",None)
            item.pop("type_resolution",None)
            if len(observations)==1:
                item["type"] = next(iter(observations))
            else:
                item["type"] = None
                item["type_resolution"] = "context_dependent"
                item["type_observations"] = sorted(
                    ({"type":kind,"contexts":sorted(values)} for kind,values in observations.items()),key=canonical)
            self.db.execute("UPDATE symbols SET data=? WHERE run=? AND id=?",(canonical(item),self.run,item["id"]))
            self.stats["symbol_json_finalizations"] += 1
        return dict(self.stats)
