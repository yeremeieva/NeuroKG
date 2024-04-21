from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
from langchain.chains import GraphCypherQAChain
import langchain_openai
import typing as t

from utils.debugger import logger
from database.init_database import init_knowledge_base
from constants.constants import QUERIES


load_dotenv()
url = os.getenv('DB_URL')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASS')

driver = GraphDatabase.driver(url, auth=(username, password))


def get_nodes_and_labels() -> dict:
    cypher_query = "MATCH (n) RETURN n.id AS node_id, labels(n) AS node_label"
    dictionary = {}

    try:
        with driver.session() as session:
            result = session.run(cypher_query)

            for record in result:
                if record['node_id'] not in dictionary.keys():
                    dictionary[record['node_id'].lower()] = record['node_label'][0]

            return dictionary

    except Exception as e:
        logger.exception(f'not successfully loaded dictionary of nodes and labels by cypher_query, exception "{e}"')


def get_nodes() -> list[dict]:
    cypher_query = "MATCH (n) RETURN properties(n) as n_properties, labels(n) as n_labels"
    nodes = []

    try:
        with driver.session() as session:
            result = session.run(cypher_query)

            for record in result:
                dictionary = record['n_properties']
                dictionary['label'] = record['n_labels'][0]
                nodes.append(dictionary)
            return nodes

    except Exception as e:
        logger.exception(f'not successfully loaded dictionary of nodes and labels by cypher_query, exception "{e}"')


def query(query_type: str) -> t.Optional:
    try:
        cypher_query = QUERIES[query_type]
        result = query_scheme(cypher_query, query_type)
        return result

    except Exception as e:
        logger.exception(f'probably have not found your request in QUERIES, exception "{e}"')


def query_scheme(cypher_query:str, query_type:str) -> t.Optional:
    try:
        with driver.session() as session:
            result = session.run(cypher_query)
            return result.data()

    except Exception as e:
        logger.exception(f'not successfully counted {query_type} or processed your cypher query, exception "{e}"')


def language_query():
    os.getenv('OPENAI_API_KEY')

    knowledge_base = init_knowledge_base()
    knowledge_base.refresh_schema()

    chain = GraphCypherQAChain.from_llm(
        langchain_openai.ChatOpenAI(temperature=1, model="gpt-4-turbo-preview"), graph=knowledge_base, verbose=True, validate_cypher=False
    )

    chain.run("What Deep Brain Stimulation treats?")


# if __name__ == '__main__':
    # print(get_nodes())
