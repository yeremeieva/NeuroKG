import PyPDF2
import os
from langchain.docstore.document import Document
from typing import Optional

from utils.debugger import logger


def list_files(folder_path: str, ending: str) -> Optional[list[str]]:
    if not os.path.exists(folder_path):
        logger.info(f"The folder '{folder_path}' does not exist.")
        return
    try:
        files = os.listdir(folder_path)
        files_names = []
        for file in files:
            if file.lower().endswith(ending):
                files_names.append(file)
        return files_names
    except IOError as e:
        logger.exception(f'not successful list of files, exception "{e}"')


def read_pdf(file_path: str) -> Optional[str]:
    if not os.path.exists(file_path):
        logger.info(f"The folder '{file_path}' does not exist.")
        return
    try:
        text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(5):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text
    except Exception as e_read:
        logger.exception(f'not successful read of pdf, exception "{e_read}"')


def read_txt(file_path: str) -> Optional[str]:
    if not os.path.exists(file_path):
        logger.info(f"The folder '{file_path}' does not exist.")
        return
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e_read:
        logger.exception(f'not successful read of txt, exception "{e_read}"')


def write_txt(file_path: str, text: str) -> None:
    try:
        with open(file_path, 'w') as file:
            file.writelines(text)
    except Exception as e_read:
        logger.exception(f'not successful read of txt, exception "{e_read}"')


def txt_to_doc(file_path: str) -> Optional[Document]:
    if not os.path.exists(file_path):
        logger.info(f"The folder '{file_path}' does not exist.")
        return
    try:
        text_content = read_txt(file_path)
        metadata = {
            'title': file_path[38:-4],
            'summary': 'no',
            'source': file_path,
            'id': 1
        }
        return Document(text_content, metadata=metadata)
    except Exception as e:
        logger.exception(f'not successfully read txt, exception "{e}"')


# if __name__ == '__main__':
#     doc = txt_to_doc('data/txt_parsed_papers/parsed_paper_innovations.txt')
#
#     text_splitter = TokenTextSplitter(chunk_size=2048, chunk_overlap=24)
#
#     documents = text_splitter.split_documents([doc])
#     print(documents)