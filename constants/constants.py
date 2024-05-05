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

COMPLEX_QUERIES = {
    'edges5_table': """MATCH (n1)-[r1]-(n2)-[r2]-(n3)-[r3]-(n4)-[r4]-(n5)-[r5]-(n6)
                       RETURN n1.name, type(r2), n3.name, type(r3), n4.name, type(r4), n5.name, type(r5), n6.name 
                       LIMIT 5000""",
    'edges5_graph': """MATCH p=(n1)-[r*5]-(n2)
                       RETURN p 
                       LIMIT 50""",
    'brain_areas_graph': """MATCH p=(n:`Brain area`)--(k) 
                            RETURN p """,
    'path_between_nodes': """MATCH p=(n1 {name:'Neuroinflammation'})-[r*1..6]-(n2 {name:'Brain Metastases'})
                             RETURN p""",
    'brain_area_forward': """MATCH (n:`Brain area`)-[r]->(k)
                             RETURN n.name, type(r), k.name""",
    'brain_area_backward': """MATCH (k)-[r]->(n:`Brain area`)
                              RETURN k.name, type(r), n.name"""

}
