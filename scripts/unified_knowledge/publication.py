"""Immutable knowledge exports, resumable retrieval synchronization and atomic activation."""
from copy import deepcopy
import time
import uuid

from . import study
from .knowledge import content_hash, freshness
from .query_api import source_manifest
from .ragflow_provider import Ragflow, validate
from .store import atomic_write, canonical, digest, identity, now, require

PREFIX = "retrieval-release:"


def get(store, release_id=None, *, ready=True):
    release_id = release_id or store.get_meta("active_retrieval_release")
    require(release_id, "No active retrieval release; prepare, synchronize and activate one")
    value = store.get_meta(PREFIX + release_id)
    require(value and value["id"] == release_id, "Unknown retrieval release")
    require(not ready or value["status"] == "ready", "Retrieval release is not ready")
    return value


def document(unit):
    # Preserve conditions and all specialized structures, not just the summary paragraph.
    value = {k:v for k,v in unit.items() if k not in {"_binding", "review"}}
    return ("# " + unit["title"] + "\n\n" + unit["body"] + "\n\n```json\n" + canonical(value) + "\n```\n").encode("utf-8")


def prepare(store, *, provider=None, revision=None):
    provider = deepcopy(validate(provider or {"kind":"local"}))
    plan = study.current(store)
    revision = revision or store.get_meta("knowledge_head")
    require(revision, "Accepted knowledge is required before publishing a retrieval release")
    record = store.record("revisions", revision)
    require((record["snapshot"], record["run"], record["profile"]) == (plan["snapshot"], plan["run"], plan["profile"]), "Knowledge revision differs from the current bound study")
    units = store.units(revision)
    require(units, "Cannot publish empty knowledge")
    stale = {uid: freshness(store, u, plan["snapshot"], plan["run"], units) for uid,u in units.items()}
    require(not any(stale.values()), "Stale knowledge must be re-reviewed before publishing")
    docs = {uid:{"content_hash":content_hash(u),"document_hash":digest(document(u)),"filename":digest(uid) + ".md"} for uid,u in units.items()}
    binding = source_manifest(store, plan)
    immutable = {"schema":"knowledge-retrieval-release/v1", "binding":binding,"knowledge_revision":revision,
                 "provider":provider,"retrieval_config_digest":digest(provider),"documents":docs}
    rid = identity("retrieval", immutable)
    key = PREFIX + rid
    folder = store.home / "retrieval-releases" / rid.replace(":", "-")
    for uid, spec in docs.items():
        atomic_write(folder / "documents" / spec["filename"], document(units[uid]))
    atomic_write(folder / "manifest.json", canonical({**immutable,"id":rid}) + "\n")
    with store.transaction():
        value = store.get_meta(key)
        if value:
            return value
        value = {**immutable, "id":rid,"created":now(),"status":"staging","sync":{},"dataset_id":None}
        store.set_meta(key, value)
        store.event("retrieval_release_prepared", {"id":rid,"revision":revision,"units":len(units)})
    return value


def _verify_export(store, value, uid):
    unit = store.units(value["knowledge_revision"], ids=[uid])[uid]
    spec = value["documents"][uid]
    require(content_hash(unit) == spec["content_hash"], "Authoritative knowledge hash mismatch")
    path = store.home / "retrieval-releases" / value["id"].replace(":", "-") / "documents" / spec["filename"]
    raw = path.read_bytes()
    require(digest(raw) == spec["document_hash"] and raw == document(unit), "Published export drift")
    return raw


def sync(store, release_id, *, max_documents=100, provider_client=None):
    require(type(max_documents) is int and 1 <= max_documents <= 1000, "max_documents must be 1..1000")
    value = get(store, release_id, ready=False)
    if value["status"] == "ready":
        return value
    token = uuid.uuid4().hex
    lockkey = "retrieval-sync-lock:" + release_id
    with store.transaction():
        lock = store.get_meta(lockkey, {})
        require(lock.get("deadline", 0) < time.time(), "Release synchronization already running")
        store.set_meta(lockkey, {"token":token,"deadline":time.time() + 600})
    client = None
    def save():
        with store.transaction():
            lock = store.get_meta(lockkey, {})
            require(lock.get("token") == token and lock.get("deadline", 0) > time.time(), "Synchronization lease expired")
            store.set_meta(lockkey, {"token":token,"deadline":time.time() + 600})
            store.set_meta(PREFIX + release_id, value)
    try:
        if value["provider"]["kind"] == "ragflow":
            client = Ragflow(value["provider"], client=provider_client)
            if not value["dataset_id"]:
                value["dataset_id"] = client.dataset(release_id)
                save()
        pending = [uid for uid in sorted(value["documents"]) if not value["sync"].get(uid, {}).get("ready")]
        for uid in pending[:max_documents]:
            raw = _verify_export(store, value, uid)
            spec = value["documents"][uid]
            if client:
                metadata = {"release_id":release_id,"unit_id":uid,"content_hash":spec["content_hash"],
                            "knowledge_revision":value["knowledge_revision"],"source_snapshot":value["binding"]["source_snapshot"],
                            "build_profile":value["binding"]["build_profile"]}
                receipt = client.ensure_document(value["dataset_id"], spec["filename"], raw, metadata)
            else:
                receipt = {"ready":True,"document_hash":spec["document_hash"],"provider":"local_fts_lexical_baseline"}
            value["sync"][uid] = receipt
            save()
        if all(value["sync"].get(uid, {}).get("ready") for uid in value["documents"]):
            value["status"] = "ready"
            value["ready_at"] = now()
        save()
        return value
    finally:
        if client:
            client.close()
        with store.transaction():
            if store.get_meta(lockkey, {}).get("token") == token:
                store.set_meta(lockkey, {})


def activate(store, release_id, *, expected_active=None):
    value = get(store, release_id)
    # Every activation, including rollback, verifies the local authoritative export.
    for uid in value["documents"]:
        _verify_export(store, value, uid)
    index = store.record("runs", value["binding"]["index_run"])
    require(index.get("facts_digest") == value["binding"]["index_facts_digest"], "Source index changed since release preparation")
    with store.transaction():
        current = store.get_meta("active_retrieval_release")
        require(current == expected_active or current == release_id, "Active release changed; provide the current expected_active")
        store.set_meta("active_retrieval_release", release_id)
        store.event("retrieval_release_activated", {"id":release_id,"previous":current})
    return {"active_release":release_id,"previous":current,"knowledge_revision":value["knowledge_revision"]}


def catalog(store):
    import json
    rows = store.db.execute("SELECT value FROM meta WHERE key LIKE ? ORDER BY key", (PREFIX + "%",))
    return {"active_release":store.get_meta("active_retrieval_release"), "releases":[
        {k:v[k] for k in ("id","status","knowledge_revision","dataset_id","created")} for v in map(lambda r:json.loads(r[0]), rows)]}
