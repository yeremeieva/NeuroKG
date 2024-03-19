from utils.reader import list_files, read_pdf, write_txt, read_txt
from utils.parser import parse_text_gpt
from utils.debugger import logger

import time

def pdf_to_txt(input_papers):
    for paper_name_pdf in input_papers:
        paper_text = read_pdf(f'./data/pdf_papers/{paper_name_pdf}')
        try:
            write_txt(f'./data/txt_papers/paper_{paper_name_pdf[:-4]}.txt', paper_text)
        except Exception as e:
            logger.exception(f'not successfully write pdf, exception "{e}"')

def txt_to_parsed_txt(input_papers):
    for paper in input_papers:
        try:
            text = read_txt(f'./data/txt_papers/{paper}')
            result = parse_text_gpt(str(text))
            try:
                write_txt(f'./data/txt_parsed_papers/parsed_{paper}', result)
                logger.info(f'paper {paper} is parsed')
            except Exception as e:
                logger.exception(f'not successfully write parsed txt, exception "{e}"')
        except Exception as e:
            logger.exception(f'not successfully read txt, exception "{e}"')


if __name__ == "__main__":
    start_time = time.time()

    papers_pdf = list_files('./data/pdf_papers', ending='.pdf')
    pdf_to_txt(papers_pdf)
    logger.info('converted pdf to txt')

    papers_txt = list_files('./data/txt_papers', ending='.txt')
    txt_to_parsed_txt(papers_txt)
    logger.info('converted txt to parsed txt by chat gpt')

    end_time = time.time()
    time = end_time - start_time
    print(f"Time taken: {time:.2f} seconds")

