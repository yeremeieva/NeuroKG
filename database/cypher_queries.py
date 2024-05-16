from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs.graph_document import GraphDocument
import langchain_openai
import typing as t

from utils.debugger import logger
from utils.reader import read_txt
from database.init_database import init_knowledge_base
from constants.constants import QUERIES
from chat.openai_parser import find_doi


load_dotenv()
url = os.getenv('DB_URL')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASS')

driver = GraphDatabase.driver(url, auth=(username, password))


def add_doi(graph_document: GraphDocument, paper_name: str):
    try:
        paper_text = read_txt(f'./data/txt_papers/{paper_name[7:]}')
        doi = find_doi(paper_text)
        print(paper_name)
        if doi == 'NO DOI FOUND':
            doi = f'paper_name: {paper_name[13:]}'
        for node in graph_document.nodes:
            node_name = node.properties['name']
            node_type = node.type
            doi_list = []
            if 'DOI' in node.properties:
                doi_list = node.properties['DOI']

            doi_list.append(doi)

            cypher_query = f'MATCH(n: `{node_type}` {{name: "{node_name}"}}) SET n.DOI = {doi_list} RETURN n'

            with driver.session() as session:
                session.run(cypher_query)

    except Exception as e:
        logger.exception(f'not successfully added DOI by cypher_query, exception "{e}"')


def get_nodes_and_labels() -> dict:
    cypher_query = """MATCH (n) 
                      RETURN n.id AS node_id, labels(n) AS node_label"""
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


def query_scheme(cypher_query: str, query_type: str) -> t.Optional:
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

    chain.run("What does contribute to Alzheimer'S Disease?")


if __name__ == '__main__':
    print(language_query())
