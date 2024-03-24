from vertexai.preview.generative_models import GenerativeModel
import vertexai
from dotenv import load_dotenv
import os

from utils.debugger import logger

load_dotenv()

vertexai.init(project=os.getenv('VERTEXAI_PROJECT'))

def txt_to_parsed_txt_gemini(text_to_parse: str):
    try:
        gemini_pro_model = GenerativeModel("gemini-1.0-pro")
        model_response = gemini_pro_model.generate_content(f"""Write a summary of the scientific paper but include as much valuable knowledge as you 
        can, do not include information about author, journal, year, methods and tested groups. Do not use any 
        abbreviations or acronyms, only full names" + {text_to_parse}""")
        return model_response.text
    except Exception as e:
        logger.exception(f'not successfully parsing text with this gemini ai, exception "{e}"')

# if __name__ == '__main__':
#     txt_to_parsed_txt_gemini()
