from openai import OpenAI



from utils.debugger import logger
client = OpenAI(api_key='')
def parse_raw_text_gpt(text_to_parse,  temperature=0.7):
    try:
        response = client.chat.completions.create(model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You: rewrite text but do not include information about author, journal, year and do not use abbreviations or acronyms, only full names" + text_to_parse},
        ],
        temperature=temperature)
        return response.choices[0].message.content
    except Exception as e:
        logger.exception(f'not successfully parsing text with fucking chat gpt, exception "{e}"')


def create_label(node_name,  temperature=0.7):
    try:
        response = client.chat.completions.create(model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": f"You: Label with one word this node {node_name} for neuroscientific knowledge graph"},
        ],
        temperature=temperature)
        return response.choices[0].message.content
    except Exception as e:
        logger.exception(f'not successfully parsing text with fucking chat gpt, exception "{e}"')
