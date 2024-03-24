from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
from langchain.chains import GraphCypherQAChain
import langchain_openai

from utils.debugger import logger
from database.init_database import init_graph


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


def get_graph_diameter() -> int:
    cypher_query = """MATCH (n)
                      WITH collect(n) AS nodes
                      UNWIND nodes AS a
                      UNWIND nodes AS b
                      WITH a, b
                      WHERE id(a) < id(b)
                      MATCH path=shortestPath((a)-[*]-(b))
                      RETURN length(path) AS diameter
                      ORDER BY diameter
                      DESC LIMIT 1"""

    try:
        with driver.session() as session:
            result = session.run(cypher_query)

            return result.data('diameter')[0]

    except Exception as e:
        logger.exception(f'not successfully calculated diameter by cypher_query, exception "{e}"')



def language_query():
    os.getenv('OPENAI_API_KEY')

    graph = init_graph()
    graph.refresh_schema()

    chain = GraphCypherQAChain.from_llm(
        langchain_openai.ChatOpenAI(temperature=0, model="gpt-4-turbo-preview"), graph=graph, verbose=True, validate_cypher=False
    )

    chain.run("What Deep Brain Stimulation (Medicalprocedure) treats?")
#
# if __name__ == '__main__':
    # print(get_nodes())
