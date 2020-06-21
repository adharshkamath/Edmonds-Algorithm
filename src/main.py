from blossom import find_maximum_matching
from demo import giveinput, show_demo


def run():
    type = int(
        input(" Enter your option \n 1. For custom input \n 2. For random input \n")
    )
    vertices = {}
    if type == 1:
        num_edge = int(input("Enter the number of the edges in the graph\n"))
        num_node = int(input("Enter the number of the nodes in the graph\n"))
        for _ in range(num_edge):
            x, y = input("Enter the two vertices in each line: \n").split()
            x = int(x)
            y = int(y)
            vertices[x, y] = 0
            if x > num_node or y > num_node:
                print("wrong input try again")
                exit(0)
        show_demo(vertices, num_node, num_edge)
    else:
        num_edge = int(input("Enter the number of the edges in the graph\n"))
        num_node = int(input("Enter the number of the nodes in the graph\n"))
        valid = num_node * (num_node - 1) / 2
        if num_edge > valid:
            print("wrong input try again!!")
        else:
            giveinput(num_node, num_edge)


run()
