"""
This contains the definitions of the find_maximum_matching and find_aug_path functions.
"""
import copy
from typing import List
from graph_utils import (
    Graph,
    Forest,
    Tree,
    Matching,
    add_edge_to_matching,
    remove_edge_from_matching,
    shortest_path,
    shortest_distance,
    contract_nodes,
    aux_add_edge_to_matching,
)


def find_maximum_matching(graph: Graph, matching: Matching) -> List[int]:
    """
    Input:
        graph: An instance of the Graph class defined in graph_utils.py
        matching: An instance of the Matching class defined in graph_utils.py
    Description:
        This is a recursive function that calls find_aug_path(), that returns an augmenting path.
        The edges in the augmenting path are added to and removed from the matching alternatingly.
        The recursion teminates once there are no more aug paths that can be found.
    Output:
        The function returns a list of edges that form the maximum matching in the given graph
    Variables:
        augmenting_path: A list of nodes that make up an augmenting path for the given graph and matching
    """
    augmenting_path = find_aug_path(graph, matching)
    if augmenting_path == []:
        return matching
    for index in range(len(augmenting_path) - 1):
        if index % 2 == 0:
            add_edge_to_matching(
                matching, augmenting_path[index], augmenting_path[index + 1]
            )
        if index % 2 == 1:
            remove_edge_from_matching(
                matching, augmenting_path[index], augmenting_path[index + 1]
            )
    return find_maximum_matching(graph, matching)


def find_aug_path(graph: Graph, matching: List[int], blossoms: List[List[int]] = []):
    """
    Input:
        graph: An instance of the Graph class defined in graph_utils.py
        matching: An instance of the Matching class defined in graph_utils.py
        blossoms: A list of blossoms from previous calls to find_aug_path
    Description:
        This function finds augmenting paths, given a graph and a matching in the graph.
        The function is called recursively if there are any odd length cycles present in
        the augmenting path
    Output:
        The function returns a list of nodes that make an augmenting path, if there exists one, 
        given the graph and the corresponding matching. 
        Returns [] if there exists none        
    Variables:
        forest: An instance of the Forest class defined in graph_utils.py. 
                This is used to store the BFS trees that are formed when the unmatched vertices are explored
        forest_nodes: A list of nodes that are unmatched in the given graph
        flag: A temporary flag variable to check unmatched vertices
        unmarked_edges: A list of edges that are not in the matching
        blossom: A list of nodes that make an odd length cycle in the augmenting path
        contracted_graph: The graph resulting from contracting the nodes in the blossom
        contracted_matching: The matching resulting from contracting the nodes in the blossom,
                            which removes the matching among the edges in the blossom
        aug_path: A list of nodes that make up an augmenting path, involving a blossom. 
                This stores the return value of the recursive call
        lifted_blossom: A list of nodes representing the blossom after selecing the proper interior path to add to the matching
        based_blossom: A list of nodes representing the blossom whose base is in the beginning
        left_stem: A list of nodes representing the part of augmenting path that is present before the blossom in cases where a blossom is detected
        right_stem: A list of nodes representing the part of augmenting path that is present after the blossom in cases where a blossom is detected       
    """
    forest = Forest()
    forest_nodes = []
    flag = False
    for i in graph.nodes:
        flag = False
        for edge in matching.edges:
            if i in edge:
                flag = True
        if not flag:
            forest.add_tree(Tree(i))
            forest_nodes.append(i)
    unmarked_edges = []
    for vertex in graph.nodes:
        for edge in graph.get_edges(vertex):
            if not edge in matching.edges and edge not in unmarked_edges:
                unmarked_edges.append(edge)
    for vertex in forest_nodes:
        v_tree_index = forest.get_tree_by_node(vertex)
        v_edges = graph.get_edges(vertex)
        for edge in v_edges:
            reverse_edge = [edge[1], edge[0]]
            if edge in unmarked_edges or reverse_edge in unmarked_edges:
                if vertex == edge[0]:
                    neighbour = edge[1]
                else:
                    neighbour = edge[0]
                neighbour_in_forest = forest.is_in_forest(neighbour)
                if not neighbour_in_forest:
                    forest.tree(v_tree_index).add_edge(edge[0], edge[1])
                    neighbour_matching = matching.get_edges(neighbour)
                    forest.tree(v_tree_index).add_edge(
                        neighbour_matching[0], neighbour_matching[1]
                    )
                    neighbour_neighbour = (
                        neighbour_matching[0]
                        if neighbour_matching[0] != neighbour
                        else neighbour_matching[1]
                    )
                    forest_nodes.append(neighbour_neighbour)
                else:
                    n_tree_index = forest.get_tree_by_node(neighbour)
                    if (
                        shortest_distance(
                            forest.tree_graph(n_tree_index),
                            neighbour,
                            forest.get_root(neighbour),
                        )
                        % 2
                        == 0
                    ):
                        if n_tree_index != v_tree_index:
                            path_v = shortest_path(
                                forest.tree_graph(v_tree_index),
                                forest.get_root(vertex),
                                vertex,
                            )
                            path_n = shortest_path(
                                forest.tree_graph(n_tree_index),
                                neighbour,
                                forest.get_root(neighbour),
                            )
                            return path_v + path_n
                        else:
                            blossom = shortest_path(
                                forest.tree_graph(
                                    v_tree_index), vertex, neighbour
                            )
                            blossom.append(vertex)
                            contracted_graph = copy.deepcopy(graph)
                            contracted_matching = copy.deepcopy(matching)
                            for index in range(len(blossom) - 1):
                                if blossom[index] != neighbour:
                                    contracted_graph = contract_nodes(
                                        contracted_graph, blossom[index], neighbour
                                    )
                                    if blossom[index] in contracted_matching.nodes:
                                        remove_edge = matching.get_edges(
                                            blossom[index])
                                        remove_edge_from_matching(
                                            contracted_matching,
                                            remove_edge[0],
                                            remove_edge[1],
                                        )
                                        if not (
                                            remove_edge[0] in blossom
                                            and remove_edge[1] in blossom
                                        ):
                                            outside_blossom = (
                                                remove_edge[0]
                                                if remove_edge[0] != blossom[index]
                                                else remove_edge[1]
                                            )
                                            aux_add_edge_to_matching(
                                                contracted_matching,
                                                neighbour,
                                                outside_blossom,
                                            )
                            blossoms.append(neighbour)
                            aug_path = find_aug_path(
                                contracted_graph, contracted_matching, blossoms
                            )
                            blossom_vertex = blossoms.pop()
                            if blossom_vertex in aug_path:
                                left_stem = aug_path[0: aug_path.index(
                                    blossom_vertex)]
                                right_stem = aug_path[
                                    aug_path.index(blossom_vertex) + 1:
                                ]
                                lifted_blossom = []
                                count = 0
                                blossom_base = None
                                base_index = -1
                                extended_blossom = blossom + [blossom[1]]
                                while blossom_base is None and count < (
                                    len(blossom) - 1
                                ):
                                    if not matching.has_edge(
                                        blossom[count], blossom[count + 1]
                                    ):
                                        if not matching.has_edge(
                                            blossom[count + 1],
                                            extended_blossom[count + 2],
                                        ):
                                            blossom_base = blossom[count + 1]
                                            base_index = count + 1
                                        else:
                                            count += 2
                                    else:
                                        count += 1
                                if blossom[0] != blossom_base:
                                    based_blossom = []
                                    for i in range(base_index, len(blossom) - 1):
                                        based_blossom.append(blossom[i])
                                    for i in range(0, base_index):
                                        based_blossom.append(blossom[i])
                                    based_blossom.append(blossom_base)
                                else:
                                    based_blossom = blossom
                                if left_stem == [] or right_stem == []:
                                    if left_stem != []:
                                        if graph.has_edge(blossom_base, left_stem[-1]):
                                            return left_stem + [blossom_base]
                                        else:
                                            count = 1
                                            while lifted_blossom == []:
                                                if graph.has_edge(
                                                    based_blossom[count], left_stem[-1]
                                                ):
                                                    if count % 2 == 0:
                                                        lifted_blossom = list(
                                                            reversed(
                                                                based_blossom)
                                                        )[-count - 1:]
                                                    else:
                                                        lifted_blossom = list(
                                                            reversed(
                                                                based_blossom)
                                                        )[count:]
                                                count += 1
                                        return left_stem + lifted_blossom
                                    else:
                                        if graph.has_edge(blossom_base, right_stem[-1]):
                                            return [blossom_base] + right_stem
                                        else:
                                            count = 1
                                            while lifted_blossom == []:
                                                if graph.has_edge(
                                                    based_blossom[count], right_stem[0]
                                                ):
                                                    if count % 2 == 0:
                                                        lifted_blossom = based_blossom[
                                                            : count + 1
                                                        ]
                                                    else:
                                                        lifted_blossom = list(
                                                            reversed(
                                                                based_blossom)
                                                        )[:-count]
                                                count += 1
                                            return lifted_blossom + right_stem
                                else:
                                    if matching.has_edge(blossom_base, left_stem[-1]):
                                        if graph.has_edge(blossom_base, right_stem[0]):
                                            return (
                                                left_stem +
                                                [blossom_base] + right_stem
                                            )
                                        else:
                                            count = 0
                                            while lifted_blossom == []:
                                                if graph.has_edge(
                                                    based_blossom[count], right_stem[0]
                                                ):
                                                    if count % 2 == 0:
                                                        lifted_blossom = based_blossom[
                                                            : count + 1
                                                        ]
                                                    else:
                                                        lifted_blossom = list(
                                                            reversed(
                                                                based_blossom)
                                                        )[:-count]
                                                count += 1
                                            return (
                                                left_stem + lifted_blossom + right_stem
                                            )
                                    else:
                                        if graph.has_edge(blossom_base, left_stem[-1]):
                                            return (
                                                left_stem +
                                                [blossom_base] + right_stem
                                            )
                                        else:
                                            count = 0
                                            while lifted_blossom == []:
                                                if graph.has_edge(
                                                    based_blossom[count], left_stem[-1]
                                                ):
                                                    if count % 2 == 0:
                                                        lifted_blossom = list(
                                                            reversed(
                                                                based_blossom)
                                                        )[-count - 1:]
                                                    else:
                                                        lifted_blossom = based_blossom[
                                                            count:
                                                        ]
                                                count += 1
                                            return (
                                                left_stem + lifted_blossom + right_stem
                                            )
                            else:
                                return aug_path
    return []
