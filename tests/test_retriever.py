import pytest
from app.services.chain import build_retriever
from app.services.config import RETRIEVER_K

#This marker sets the test aside for pytest that include calling external services

pytestmark = pytest.mark.integration


def test_retriever_returns_docs(embedding):
    retriever = build_retriever(embedding, "engineering")
    docs = retriever.invoke("What CI/CD pipelines does FinSolve use?")
    assert len(docs) > 0


def test_retriever_respects_k(embedding):
    retriever = build_retriever(embedding, "engineering")
    docs = retriever.invoke("What CI/CD pipelines does FinSolve use?")
    assert len(docs) <= RETRIEVER_K


def test_retriever_rbac_filter(embedding):
    "All returned docs must belong to the queried role or general"
    retriever = build_retriever(embedding, "marketing")
    docs = retriever.invoke("What is FinSolve's marketing strategy?")
    for doc in docs:
        assert doc.metadata["role"] in {"marketing", "general"}


def test_retriever_rbac_isolation(embedding):
    "Engineering-tagged docs must never appear for a marketing user"
    retriever = build_retriever(embedding, "marketing")
    docs = retriever.invoke("CI/CD pipeline deployment infrastructure")
    for doc in docs:
        assert doc.metadata["role"] != "engineering"