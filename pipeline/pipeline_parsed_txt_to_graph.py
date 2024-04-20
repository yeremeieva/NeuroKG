from langchain.docstore.document import Document
from langchain_community.graphs.graph_document import GraphDocument
from tqdm import tqdm
import time

from database.neo4j_database import map_to_base_node, map_to_base_relationship, add_node_history
from database.init_database import init_knowledge_base
from chat.openai_parser import prompt_to_create_knowledge_openai
from utils.reader import list_files, txt_to_doc
from utils.debugger import logger


def extract_graph(document: Document) -> GraphDocument:
    extract_chain = prompt_to_create_knowledge_openai()
    data = extract_chain.invoke(document.page_content)['function']

    nodes = [map_to_base_node(node) for node in data.nodes]
    rels = [map_to_base_relationship(rel) for rel in data.rels]

    for node in nodes:
        add_node_history(node)

    for node in nodes:
        for rel in rels:
            if node.id == rel.source.id:
                rel.source = node
            elif node.id == rel.target.id:
                rel.target = node

    graph_document = GraphDocument(
      nodes= nodes,
      relationships = rels,
      source = document)

    return graph_document

def store_graph(graph_document: GraphDocument):
    knowledge_base = init_knowledge_base()
    knowledge_base.add_graph_documents([graph_document])

def compare_graphs(graph_documents: list[GraphDocument]) -> GraphDocument:
    rel_to_nodes = []

    for graph_document in graph_documents:
        rel_to_nodes.append(abs(len(graph_document.nodes) - len(graph_document.relationships)))

    graph1 = graph_documents[rel_to_nodes.index(min(rel_to_nodes))]
    rel_to_nodes.pop(rel_to_nodes.index(min(rel_to_nodes)))
    graph2 = graph_documents[rel_to_nodes.index(min(rel_to_nodes))]

    if len(graph2.nodes) > len(graph1.nodes) and min(rel_to_nodes) <= 5:
        return graph2
    else:
        return graph1


def loop_over_documents(inner_documents:  list[Document]):
    for i, d in tqdm(enumerate(inner_documents), total=len(inner_documents)):
        try:
            graphs = []
            for _ in range(0, 2):
                graph = extract_graph(d)
                graphs.append(graph)

            best_graph = compare_graphs(graphs)
            store_graph(best_graph)
        except Exception as e:
            logger.exception(f'not successfully add the graph to KB, exception "{e}"')

if __name__ == '__main__':
    start_time = time.time()
    model = 'openai'
    input_papers = list_files(f'./data/{model}_txt_parsed_papers', ending='.txt')
    documents = [txt_to_doc(f'./data/{model}_txt_parsed_papers/{paper}') for paper in input_papers]
    logger.info('Good News!!!! Parsed txt to documents')

    loop_over_documents(documents)

    logger.info('Exciting News!!!! All papers were written to the graph!!!!!!!!!')

    end_time = time.time()
    time = end_time - start_time
    print(f"Time taken: {time/60:.2f} minutes")