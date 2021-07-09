"""
This program combines all algorithms that have been written during the project weeks.
It is able to automatically recognize files based on their naming and takes the appropriate actions.
"""

from graph import Graph
from graph_io import load_graph
from branching import count_isomorphism, count_ismorphism_2
from auto_morphisms import count_automorphisms


def basic_GI(graphs: list[Graph]) -> None:
    """
    Figure out the equivalence classes between the graphs in the lists.
    :param graphs: A list with graphs
    """
    equivalence_classes = []
    for i in range(len(graphs)):
        added = False
        for equivalence_class in equivalence_classes:
            number_of_isomorphisms = count_ismorphism_2(graphs[equivalence_class[0]] + Graph(False), graphs[i] + Graph(False), [], [])
            if number_of_isomorphisms:
                equivalence_class.append(i)
                added = True
        if not added:
            equivalence_classes.append([i])

    print("Equivalence Classes:")
    for value in equivalence_classes:
        print(value)


def basic_GIAut(graphs: list[Graph]) -> None:
    """
    Calculates bot the equivalence classes as the number of automorphisms for each graph.
    :param graphs: A list with graphs
    """
    basic_GI(graphs)
    basic_Aut(graphs)


def basic_Aut(graphs: list[Graph]) -> None:
    """
    Calculates the number of automorphisms for each graph.
    :param graphs: A list with graphs
    """
    automorphisms = [0 for _ in range(len(graphs))]

    for i in range(len(graphs)):
        automorphisms[i] = count_isomorphism(graphs[i] + Graph(False), graphs[i] + Graph(False), [], [])

    print("Automorphisms:")
    for i, value in enumerate(automorphisms):
        print(f"{i}: {value}")


def bonus_Aut(graphs: list[Graph]) -> None:
    """
    Calculates the number of automorphisms for each graph.
    :param graphs: A list with graphs
    """
    automorphisms = [0 for _ in range(len(graphs))]

    for i, value in enumerate(graphs):
        automorphisms[i] = count_automorphisms(value)

    print("Automorphisms:")
    for i, value in enumerate(automorphisms):
        print(f"{i}: {value}")


if __name__ == '__main__':

    graph_name = input("Please enter the name of the graph file (leave empty for basicGI1.grl): ")
    if graph_name == "":
        graph_name = "basicGI1.grl"

    try:
        with open('graphs/delivery/' + graph_name) as f:
            graphs = load_graph(f, read_list=True)
    except FileNotFoundError:
        print(f"Unable to open {graph_name}, make sure that it is located in graphs/delivery!")
        exit()

    if "basicGIAut" in graph_name:
        basic_GIAut(graphs[0])
    elif "basicGI" in graph_name or "bonusGI" in graph_name:
        basic_GI(graphs[0])
    elif "basicAut" in graph_name:
        basic_Aut(graphs[0])
    elif "bonusAut" in graph_name:
        bonus_Aut(graphs[0])
    else:
        print(f"The file couldn't be recognized, please adhere to the naming scheme as denoted on Canvas!")