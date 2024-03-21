from openai import OpenAI
from langchain.chains.openai_functions import create_structured_output_chain
import langchain_openai
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

from database.neo4j_database import KnowledgeGraph
from utils.debugger import logger

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def txt_to_parsed_txt_openai(text_to_parse: str,  temperature=0.7) -> str:
    try:
        response = client.chat.completions.create(model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You: rewrite text but do not include information about author, journal, year and do not use abbreviations or acronyms, only full names" + text_to_parse},
        ],
        temperature=temperature)
        return response.choices[0].message.content
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
{'- **Allowed Node Labels:**' + ", ".join(['Medical Condition', 'Medical Procedure', 'Symptom', 'Innovation', 'Condition', 'Brain area', 'Disease', 'Treatment', 'Psychiatric Disorder'])}
## 3. Handling Numerical Data and Dates
- Numerical data, like age or other related information, should be incorporated as attributes or properties of the respective nodes.
- **No Separate Nodes for Dates/Numbers**: Do not create separate nodes for dates or numerical values. Always attach them as attributes or properties of nodes.
- **Property Format**: Properties must be in a key-value format.
- **Quotation Marks**: Never use escaped single or double quotes within property values.
- **Naming Convention**: Use space for property keys, e.g., `Birth Date`.
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