import importlib.util
import os
import sys
import pytest


def load_module():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rag-pipeline.py'))
    spec = importlib.util.spec_from_file_location("rag_pipeline_module", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["rag_pipeline_module"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_validate_docs_path(tmp_path):
    mod = load_module()
    nonexist = tmp_path / "nope"
    with pytest.raises(FileNotFoundError):
        mod.validate_docs_path(str(nonexist))
    # existing dir should not raise
    mod.validate_docs_path(str(tmp_path))


def test_load_documents_empty(tmp_path):
    mod = load_module()
    docs = mod.load_documents(str(tmp_path))
    assert docs == []


def test_split_into_chunks_raises_on_empty():
    mod = load_module()
    with pytest.raises(RuntimeError):
        mod.split_into_chunks([])


def test_build_vectorstore_with_retries(monkeypatch):
    mod = load_module()
    called = {}

    class DummyEmb:
        def __init__(self, model):
            called['emb_model'] = model

    class DummyFAISS:
        @staticmethod
        def from_documents(chunks, emb):
            called['chunks_len'] = len(chunks)
            called['emb'] = emb
            return "VS"

    monkeypatch.setattr(mod, 'OpenAIEmbeddings', DummyEmb)
    monkeypatch.setattr(mod, 'FAISS', DummyFAISS)
    vs = mod.build_vectorstore_with_retries([1, 2, 3])
    assert vs == "VS"
    assert called['chunks_len'] == 3
    assert called['emb_model'] == "text-embedding-3-large"


def test_run_query_with_retries():
    mod = load_module()

    class DummyChain:
        def __call__(self, args):
            return {"result": "ok", "source_documents": []}

    res = mod.run_query_with_retries(DummyChain(), "q?")
    assert isinstance(res, dict) and res['result'] == "ok"
