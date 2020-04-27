import copy
from graph_utils import (
    Forest,
    Tree,
    add_edge_to_matching,
    remove_edge_from_matching,
    shortest_path,
    shortest_distance,
    contract_nodes,
)


def find_maximum_matching(graph, matching):
    augmenting_path = find_aug_path(graph, matching)
    if augmenting_path == []:
        return matching
    else:
        for index in enumerate(augmenting_path):
            if index % 2 == 0:
                add_edge_to_matching(
                    matching, augmenting_path[index], augmenting_path[index + 1]
                )
            if index % 2 == 1:
                remove_edge_from_matching(
                    matching, augmenting_path[index], augmenting_path[index + 1]
                )
        return find_maximum_matching(graph, matching)


def find_aug_path(graph, matching, blossoms=[]):
    forest = Forest()
    forest_nodes = []
    exposed_vertices = []
    path = []
    flag = False
    for i in enumerate(graph.nodes):
        flag = False
        for edge in matching:
            if i in (edge[0], edge[1]):
                flag = True
        if not flag:
            exposed_vertices.append(i)
    node_to_root = [None for i in exposed_vertices]
    for vertex in exposed_vertices:
        forest.add_tree(Tree(vertex))
        forest_nodes.append(vertex)
        node_to_root[vertex] = vertex
    unmarked_edges = []
    for vertex in graph.nodes:
        for edge in graph.get_edges(vertex):
            if not edge in matching:
                unmarked_edges.append(edge)
    for vertex in forest_nodes:
        v_tree_index = forest.get_tree_by_node(vertex)
        v_edges = graph.get_edges(vertex)
        for edge in v_edges:
            reverse_edge = [edge[1], edge[0]]
            if edge in unmarked_edges or reverse_edge in unmarked_edges:
                neighbour = edge[1]
                neighbour_in_forest = forest.is_in_forest(neighbour)
                if neighbour_in_forest == False:
                    forest.tree(v_tree_index).add_edge(edge)
                    neighbour_matching = matching.get_edges(neighbour)
                    forest.tree(v_tree_index).add_edge(neighbour_matching)
                    forest_nodes.append(neighbour_matching[1])
                else:
                    n_tree_index = forest.get_tree_by_node(neighbour)
                    if (
                        shortest_distance(
                            forest.tree(v_tree_index),
                            neighbour,
                            forest.get_root(neighbour),
                        )
                        % 2
                        == 0
                    ):
                        if n_tree_index != v_tree_index:
                            path_v = shortest_path(
                                forest.tree(v_tree_index),
                                forest.get_root(vertex),
                                vertex,
                            )
                            path_n = shortest_path(
                                forest.tree(n_tree_index),
                                neighbour,
                                forest.get_root(neighbour),
                            )
                            return path_v + path_n
                        else:
                            blossom = shortest_path(
                                forest.tree(v_tree_index), vertex, neighbour
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
                                        remove_edge = matching.get_edges(blossom[index])
                                        remove_edge_from_matching(
                                            contracted_matching,
                                            remove_edge[0],
                                            remove_edge[1],
                                        )
                            blossoms.append(neighbour)
                            aug_path = find_aug_path(
                                contracted_graph, contracted_matching, blossoms
                            )
                            blossom_vertex = blossoms.pop()
                            if blossom_vertex in aug_path:
                                left_stem = aug_path[0 : aug_path.index(blossom_vertex)]
                                right_stem = aug_path[
                                    aug_path.index(blossom_vertex) + 1 :
                                ]
                                lifted_blossom = []
                                count = 0
                                blossom_base = None
                                base_index = -1
                                extended_blossom = blossom + blossom[1]
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
                                                            reversed(based_blossom)
                                                        )[-count - 1 :]
                                                    else:
                                                        lifted_blossom = list(
                                                            reversed(based_blossom)
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
                                                            reversed(based_blossom)
                                                        )[:-count]
                                                count += 1
                                            return lifted_blossom + right_stem
                                else:
                                    if matching.has_edge(blossom_base, left_stem[-1]):
                                        if graph.has_edge(blossom_base, right_stem[0]):
                                            return (
                                                left_stem + [blossom_base] + right_stem
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
                                                            reversed(based_blossom)
                                                        )[:-count]
                                                count += 1
                                            return (
                                                left_stem + lifted_blossom + right_stem
                                            )
                                    else:
                                        if graph.has_edge(blossom_base, left_stem[-1]):
                                            return (
                                                left_stem + [blossom_base] + right_stem
                                            )
                                        else:
                                            count = 0
                                            while lifted_blossom == []:
                                                if graph.has_edge(
                                                    based_blossom[count], left_stem[-1]
                                                ):
                                                    if count % 2 == 0:
                                                        lifted_blossom = list(
                                                            reversed(based_blossom)
                                                        )[-count - 1 :]
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
    return path
