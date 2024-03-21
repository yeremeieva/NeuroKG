from utils.reader import list_files, read_pdf, write_txt, read_txt
from chat.openai_parser import txt_to_parsed_txt_openai
from utils.debugger import logger

import time

def pdf_to_txt(input_papers):
    for paper_name_pdf in input_papers:
        paper_text = read_pdf(f'./data/pdf_papers/{paper_name_pdf}')
        try:
            write_txt(f'./data/txt_papers/paper_{paper_name_pdf[:-4]}.txt', paper_text)
        except Exception as e:
            logger.exception(f'not successfully wrote txt to folder txt_papers, exception "{e}"')

def txt_to_parsed_txt(input_papers):
    for paper in input_papers:
        try:
            text = read_txt(f'./data/txt_papers/{paper}')
            result = txt_to_parsed_txt_openai(str(text))
            try:
                write_txt(f'./data/txt_parsed_papers/parsed_{paper}', result)
                logger.info(f'paper {paper} is parsed')
                time.sleep(3)
            except Exception as e:
                logger.exception(f'not successfully wrote parsed txt to folder txt_parsed_papers, exception "{e}"')
        except Exception as e:
            logger.exception(f'not successfully read txt from folder txt_papers, exception "{e}"')


if __name__ == "__main__":
    start_time = time.time()

    papers_pdf = list_files('./data/pdf_papers', ending='.pdf')
    logger.info(f'number of papers is {len(papers_pdf)}')
    pdf_to_txt(papers_pdf)
    logger.info('Good News!!!! Converted pdf papers to txt papers')

    papers_txt = list_files('./data/txt_papers', ending='.txt')
    txt_to_parsed_txt(papers_txt)
    logger.info('Good News!!!! Converted txt to parsed txt by chat gpt')

    end_time = time.time()
    time = end_time - start_time
    print(f"Time taken: {time/60:.2f} minutes")

