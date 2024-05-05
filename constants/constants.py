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
                         WHERE NOT (n)--()
                         RETURN COUNT(n) as isolated_nodes""",

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

    'adjacency_matrix': """MATCH (n) 
                           MATCH (m)
                           WHERE EXISTS ((n)-[]-(m))
                           RETURN n.id as node1_id, m.id as node2_id""",

    'nodes_names': """MATCH (n) 
                      WHERE EXISTS ((n)-[]-())
                      RETURN n.id as node_id""",
    'count_label_dis': """MATCH (n) 
                          RETURN labels(n) as label,  COUNT(*) as count
                          ORDER BY count DESC, label ASC""",

    'count_edge_dis': """MATCH ()-[r]->() 
                         RETURN type(r) as edge, COUNT(*) as count
                         ORDER BY count DESC, edge ASC"""

}
