import copy
import sys


def bfs_util(graph, source, destination):
    bfs_queue = []
    visited = [False for i in enumerate(graph)]
    parent = [None for i in enumerate(graph)]
    distance = [sys.maxsize for i in enumerate(graph)]
    visited[source] = True
    distance[source] = 0
    bfs_queue.append(source)
    while bfs_queue != []:
        current = bfs_queue.pop(0)
        for neighbour in graph[current]:
            if not visited[neighbour]:
                visited[neighbour] = True
                distance[neighbour] = distance[current] + 1
                parent[neighbour] = current
                bfs_queue.append(neighbour)
                if neighbour == destination:
                    return parent, distance[destination]
    return parent, distance[destination]


def shortest_path(graph, source, destination):
    parent, distance = bfs_util(graph, source, destination)
    return reversed(parent)


def shortest_distance(graph, source, destination):
    parent, distance = bfs_util(graph, source, destination)
    return distance


def contract_nodes(graph, node1, node2):
    new_node = max(graph.nodes)
    graph.nodes.append(new_node)
    for edge in graph.edges:
        if edge == [node1, node2] or edge == [node2, node1]:
            graph.edges.remove(edge)
        else:
            if node1 == edge[0]:
                edge[0] = new_node
            if node1 == edge[1]:
                edge[1] = new_node
            if node2 == edge[0]:
                edge[0] = new_node
            if node2 == edge[1]:
                edge[1] = new_node
    return graph


def add_edge_to_matching(matching, vertex1, vertex2):
    if (
        [vertex1, vertex2] in matching.edges
        or [vertex2, vertex1] in matching.edges
        or vertex1 in matching.nodes
        or vertex2 in matching.nodes
    ):
        return matching
    matching.edges.append([vertex1, vertex2])
    if vertex1 not in matching.nodes:
        matching.nodes.append(vertex1)
    if vertex2 not in matching.nodes:
        matching.nodes.append(vertex2)


def remove_edge_from_matching(matching, vertex1, vertex2):
    if [vertex1, vertex2] in matching.edges:
        matching.edges.remove([vertex1, vertex2])
    if [vertex2, vertex1] in matching.edges:
        matching.edges.remove([vertex2, vertex1])
    matching.nodes.remove(vertex1)
    matching.nodes.remove(vertex2)


class Forest:
    def __init__(self):
        self.tree_list = []

    def add_tree(self, tree):
        self.tree_list.append(tree)

    def get_tree_by_node(self, node):
        for index in enumerate(self.tree_list):
            if node in self.tree_list[index].nodes:
                return index

    def is_in_forest(self, node):
        for tree in self.tree_list:
            if node in tree.nodes:
                return True
        return False

    def tree(self, tree_index):
        return self.tree_list[tree_index]

    def get_root(self, node):
        for tree in self.tree_list:
            if node in tree.nodes:
                return tree.root
        return False


class Tree:
    def __init__(self, root):
        self.root = root
        self.nodes = []
        self.nodes.append(root)
        self.graph = {}
        self.graph[root] = None

    def add_edge(self, vertex1, vertex2):
        if vertex1 not in self.nodes:
            self.nodes.append(vertex1)
        if vertex2 not in self.nodes:
            self.nodes.append(vertex2)
        if vertex1 not in self.graph.keys():
            self.graph[vertex1] = []
        if vertex2 not in self.graph.keys():
            self.graph[vertex2] = []
        if vertex1 not in self.graph[vertex2]:
            self.graph[vertex2].append(vertex1)
        if vertex2 not in self.graph[vertex1]:
            self.graph[vertex1].append(vertex2)


class Matching:
    def __init__(self):
        self.edges = []
        self.nodes = []

    def get_edges(self, node):
        for edge in self.edges:
            if node in edge:
                return edge
        return []

    def has_edge(self, node1, node2):
        for _edge in self.edges:
            if [node1, node2] == _edge or [node2, node1] == _edge:
                return True
        return False


class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = []

    def has_edge(self, vertex1, vertex2):
        for edge in self.edges:
            if [vertex1, vertex2] == edge or [vertex2, vertex1] == edge:
                return True
        return False

    def get_edges(self, node):
        edge_list = []
        for edge in self.edges:
            if node in edge:
                edge_list.append(edge)
        return edge_list
