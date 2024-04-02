import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

print(list(combinations([1, 2, 3, 4, 5, 6], 3)))

g1 = nx.Graph()
g1.add_nodes_from([1, 2, 3, 4])
g1.add_edges_from([(1, 2), (1, 2), (2, 1), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])

g2 = nx.Graph()
g2.add_nodes_from([1, 2, 3, 4])
g2.add_edges_from([(1, 2), (2, 3), (3, 4)])

g3 = nx.Graph()
g3.add_nodes_from([1, 2, 3, 4])
g3.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4)])

g4 = nx.Graph()
g4.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
g4.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)])

g5 = nx.Graph()
g5.add_nodes_from([1, 2, 3, 4, 5, 6])
g5.add_edges_from([(1, 2), (1, 3), (1, 4), (1, 6), (2, 3), (2, 4), (4, 5)])


def to_token(g, k=2):
    node_combinations = list(combinations(g.nodes, k))
    token = nx.Graph()
    token.add_nodes_from(node_combinations)

    for nodes1 in token.nodes:
        for nodes2 in token.nodes:
            if nodes1 != nodes2 and len(set(nodes1).intersection(nodes2)) == k - 1:
                diff = set(nodes1) ^ set(nodes2)
                if g.has_edge(diff.pop(), diff.pop()):
                    token.add_edge(nodes1, nodes2)

    print(len(list(token.edges)))
    print(list(token.edges))

    draw(token)

    return token


def draw(g):
    p = nx.spring_layout(g)
    nx.draw(g, p, with_labels=True, node_size=700, node_color='skyblue', font_size=12, font_weight='bold', width=2)
    plt.show()


# to_token(g1)
# to_token(g2)
# to_token(g3)
# to_token(g4)

# to_token(g1, 3)

t = to_token(g5, 3)


# '''2-token grafy'''
# def to_2token(g):
#     nodes = list(combinations(g.nodes, 2))
#     token = nx.Graph()
#     token.add_nodes_from(nodes)
#
#     print("token nodes: ", token.nodes)
#     print("g nodes: ", list(g.nodes))
#     print("g edges: ", list(g.edges))
#
#     '''funguje, ale skrátená verzia!!!'''
#     for x1, y1 in token.nodes:
#         for x2, y2 in token.nodes:
#             if (x1, y1) != (x2, y2):
#                 if ((x1 == x2 and g.has_edge(y1, y2)) or
#                         (y1 == y2 and g.has_edge(x1, x2)) or
#                         (x1 == y2 and g.has_edge(x2, y1)) or
#                         (y1 == x2 and g.has_edge(x1, y2))):
#
#                     print(f"{x1} {y1}, {x2} {y2}")
#                     token.add_edge((min(x1, y1), max(x1, y1)), (min(x2, y2), max(x2, y2)))
#
#     # '''funguje!!!'''
#     # for x1, y1 in token.nodes:
#     #     for x2, y2 in token.nodes:
#     #         if x1 != x2 or y1 != y2:
#     #
#     #             if x1 == x2:
#     #                 if (y1, y2) in g.edges:
#     #                     print(f"{x1} {y1}, {x2} {y2}")
#     #                     token.add_edge((min(x1, y1), max(x1, y1)), (min(x2, y2), max(x2, y2)))
#     #             if y1 == y2:
#     #                 if (x1, x2) in g.edges:
#     #                     print(f"{x1} {y1}, {x2} {y2}")
#     #                     token.add_edge((min(x1, y1), max(x1, y1)), (min(x2, y2), max(x2, y2)))
#     #             if x1 == y2:
#     #                 if (x2, y1) in g.edges:
#     #                     print(f"{x1} {y1}, {x2} {y2}")
#     #                     token.add_edge((min(x1, y1), max(x1, y1)), (min(x2, y2), max(x2, y2)))
#     #             if y1 == x2:
#     #                 if (x1, y2) in g.edges:
#     #                     print(f"{x1} {y1}, {x2} {y2}")
#     #                     token.add_edge((min(x1, y1), max(x1, y1)), (min(x2, y2), max(x2, y2)))
#
#     # '''funguje pre g2, nefunguje pre nič iné'''
#     # for x, y in token.nodes:
#     #
#     #     for node1 in g.nodes:
#     #         for node2 in g.nodes:
#     #             if (x, node1) in g.edges:
#     #                 if (node, y) in token.nodes:
#     #                     print(f"{x} {y}, {node} {y}")
#     #                     token.add_edge((min(x, y), max(x, y)), (min(node, y), max(node, y)))
#     #
#     #             if (y, node) in g.edges:
#     #                 if (x, node) in token.nodes:
#     #                     print(f"{x} {y}, {x} {node}")
#     #                     token.add_edge((min(x, y), max(x, y)), (min(x, node), max(x, node)))
#
#     # '''fungovalo pre g1 nefungovalo pre nič iné'''
#     # for edge in g.edges:
#     #
#     #     x = edge[0]
#     #     y = edge[1]
#     #
#     #     for node in g.nodes:
#     #
#     #         if (x, node) in g.edges and node != y:
#     #             token.add_edge((min(x, y), max(x, y)), (min(x, node), max(x, node)))
#     #         if (node, y) in g.edges and node != x:
#     #             token.add_edge((min(x, y), max(x, y)), (min(node, y), max(node, y)))
#
#     print(len(list(token.edges)))
#     print(list(token.edges))
#
#     p = nx.spring_layout(token)
#     nx.draw(token, p, with_labels=True, node_size=700, node_color='skyblue',font_size=12, font_weight='bold', width=2)
#     plt.show()
