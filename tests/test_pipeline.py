import pytest
from app.services.chain import build_chain, store

pytestmark = pytest.mark.integration


def test_pipeline_returns_answer(require_env):
    chain = build_chain("general")
    result = chain.invoke(
        {"question": "What does FinSolve do?"},
        config={"configurable": {"session_id": "test:pipeline-basic"}},
    )
    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_pipeline_rbac_isolation(require_env):
    "Marketing user asking about finance data should get a refusal, not financial figures"
    chain = build_chain("marketing")
    result = chain.invoke(
        {"question": "What are FinSolve's quarterly revenue figures?"},
        config={"configurable": {"session_id": "test:pipeline-rbac"}},
    )
    print(f"\nLLM response: {result}")
    refusal_signals = [
        "don't have", "not available", "cannot", "no information",
        "context doesn't", "don't know", "do not have", "unable", "not contain",
    ]
    assert any(signal in result.lower() for signal in refusal_signals)


def test_pipeline_conversation_memory(require_env):
    "Two turns with the same session_id should populate the session store"
    session_id = "test:pipeline-memory"
    chain = build_chain("hr")

    chain.invoke(
        {"question": "What is FinSolve's HR policy?"},
        config={"configurable": {"session_id": session_id}},
    )
    chain.invoke(
        {"question": "Can you summarise that?"},
        config={"configurable": {"session_id": session_id}},
    )

    assert session_id in store
    assert len(store[session_id].messages) >= 2