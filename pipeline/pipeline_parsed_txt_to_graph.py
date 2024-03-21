from langchain.docstore.document import Document
from langchain_community.graphs.graph_document import GraphDocument
from tqdm import tqdm

from database.cypher_queries import get_nodes_and_labels
from database.neo4j_database import map_to_base_node, map_to_base_relationship, init_graph
from chat.openai_parser import prompt_to_create_knowledge_openai, create_node_label_openai
from utils.reader import list_files, txt_to_doc
from utils.debugger import logger


def check_label(node: str, label: str) -> str:
    dictionary = get_nodes_and_labels()
    if node.lower() in dictionary.keys():
        return dictionary[node.lower()]
    elif label == 'Node':
        return create_node_label_openai(node)
    else:
        return label

def extract_and_store_graph(document: Document) -> None:
    extract_chain = prompt_to_create_knowledge_openai()
    data = extract_chain.invoke(document.page_content)['function']

    nodes = []
    for node in data.nodes:
        node.type = str(check_label(node.id, node.type))
        map_to_base_node(node)
        nodes.append(map_to_base_node(node))

    for node in data.nodes:
        for rel in data.rels:
            if node.id == rel.source.id:
                rel.source = node
            elif node.id == rel.target.id:
                rel.target = node

    graph = init_graph()

    graph_document = GraphDocument(
      nodes=nodes,
      relationships = [map_to_base_relationship(rel) for rel in data.rels],
      source = document)

    graph.add_graph_documents([graph_document])

if __name__ == '__main__':
    input_papers = list_files('./data/txt_parsed_papers', ending='.txt')
    documents = [txt_to_doc(f'./data/txt_parsed_papers/{paper}') for paper in input_papers]
    logger.info('Parsed txt to documents')

    extract_and_store_graph(documents[3])

    # for i, d in tqdm(enumerate(documents), total=(len(documents) - 1)):
    #     print(d.metadata['title'])
    #     extract_and_store_graph(d)