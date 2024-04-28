QUERIES = {
    'diameter': """MATCH (n)
                      WITH collect(n) AS nodes
                      UNWIND nodes AS a
                      UNWIND nodes AS b
                      WITH a, b
                      WHERE id(a) < id(b)
                      MATCH path=shortestPath((a)-[*]-(b))
                      RETURN length(path) AS diameter
                      ORDER BY diameter
                      DESC LIMIT 1""",

    'count_nodes': """MATCH (n)
                      RETURN count(n) as count_nodes""",

    'count_edges': """MATCH ()-[r]->()
                      RETURN count(r) as count_edges""",

    'isolated_nodes': """MATCH (n) 
                         WHERE NOT EXISTS ((n)<-[]-()) RETURN count(n) as isolated_nodes""",

    'degree_nodes': """MATCH (n)
                       WITH COUNT{(n)-[]-()} as degree
                       WHERE  degree >= 1
                       RETURN degree""",

    'pagerank': """CALL gds.pageRank.stream('full_graph')
                   YIELD nodeId, score
                   RETURN gds.util.asNode(nodeId).name AS name, score
                   ORDER BY score DESC, name ASC""",

    'create_full_graph': """CALL gds.graph.project.cypher('full_graph',
                       'MATCH (n) RETURN id(n) AS id',
                       'MATCH (n)-[e]-(m) RETURN id(n) AS source, id(m) AS target'
                       )""",
    'adjacency_matrix': """MATCH (n1)
                           WITH collect(n1) as nodes1
                           MATCH (n2)
                           WITH nodes1, collect(n2) as nodes2
                           UNWIND nodes1 as node1
                           UNWIND nodes2 as node2
                           OPTIONAL MATCH (node1)-[]->(node2)
                           RETURN node1.id as node1_id, node2.id as node2_id""",
    'nodes_names': """MATCH (n) 
                      WHERE EXISTS ((n)-[]-())
                      RETURN n.id as node_id"""
}