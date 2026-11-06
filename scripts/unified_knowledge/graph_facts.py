"""Cross-translation-unit definition binding and bounded NetworkX traversals."""
import json

import networkx as nx

from .store import canonical, identity


FUNCTION_KINDS = ("function_decl", "cxx_method", "constructor", "destructor", "function_template", "conversion_function")


class LegacyCalls:
    """Qualify old declaration-only calls using indexed lookups in the original run."""
    def __init__(self, store, run):
        self.db = store.db
        self.run = run
        self.targets = {}

    def matches(self, node, definition, limit):
        if node.get("kind") not in FUNCTION_KINDS or not node.get("usr"):
            return []
        rows = self.db.execute("SELECT id,logical,data FROM symbols WHERE run=? AND name=? "
                               "AND json_extract(data,'$.usr')=? AND json_extract(data,'$.definition')=? "
                               "AND coalesce(json_extract(data,'$.linkage'),'EXTERNAL')='EXTERNAL' LIMIT ?",
                               (self.run,node["name"],node["usr"],definition,limit))
        return [json.loads(row["data"]) for row in rows]

    def rewrite(self, edge):
        if edge["kind"] != "CALLS" or edge.get("target_binding") or edge.get("dispatch") == "virtual":
            return edge
        target = edge["target"]
        if target not in self.targets:
            binding = {}
            row = self.db.execute("SELECT data FROM symbols WHERE run=? AND id=?", (self.run,target)).fetchone()
            node = json.loads(row[0]) if row else {}
            if node.get("kind") in FUNCTION_KINDS and node.get("definition") is False:
                defs = self.matches(node,True,2)
                binding = {"declared_target":target,"resolution":"unresolved","target_binding":"declaration_only"}
                if len(defs) > 1:
                    binding.update(resolution="candidate",target_binding="ambiguous_definitions")
                elif defs and node.get("linkage") == defs[0].get("linkage") == "EXTERNAL":
                    binding.update(resolution="resolved",target_binding="linked_definitions",target=defs[0]["id"],target_logical=defs[0]["logical"])
                elif defs and node.get("linkage") is None and node["kind"]=="function_decl":
                    binding.update(resolution="candidate",target_binding="legacy_usr_candidate",target=defs[0]["id"],target_logical=defs[0]["logical"])
            self.targets[target] = binding
        if not self.targets[target]:
            return edge
        revised = {k:v for k,v in edge.items() if k!="id"}
        revised.update(self.targets[target])
        return {**revised,"id":identity("relation",revised)}


def link_calls(store, run, *, legacy_candidates=False):
    """Join declaration occurrences by USR; keep legacy edges explicitly qualified."""
    kinds = FUNCTION_KINDS
    slots = ",".join("?" for _ in kinds)
    counts = {"linked_definitions": 0, "declaration_only": 0, "ambiguous_definitions": 0, "legacy_usr_candidate": 0}
    db = store.db
    db.execute("DROP TABLE IF EXISTS temp.link_definitions")
    db.execute("DROP TABLE IF EXISTS temp.link_sites")
    db.execute("CREATE TEMP TABLE link_definitions AS SELECT json_extract(data,'$.usr') usr, count(*) n, min(id) target,"
               " min(logical) logical, min(coalesce(json_extract(data,'$.linkage'),'')) linkage FROM symbols "
               "WHERE run=? AND kind IN (" + slots + ") AND json_extract(data,'$.definition')=1 "
               "AND (json_extract(data,'$.linkage')='EXTERNAL' OR (? AND json_extract(data,'$.linkage') IS NULL)) "
               "AND json_extract(data,'$.usr') IS NOT NULL GROUP BY usr", (run, *kinds, legacy_candidates))
    db.execute("CREATE INDEX temp.link_by_usr ON link_definitions(usr)")
    # Freeze this worklist; rewriting relationship IDs cannot extend a live cursor.
    db.execute("CREATE TEMP TABLE link_sites AS SELECT e.id,e.data,d.id decl,d.logical decl_logical,"
               "json_extract(d.data,'$.linkage') linkage,d.kind,defs.n,defs.target,defs.logical,defs.linkage def_linkage "
               "FROM relations e JOIN symbols d ON d.run=e.run AND d.id=coalesce(json_extract(e.data,'$.declared_target'),e.target) "
               "LEFT JOIN link_definitions defs ON defs.usr=json_extract(d.data,'$.usr') "
               "WHERE e.run=? AND e.kind='CALLS' AND coalesce(json_extract(e.data,'$.dispatch'),'')<>'virtual' "
               "AND d.kind IN (" + slots + ") AND json_extract(d.data,'$.definition')=0", (run, *kinds))
    for row in db.execute("SELECT * FROM link_sites"):
        edge = json.loads(row["data"])
        target, logical = row["decl"], row["decl_logical"]
        if row["n"] == 1 and row["linkage"] == row["def_linkage"] == "EXTERNAL":
            target, logical = row["target"], row["logical"]
            resolution, reason = "resolved", "linked_definitions"
        elif legacy_candidates and row["n"] == 1 and row["linkage"] is None and row["kind"] == "function_decl":
            target, logical = row["target"], row["logical"]
            resolution, reason = "candidate", "legacy_usr_candidate"
        elif row["n"] and row["n"] > 1:
            resolution, reason = "candidate", "ambiguous_definitions"
        else:
            resolution, reason = "unresolved", "declaration_only"
        counts[reason] += 1
        edge.update(target=target, target_logical=logical, resolution=resolution,
                    declared_target=row["decl"], target_binding=reason)
        edge.pop("id", None)
        edge["id"] = identity("relation", edge)
        if edge["id"] != row["id"]:
            db.execute("DELETE FROM relations WHERE run=? AND id=?", (run, row["id"]))
            db.execute("INSERT OR IGNORE INTO relations VALUES(?,?,?,?,?,?,?)",
                       (run, edge["id"], edge["source"], target, "CALLS", resolution, canonical(edge)))
    db.execute("DROP TABLE temp.link_sites")
    db.execute("DROP TABLE temp.link_definitions")
    return counts


def traversal(relations, seeds, direction, algorithm, depth):
    """Operate only on the bounded, already fetched neighborhood."""
    graph = nx.DiGraph()
    graph.add_nodes_from(seeds)
    for edge in relations:
        a, b = edge["source"], edge["target"]
        if direction in {"both", "forward"}:
            graph.add_edge(a, b)
        if direction in {"both", "reverse"}:
            graph.add_edge(b, a)
    trees = []
    for seed in sorted(set(seeds)):
        edges = list((nx.dfs_edges if algorithm == "dfs" else nx.bfs_edges)(
            graph, source=seed, depth_limit=depth)) if depth else []
        tree = nx.DiGraph()
        tree.add_node(seed)
        tree.add_edges_from(edges)
        trees.append({"root": seed, "edges": edges, "postorder": list(nx.dfs_postorder_nodes(tree, seed))})
    return {"provider": "networkx", "algorithm": algorithm, "trees": trees}
