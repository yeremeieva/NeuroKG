from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

from utils.debugger import logger


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


if __name__ == '__main__':
    print(get_nodes_and_labels())


# from langchain.chains import GraphCypherQAChain
#
# graph.refresh_schema()
#
# cypher_chain = GraphCypherQAChain.from_llm(
#     graph=graph,
#     cypher_llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
#     qa_llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
#     validate_cypher=True,
#     verbose=True
# )
#
# cypher_chain.invoke({"query": "What Deep Brain Stimulation treats?"})