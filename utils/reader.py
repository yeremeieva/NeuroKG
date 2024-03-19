import PyPDF2
import os
from langchain.docstore.document import Document

from utils.debugger import logger


def list_files(folder_path, ending):
    try:
        files = os.listdir(folder_path)
        files_names = []
        for file in files:
            if file.lower().endswith(ending):
                files_names.append(file)
        return files_names
    except IOError as e:
        logger.exception(f'not successful list of files, exception "{e}"')


def read_pdf(path_pdf):
    if not os.path.exists(path_pdf):
        logger.info(f"The folder '{path_pdf}' does not exist.")
        return
    try:
        text = ""
        with open(path_pdf, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text
    except Exception as e_read:
        logger.exception(f'not successful read of pdf, exception "{e_read}"')


def read_txt(path_pdf):
    if not os.path.exists(path_pdf):
        logger.info(f"The folder '{path_pdf}' does not exist.")
        return
    try:
        with open(path_pdf, "r") as file:
            return file.read()
    except Exception as e_read:
        logger.exception(f'not successful read of txt, exception "{e_read}"')


def write_txt(path_txt, text):
    with open(path_txt, 'w') as file:
        file.writelines(text)


# class Document:
#     def __init__(self, page_content, metadata=None):
#         self.page_content = page_content
#         self.metadata = metadata if metadata is not None else {}

def txt_to_doc(file_path):
    text_content = read_txt(file_path)
    metadata = {
        'title': file_path[36:-4],
        'summary': 'no',
        'source': file_path,
        'id': 1
    }
    return Document(text_content, metadata=metadata)

# if __name__ == '__main__':
#     doc = txt_to_doc('data/txt_parsed_papers/parsed_paper_innovations.txt')
#
#     text_splitter = TokenTextSplitter(chunk_size=2048, chunk_overlap=24)
#
#     documents = text_splitter.split_documents([doc])
#     print(documents)