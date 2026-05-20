import pytest
from app.services.indexing import loading_docs


def test_returns_for_valid_directory(tmp_path):
    """Testing the loading_docs which takes Director-loader with markdown files"""
    #create a file at a temparay location
    file= tmp_path/'new-file.md'
    file.write_text("# Hello\n\nSome content.")
    #Pass the directory that contain temp_file
    docs= loading_docs(tmp_path)
    assert len(docs)>0

def test_all_docs_have_content(tmp_path):
    file= tmp_path/'new-file.md'
    file.write_text("# Hello\n\nSome content.")
    #Pass the directory that contain temp_file
    docs= loading_docs(tmp_path)
    for doc in docs:
        assert len(doc.page_content) >0

def test_ignores_non_markdown_files(tmp_path):
    file1= tmp_path/'md_file.md'
    file2= tmp_path/'csv_file.csv'
    file3= tmp_path/'csv_file.txt'
    file1.write_text("# Hello\n\nSome content.")
    file2.write_text("col1,col2\n1,2")
    file3.write_text("# Hello\n\nSome content.")
    docs = loading_docs(tmp_path)
    assert len(docs)==1


def test_empty_directory_returns_empty_list(tmp_path):
    docs = loading_docs(tmp_path)
    assert len(docs)==0