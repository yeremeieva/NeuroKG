from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
import os
from typing import List, Optional
from langchain.pydantic_v1 import Field, BaseModel
from langchain_community.graphs.graph_document import (Node as BaseNode, Relationship as BaseRelationship)

from utils.debugger import logger

def init_knowledge_base() -> Neo4jGraph:
    try:
        load_dotenv()
        url = os.getenv('DB_URL')
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASS')

        graph = Neo4jGraph(url=url, username=username, password=password)
        return graph

    except Exception as e:
        logger.exception(f'not successfully initialised graph, probably awful credentials of neo4j, exception "{e}"')


class Property(BaseModel):
  """A single property consisting of key and value"""
  key: str = Field(..., description="key")
  value: Optional[str] = Field(..., description="value")

class Node(BaseNode):
    properties: Optional[List[Property]] = Field(
        None, description="List of node properties")

class Relationship(BaseRelationship):
    properties: Optional[List[Property]] = Field(
        None, description="List of relationship properties"
    )

class KnowledgeGraph(BaseModel):
    """Generate a knowledge graph with entities and relationships."""
    nodes: List[Node] = Field(
        ..., description="List of nodes in the knowledge graph")
    rels: List[Relationship] = Field(
        ..., description="List of relationships in the knowledge graph")