from langchain.docstore.document import Document
from langchain_community.graphs.graph_document import GraphDocument
from tqdm import tqdm
import time

from database.neo4j_database import map_to_base_node, map_to_base_relationship, add_node_history
from database.init_database import init_graph
from chat.openai_parser import prompt_to_create_knowledge_openai
from utils.reader import list_files, txt_to_doc
from utils.debugger import logger


def extract_and_store_graph(document: Document) -> None:
    extract_chain = prompt_to_create_knowledge_openai()
    data = extract_chain.invoke(document.page_content)['function']

    nodes = [map_to_base_node(node) for node in data.nodes]
    rels = [map_to_base_relationship(rel) for rel in data.rels]
    print('doc name: '+ document.metadata['source'])
    print(f'rels nodes: {len(nodes)}')
    print(f'rels len: {len(rels)}')


    for node in nodes:
        add_node_history(node)

    for node in nodes:
        for rel in rels:
            if node.id == rel.source.id:
                rel.source = node
            elif node.id == rel.target.id:
                rel.target = node

    graph = init_graph()

    graph_document = GraphDocument(
      nodes= nodes,
      relationships = rels,
      source = document)

    graph.add_graph_documents([graph_document])

if __name__ == '__main__':
    start_time = time.time()
    model = 'openai'
    input_papers = list_files(f'./data/{model}_txt_parsed_papers', ending='.txt')
    documents = [txt_to_doc(f'./data/{model}_txt_parsed_papers/{paper}') for paper in input_papers]
    logger.info('Good News!!!! Parsed txt to documents')

    # extract_and_store_graph(documents[5])

    for i, d in tqdm(enumerate(documents), total=len(documents)):
        print(d.metadata['title'])
        extract_and_store_graph(d)

    logger.info('Exciting News!!!! All papers were written to the graph!!!!!!!!!')

    end_time = time.time()
    time = end_time - start_time
    print(f"Time taken: {time/60:.2f} minutes")