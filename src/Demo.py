import random
import networkx as nx
import matplotlib.pyplot as plt
import blossom
from graph_utils import Graph,Matching


def giveinput(nodeCount,vertexCount):
    vertices = {}
    while len(vertices) < vertexCount:
        x = random.randint (1, nodeCount)
        y = random.randint (1, nodeCount)
        if x == y: continue
        #comment the following line if the graph is directed
        if y < x: x, y = y, x
        w = 0
        vertices [x, y] = w
    show_demo(vertices,nodeCount,vertexCount)



def show_demo(vertices,nodeCount,vertexCount):
    G=nx.Graph()
    nodes = []
    for i in range(1,nodeCount+1):
        nodes.append(i)
        G.add_node(i)
    edges= []
    for (x, y) in vertices.items ():
        edges.append([x[0],x[1]])
        edges.append([x[1],x[0]])
        e = (x[0],x[1])
        G.add_edge(x[0],x[1],color='black',weight=2)



    matching = Matching()

    graph = Graph()

    graph.nodes = nodes
    graph.edges = edges



    print("Nodes of graph: ")
    print(G.nodes())
    print("Edges of graph: ")
    print(G.edges())






    colors = [G[u][v]['color'] for u,v in G.edges()]
    weights = [G[u][v]['weight'] for u,v in G.edges()]





    # pos = nx.spring_layout(G)
    pos = nx.circular_layout(G)
    # pos = nx.random_layout(G)
    # pos = nx.kamada_kawai_layout(G)
    # pos = nx.spectral_layout(G)

    nx.draw(G, pos,with_labels = True, edges=edges, edge_color=colors, width=weights,node_color='blue')
    plt.savefig("input_graph.png") 
    plt.show() 






    print("Resultant Graph with Matched edges ")
    print("\n\n")
    print("=================================================================")
    print("\n")
    matching = (blossom.find_maximum_matching(graph,matching).edges)
    print(matching)



    print("\n\n")


    print("===================================================================")


    






    Gdash = nx.Graph()
    for i in range(1,nodeCount+1):
        Gdash.add_node(i)


    edges.clear()
    for (x, y) in vertices.items ():
        edges.append([x[0],x[1]])
        e = [x[0],x[1]]
        e_reverse = [x[1],x[0]]
        if(e in matching or e_reverse in matching):
            Gdash.add_edge(x[0],x[1],color='r',weight=3)
        else:
            Gdash.add_edge(x[0],x[1],color='black',weight=2)

    color = [Gdash[u][v]['color'] for u,v in G.edges()]
    weight = [Gdash[u][v]['weight'] for u,v in G.edges()]

    # pos = nx.spring_layout(Gdash)
    pos = nx.circular_layout(Gdash)
    # pos = nx.kamada_kawai_layout(Gdash)
    # pos = nx.spectral_layout(Gdash)


    nx.draw(Gdash, pos,with_labels = True, edges=edges,font_color='black',node_color='blue', edge_color=color, width=weight)
    plt.savefig("graphwith_matching.png") 
    plt.show() 


