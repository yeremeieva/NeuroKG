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
                       )"""

}