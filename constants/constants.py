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
                       RETURN degree"""
}