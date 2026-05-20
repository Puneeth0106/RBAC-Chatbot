import pytest
from app.services.indexing import tag_chunks
from langchain_core.documents import Document


def test_role_is_tagged_correctly():
    "Check that the role is correctly assigned to chunk metadata"
    chunk = Document(metadata={'header': 1}, page_content="Hello")
    result = tag_chunks([chunk], "finance")
    assert result[0].metadata["role"] == "finance"


def test_all_roles_tagged_correctly():
    "Check that all five roles are correctly tagged without typos"
    roles = ["engineering", "finance", "marketing", "hr", "general"]
    for role in roles:
        chunk = Document(page_content="Some content.")
        result = tag_chunks([chunk], role)
        assert result[0].metadata["role"] == role


def test_every_chunk_has_role_key():
    "Check that no chunk is missing the role key after tagging"
    chunks = [Document(page_content=f"chunk {i}") for i in range(5)]
    result = tag_chunks(chunks, "hr")
    for chunk in result:
        assert "role" in chunk.metadata


def test_role_does_not_bleed():
    "Check that a chunk tagged with one role does not carry another role"
    chunks = [Document(page_content="Sensitive finance data.")]
    result = tag_chunks(chunks, "finance")
    assert result[0].metadata["role"] != "marketing"
