"""Thin RAGFlow 1.0 HTTP adapter. Credentials are resolved from the operator's environment."""
import os
from urllib.parse import urlparse, quote

from .store import digest, require

RETRIEVAL_KEYS = {"similarity_threshold", "keywords_similarity_weight", "knn_top_k", "knn_num_candidates", "rerank_candidates_count", "cross_languages"}


def validate(config):
    require(isinstance(config, dict) and config.get("kind") in {"local", "ragflow"}, "Choose an explicit local or ragflow retrieval provider")
    allowed = {"kind", "base_url", "api_key_env", "embedding_model", "rerank_model", "retrieval", "parser_config"}
    require(not set(config) - allowed, "Unknown provider configuration fields; use environment references for secrets")
    if config["kind"] == "ragflow":
        address = urlparse(config.get("base_url", ""))
        require(address.scheme in {"http", "https"} and address.hostname and not address.username and not address.password and not address.query and not address.fragment, "Invalid RAGFlow endpoint")
        require(isinstance(config.get("api_key_env"), str) and config["api_key_env"], "Provide api_key_env, never an inline credential")
        require(isinstance(config.get("embedding_model"), str) and config["embedding_model"], "Lock the actual embedding model ID")
    require(isinstance(config.get("retrieval", {}), dict) and not set(config.get("retrieval", {})) - RETRIEVAL_KEYS, "Unsupported retrieval settings")
    return config


class Ragflow:
    def __init__(self, config, *, client=None):
        import httpx
        self.config = validate(config)
        require(config["kind"] == "ragflow", "RAGFlow configuration required")
        token = os.environ.get(config["api_key_env"])
        require(token, "RAGFlow API credential environment variable is missing")
        self.client = client or httpx.Client(timeout=httpx.Timeout(30, connect=5), follow_redirects=False)
        self.owned = client is None
        self.headers = {"Authorization": "Bearer " + token}
        self.base = config["base_url"].rstrip("/") + "/api/v1"

    def close(self):
        if self.owned:
            self.client.close()

    def request(self, method, path, *, raw=False, **kwargs):
        # Do not surface response bodies or credential-bearing request representations in errors.
        with self.client.stream(method, self.base + path, headers=self.headers, **kwargs) as response:
            require(200 <= response.status_code < 300, "RAGFlow HTTP failure: " + str(response.status_code))
            chunks, size = [], 0
            for chunk in response.iter_bytes():
                size += len(chunk)
                require(size <= 8_000_000, "RAGFlow response exceeds byte budget")
                chunks.append(chunk)
            body = b"".join(chunks)
        if raw:
            return body
        import json
        value = json.loads(body)
        require(isinstance(value, dict) and value.get("code") == 0, "RAGFlow returned a non-success business code")
        return value.get("data")

    def dataset(self, release_id):
        name = "source-kb-" + digest(release_id)[:28]
        rows = self.request("GET", "/datasets", params={"name":name,"page":1,"page_size":100})
        require(isinstance(rows, list), "Unexpected RAGFlow dataset list")
        exact = [r for r in rows if r.get("name") == name]
        require(len(exact) <= 1, "Ambiguous release datasets; reconcile duplicate creation before continuing")
        if exact:
            result = exact[0]
        else:
            result = self.request("POST", "/datasets", json={"name":name,"parse_type":1,"parser_id":"general","language":"Chinese",
                "embedding_model":self.config["embedding_model"], "permission":"me", "parser_config":self.config.get("parser_config", {})})
        require(isinstance(result, dict) and result.get("id"), "RAGFlow dataset identity missing")
        if result.get("embedding_model"):
            require(result["embedding_model"] == self.config["embedding_model"], "RAGFlow embedding model differs from release configuration")
        return result["id"]

    def documents(self, dataset, *, name=None, document_id=None):
        params = {"page":1,"page_size":100}
        if name:
            params["name"] = name
        if document_id:
            params["id"] = document_id
        result = self.request("GET", "/datasets/" + quote(dataset, safe="") + "/documents", params=params)
        require(isinstance(result, dict) and isinstance(result.get("docs"), list), "Unexpected RAGFlow document list")
        require(result.get("total", len(result["docs"])) <= 100, "Document reconciliation is ambiguous; narrow the exact identity")
        return result["docs"]

    def ensure_document(self, dataset, name, body, metadata):
        path = "/datasets/" + quote(dataset, safe="") + "/documents"
        rows = [d for d in self.documents(dataset, name=name) if d.get("name") == name]
        require(len(rows) <= 1, "Duplicate published document name")
        if rows:
            doc = rows[0]
        else:
            created = self.request("POST", path, files={"file":(name, body, "text/markdown")})
            require(isinstance(created, list) and len(created) == 1, "Unexpected upload receipt")
            doc = created[0]
        docid = doc["id"]
        stored = self.request("GET", path + "/" + quote(docid, safe=""), raw=True)
        require(stored == body, "Remote document bytes differ from authoritative export")
        if doc.get("meta_fields") != metadata:
            self.request("PATCH", path + "/" + quote(docid, safe=""), json={"meta_fields":metadata})
        state = str(doc.get("run", "UNSTART")).upper()
        if state in {"UNSTART", "0", "FAIL", "3", "CANCEL", "4"}:
            self.request("POST", "/datasets/" + quote(dataset, safe="") + "/chunks", json={"document_ids":[docid]})
        current = [d for d in self.documents(dataset, document_id=docid) if d.get("id") == docid]
        require(len(current) == 1, "Published document disappeared")
        require(current[0].get("meta_fields") == metadata, "Published metadata did not persist")
        ready = str(current[0].get("run")).upper() in {"DONE", "2"} and current[0].get("chunk_count", 0) > 0
        return {"document_id":docid,"ready":ready,"parse_status":current[0].get("run"),"document_hash":digest(body)}

    def retrieve(self, dataset, release_id, question, limit=20):
        payload = {**self.config.get("retrieval", {}), "question":question,"dataset_ids":[dataset],"page":1,"page_size":limit,
                   "highlight":False,"use_kg":False,"include_knowledge_compilation":False,
                   "metadata_condition":{"logic":"and","conditions":[{"name":"release_id","comparison_operator":"=","value":release_id}]}}
        if self.config.get("rerank_model"):
            payload["rerank_id"] = self.config["rerank_model"]
        value = self.request("POST", "/retrieval", json=payload)
        require(isinstance(value, dict) and isinstance(value.get("chunks"), list), "Unexpected retrieval response")
        return value["chunks"]
