
from langchain_community.graphs.graph_document import (Node as BaseNode, Relationship as BaseRelationship)

from utils.debugger import logger
from database.cypher_queries import get_nodes
from database.init_database import Node, Relationship, Property
from chat.openai_parser import create_node_label_openai


def format_property_key(s: str) -> str:
    words = s.split()
    if not words:
        return s
    first_word = words[0].lower()
    capitalized_words = [word.capitalize() for word in words[1:]]
    return "".join([first_word] + capitalized_words)

def props_to_dict(props) -> dict:
    """Convert properties to a dictionary."""
    properties = {}
    if not props:
      return properties
    for p in props:
        properties[format_property_key(p.key)] = p.value
    return properties


def check_label(this_node_name: str, this_node_label: str, graph_node_label: str = None) -> str:
    if this_node_label == graph_node_label:
        return graph_node_label
    elif this_node_label == 'Node':
        return create_node_label_openai(this_node_name)
    else:
        return this_node_label


def add_node_history(this_node: BaseNode, paper_name:str) -> Node:
    # """Map the KnowledgeGraph Node to the base Node."""
    graph_nodes = get_nodes()

    if graph_nodes is {}:
        for node in graph_nodes:
            if node['name'].lower() == this_node.id.lower():
                this_node.type = check_label(this_node.id ,this_node.type, node['label'])
                this_node.properties.update(node.pop('label'))
                this_node.properties['reference'].append(paper_name)
    else:
        check_label(this_node.id, this_node.type)
        this_node.properties['name'] = this_node.id.title()
        this_node.properties['reference'] = [paper_name]

    return this_node


def map_to_base_node(node: Node) -> BaseNode:
    """Map the KnowledgeGraph Node to the base Node."""
    properties = props_to_dict(node.properties) if node.properties else {}

    properties["name"] = node.id.title()

    return BaseNode(
        id=node.id.title(), type=node.type.capitalize(), properties=properties
    )

def map_to_base_relationship(rel: Relationship) -> BaseRelationship:
    """Map the KnowledgeGraph Relationship to the base Relationship."""
    source = map_to_base_node(rel.source)
    target = map_to_base_node(rel.target)
    properties = props_to_dict(rel.properties) if rel.properties else {}
    return BaseRelationship(
        source=source, target=target, type=rel.type, properties=properties
    )
