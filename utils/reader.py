import PyPDF2
import os
from langchain.docstore.document import Document
from typing import Optional
import nltk
# nltk.download('punkt')

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
            for page_num in range(num_pages - 2):
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

def split_text_by_tokens(text, token_limit):
    tokens = nltk.word_tokenize(text)
    num_tokens = len(tokens)
    num_chunks = num_tokens // token_limit + (1 if num_tokens % token_limit != 0 else 0)
    chunks = []
    for i in range(num_chunks):
        start_index = i * token_limit
        end_index = min((i + 1) * token_limit, num_tokens)
        chunk = ' '.join(tokens[start_index:end_index])
        chunks.append(chunk)
    return chunks

# if __name__ == '__main__':
#     long_text = " "
#     result = split_text_by_tokens(long_text, 5)
#     for i, elem in enumerate(result):
#         print(f"Chunk {i + 1}:", elem)