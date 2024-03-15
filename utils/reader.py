import PyPDF2
import os

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
        with open(path_pdf, "rb") as file:
            return file.read()
    except Exception as e_read:
        logger.exception(f'not successful read of txt, exception "{e_read}"')


def write_txt(path_txt, text):
    with open(path_txt, 'w') as file:
        file.writelines(text)