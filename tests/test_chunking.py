from langchain_core.documents import Document
from app.services.indexing import splitting_docs
from app.services.config import DATA_PATH, CHUNK_SIZE

def test_chunk_size():
    fake_doc= Document(page_content= "# Header\n\n"+ "word"*300 + "# Header2 \n\n" + "second" *300, metadata= {'source': str(DATA_PATH / "finance" / "report.md")})
    chunks= splitting_docs([fake_doc])
    for chunk in chunks:
        assert len(chunk.page_content)<= CHUNK_SIZE


def test_white_spaced_chunk():
    "Test to check if the chunk only consists of white space"
    fake_doc1= Document(page_content= "# Header\n\n"+ "word"*300 + "# Header2 \n\n" + '   '*500 + "second" *300, metadata= {'source': str(DATA_PATH / "finance" / "report.md")})
    chunks= splitting_docs([fake_doc1])
    for chunk in chunks:
        assert len(chunk.page_content.strip()) >0


def test_headers_appear_in_metadata():
    "Test to check whether header is included in metadta"
    fake_doc1= Document(page_content= "# Financial Policy\n\n"+ "word"*300 + "# Header2 \n\n" + "second" *300, metadata= {'source': str(DATA_PATH / "finance" / "report.md")})
    chunks= splitting_docs([fake_doc1])
    assert any(["Financial Policy" in chunk.metadata.values()  for chunk in chunks  ])


def test_document_with_less_characters():
    "Document with char less than 500 shouldnt split"
    fake_doc1= Document(page_content="This is a short document with real words. " * 5, metadata= {'source': str(DATA_PATH / "finance" / "report.md")})
    chunks= splitting_docs([fake_doc1])
    assert len(chunks)==1


def test_multiple_docs():
    "Check you get chunks back from multiple documents "
    fake_doc1= Document(page_content="*"*400, metadata= {'source': str(DATA_PATH / "finance" / "report.md")})
    fake_doc2= Document(page_content=";"*400,  metadata= {'source': str(DATA_PATH / "finance" / "report.md")})

    chunks= splitting_docs([fake_doc1,fake_doc2])

    all_content = "".join(c.page_content for c in chunks)
    assert "*" in all_content
    assert ";" in all_content 


def test_content_lost():
    "Check if the content is lost after splitting."
    fake_doc= Document(page_content="Hi, myself Puneeth. I am an Applied Computer Science graduate student.", metadata= {'source': str(DATA_PATH / "finance" / "report.md")})
    chunks= splitting_docs([fake_doc])
    all_content = "".join(c.page_content for c in chunks)
    original_doc= "Hi, myself Puneeth. I am an Applied Computer Science graduate student.".split(' ')
    assert all([word in all_content for word in original_doc])

def test_metadata_source_path():
    fake_doc= Document(page_content="Hi, myself Puneeth. I am an Applied Computer Science graduate student.",  metadata= {'source': str(DATA_PATH / "finance" / "report.md")})
    chunks= splitting_docs([fake_doc])
    for chunk in chunks:
        assert chunk.metadata['source'] == "finance/report.md"