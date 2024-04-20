from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.chains import ConversationChain, LLMChain
import langchain_openai
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback
import tiktoken
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from dotenv import load_dotenv
import os

from database.init_database import KnowledgeGraph
from utils.debugger import logger
from utils.reader import split_text_by_tokens

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
os.getenv('OPENAI_API_KEY')


# def split_text_by_tokens(text : str, token_limit=80):
#     try:
#         text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
#             chunk_size=token_limit, chunk_overlap=0
#         )
#         chunks = text_splitter.split_text(text)
#         print(len(chunks))
#         return chunks
#     except Exception as e:
#         logger.exception(f'not successfully split txt by tokens, exception "{e}"')


def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.invoke(query)
        # logger.info(f'Spent a total of {cb.total_tokens} tokens')
    return result


# def replace_memory():
#   AImem = []
#   for index,value in enumerate(memory.dict()['chat_memory']['messages']):
#     if value['type']=='ai':
#       AImem.append(memory.dict()['chat_memory']['messages'][index]['content'])
#
#   memory.clear()
#
#   for ai_mem in AImem:
#     memory.chat_memory.add_ai_message(ai_mem)


def txt_to_parsed_txt_openai(text_to_parse: str,  temperature=0.2) -> str:
    try:
        chunks = split_text_by_tokens(text_to_parse, 2000)

        llm = ChatOpenAI(
            temperature=temperature,
            model_name="gpt-4-turbo-preview"
        )

        template = """You need to provide summary of the large scientific papers about neuroscience. 
        During the conversation you will get around 80 tokens from the paper and you have to write your summary about this part.
        If Previous parts are not provided, than it is the first chunk of the paper.
        If you have Previous parts and summaries, your task is to extend existing summary with new details from the new chunk of the paper.
        Later this summaries will be used to create neuroscientific knowledge graph, so keep in mind to select detailed and valuable information.
        Every time return full summary, do not shorten it.

        Previous parts of paper and AI summary:
        {chat_history}

        New part of the paper: {chunk}
        Extended summary:"""
        prompt = PromptTemplate.from_template(template)
        memory = ConversationBufferWindowMemory(k=1, memory_key="chat_history")
        conversation = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=memory
        )
        try:
            result = ''
            for chunk in chunks:
                result = conversation.invoke({"chunk": chunk})
            return result['text']

        except Exception as e:
            logger.exception(f'not successful conversation with chunks and fucking chat gpt, exception "{e}"')
    except Exception as e:
        logger.exception(f'not successfully parsing text with fucking chat gpt, exception "{e}"')


def create_node_label_openai(node_name: str,  temperature=0.7) -> str:
    try:
        response = client.chat.completions.create(model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": f"You: Label with one word this node {node_name} for neuroscientific knowledge graph"},
        ],
        temperature=temperature)
        return response.choices[0].message.content
    except Exception as e:
        logger.exception(f'not successfully created new label with fucking chat gpt, exception "{e}"')

def prompt_to_create_knowledge_openai():
    os.getenv('OPENAI_API_KEY')
    llm = langchain_openai.ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
    prompt = ChatPromptTemplate.from_messages(
        [("system",
          f"""# Knowledge Graph Instructions for GPT-4
## 1. Overview
You are a top-tier algorithm designed for extracting information from neuro scientific papers in structured formats to build a knowledge graph.Nodes represent entities and concepts like disease, treatment, etc.
Node(id='Neurological and psychiatric side effects', type='Adverse Effect')] rels=[Relationship(source=Node(id='H.A. Wishart'), target=Node(id='Journal of Neurology, Neurosurgery, and Psychiatry'), type='Published In')
## 2. Labeling Nodes
- **Consistency**: Ensure you use basic or elementary types for node labels.
  - For example, when you identify an entity representing a brain area, always label it as **"Brain Area"**. Avoid using more specific terms like "region" or "anatomy structure".
- **Node IDs**: Never utilize integers as node IDs. Node IDs should be names or human-readable identifiers found

## 3. Handling Numerical Data and Dates
- Numerical data, like age or other related information, should be incorporated as attributes or properties of the respective nodes.
- **No Separate Nodes for Dates/Numbers**: Do not create separate nodes for dates or numerical values. Always attach them as attributes or properties of nodes.
- **Property Format**: Properties must be in a key-value format.
- **Quotation Marks**: Never use escaped single or double quotes within property values.
- **Naming Convention**: Do not space for property keys and use title case, e.g., `BirthDate`.
## 4. Coreference Resolution
- **Maintain Entity Consistency**: When extracting entities, it's vital to ensure consistency.
If an entity, such as "John Doe", is mentioned multiple times in the text but is referred to by different names or pronouns (e.g., "Joe", "he"),
always use the most complete identifier for that entity throughout the knowledge graph. In this example, use "John Doe" as the entity ID.
Save acronyms and abbreviations as attributes or properties of the respective nodes. Never include them in nodes id and name.
Remember, the knowledge graph should be coherent and easily understandable for scientists, so maintaining consistency in entity references is crucial.
## 5. Strict Compliance
Adhere to the rules strictly. Non-compliance will result in termination.
          """),
            ("human", "Use the given format to extract information from the following input: {input}"),
            ("human", "Tip: Make sure to answer in the correct format"),
        ])
    return create_structured_output_chain(KnowledgeGraph, llm, prompt, verbose=False)