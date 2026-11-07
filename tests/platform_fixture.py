"""Synthetic protocol fixture; no real product knowledge or model-quality assertions."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from make_fixture import build_fixture
from unified_knowledge import ecs, study, knowledge
from unified_knowledge.store import Store


def workspace(root):
    root = Path(root)
    source = root / "source"
    shutil.copytree(ROOT / "assets/ecs-fixture/source", source)
    incoming = root / "input.sqlite3"
    build_fixture(incoming)
    store = Store(root / "home")
    try:
        ecs.connect(store, {"repositories":[{"id":"server","root":str(source)}], "product_adapter":"opengauss",
                            "ecs_index":{"database":str(incoming),"graph_storage":"reference"}})
        plan = study.current(store)
        symbol = store.db.execute("SELECT id,json_extract(data,'$.evidence') evidence FROM symbols WHERE run=? AND name='cg_compute' AND json_extract(data,'$.definition')=1", (plan["run"],)).fetchone()
        body = store.read_evidence(symbol["evidence"])
        assert "return value + 1" in body["text"]
        unit = {"id":"fixture:increment", "kind":"claim", "title":"Fixture increment mechanism", "body":"The synthetic fixture returns value + 1.",
                "statement":"The fixture computes input plus one.","conditions":["Input plus one is representable as int"],
                "counterexamples":["INT_MAX overflows; this condition excludes it"],"source_refs":[symbol["evidence"]], "symbol_refs":[symbol["id"]]}
        accept(store, unit)
        return store, plan, unit
    except BaseException:
        store.close()
        raise


def accept(store, unit):
    plan = study.current(store)
    proposal = knowledge.propose(store, {"snapshot":plan["snapshot"],"run":plan["run"],"profile":plan["profile"],
        "author":"synthetic-fixture-author","expected_head":store.get_meta("knowledge_head"),"units":[unit],
        "import_provenance":{"kind":"synthetic-software-protocol-test","not_product_acceptance":True}})
    context = knowledge.review_context(store, proposal["id"], "synthetic-fixture-reviewer")
    assert not context["truncated"]
    return knowledge.review(store, proposal["id"], {"reviewer":"synthetic-fixture-reviewer","mode":"independent_review","verdict":"accept",
        "notes":"Synthetic protocol test actors, not a database expert review or real product acceptance.","proposal_digest":context["proposal_digest"]})
