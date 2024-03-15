from openai import OpenAI

client = OpenAI(api_key='')

from utils.debugger import logger

def parse_text_gpt(text_to_parse, max_tokens=4096, temperature=0.7):
    try:
        response = client.chat.completions.create(model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You: " + text_to_parse},
        ],
        max_tokens=max_tokens,
        temperature=temperature)

        return response.choices[0].message.content
    except Exception as e:
        logger.exception(f'not successfully parsing text with fucking chat gpt, exception "{e}"')


