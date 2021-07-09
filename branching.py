"""
This program implements the branching algorithm for individual color refinement.
"""

from graph import Graph, Vertex
from graph_io import load_graph
from color_refinement import color_refinement


def get_c(graphs: list[Graph]) -> tuple[int, int]:
    """
    FIXME: Complexity -> O(n) n = |V(g)| + |V(h)|

    Calculates c and while we're at it the next new color.
    :param graphs: The refined graphs
    :return: c and the next new color
    """
    colors = {}
    for graph in graphs:
        for v in graph.vertices:
            if v.colornum not in colors.keys():
                colors[v.colornum] = 1
            else:
                colors[v.colornum] += 1
                if colors[v.colornum] >= 4:
                    return v.colornum, len(colors.keys())


def count_isomorphism(g: Graph, h: Graph, d: list[Vertex] = [], i: list[Vertex] = []) -> int:
    """
    Counts the number of isomorphisms between the graphs g and h.
    :param g: The graph g
    :param h: The graph h
    :param d: A subset of the vertices from graph g
    :param i: A subset of the vertices from graph h
    :return: The number of isomorphisms between the graphs g and h.
    """
    # Refine the graphs
    refined = color_refinement([g, h])

    if not is_balanced(g, h):
        return 0
    if is_bijection(g, h):
        return 1

    # Determine the color class c, which should have at least 4 vertices.
    c, next_color = get_c([g, h])

    # Select a vertex from the first graph, variable x.
    # (See the pseudo-code in the second lecture of the project (Slide 12))
    # FIXME: O(n), n = |V(g)|
    for vertex in g:
        if vertex.colornum == c and vertex not in d:
            x = vertex
            break

    num = 0
    # FIXME: O(n), n = |V(h)|
    for vertex in h:
        if vertex.colornum == c and vertex not in i:
            # We have to create deep copies of all the graphs and lists,
            # otherwise they will be affected by the recursive calls.
            g1 = Graph(False) + g  # Adding an empty graph to the current graph is quicker than the deepcopy library ;)
            h1 = Graph(False) + h  # FIXME: O(n + m), n = |V(h)|, m = |E(h)|
            g1.vertices[g.vertices.index(x)].colornum = next_color
            h1.vertices[h.vertices.index(vertex)].colornum = next_color
            d1 = d[::]  # FIXME: O(n), n = |d|
            i1 = i[::]
            d1.append(x)
            i1.append(vertex)
            num = num + count_isomorphism(g1, h1, d1, i1)

    return num


def count_ismorphism_2(g, h, d, i):
    """
        Counts the number of isomorphisms between the graphs g and h.
        :param g: The graph g
        :param h: The graph h
        :param d: A subset of the vertices from graph g
        :param i: A subset of the vertices from graph h
        :return: The number of isomorphisms between the graphs g and h.
        """
    # Refine the graphs
    refined = color_refinement([g, h])

    if not is_balanced(g, h):
        return False
    if is_bijection(g, h):
        return True

    # Determine the color class c, which should have at least 4 vertices.
    c, next_color = get_c([g, h])

    # Select a vertex from the first graph, variable x.
    # (See the pseudo-code in the second lecture of the project (Slide 12))
    # FIXME: O(n), n = |V(g)|
    for vertex in g:
        if vertex.colornum == c and vertex not in d:
            x = vertex
            break

    num = 0
    # FIXME: O(n), n = |V(h)|
    for vertex in h:
        if vertex.colornum == c and vertex not in i:
            # We have to create deep copies of all the graphs and lists,
            # otherwise they will be affected by the recursive calls.
            g1 = Graph(False) + g  # Adding an empty graph to the current graph is quicker than the deepcopy library ;)
            h1 = Graph(False) + h  # FIXME: O(n + m), n = |V(h)|, m = |E(h)|
            g1.vertices[g.vertices.index(x)].colornum = next_color
            h1.vertices[h.vertices.index(vertex)].colornum = next_color
            d1 = d[::]  # FIXME: O(n), n = |d|
            i1 = i[::]
            d1.append(x)
            i1.append(vertex)
            if count_ismorphism_2(g1, h1, d1, i1):
                return True
            # num = num + count_isomorphism(g1, h1, d1, i1)

    # return num


def is_balanced(g: Graph, h: Graph):
    """
    FIXME: Complexity -> 2*2n -> O(n) n = |V(g)| = |V(h)|
    Instead of a sorted list we now generate a set, which is faster. But it does not keep track of the number of
    vertices within a color group. This might cause issues in next iterations. But for now all tests pass!

    Check if the graphs are balanced.
    :param g: The first graph
    :param h: The second graph
    :return: True if both graphs have the same colors
    """
    return set(v.colornum for v in g.vertices) == set(v.colornum for v in h.vertices)


def is_bijection(g: Graph, h: Graph):
    """
    FIXME: Complexity -> O(n)

    Check if the graphs are a bijection.
    :param g: The first graph
    :param h: The second graph
    :return: True if each graph has an unique color for each vertex.
    """
    return len(set(v.colornum for v in g.vertices)) == len(g.vertices) and len(set(v.colornum for v in h.vertices)) == len(h.vertices)


if __name__ == '__main__':

    graph_name = input("Please enter the name of the graph file (leave empty for cubes3.grl): ")
    if graph_name == "":
        graph_name = "cubes3.grl"

    try:
        with open('graphs/branching/' + graph_name) as f:
            graphs = load_graph(f, read_list=True)
    except FileNotFoundError:
        print(f"Unable to open {graph_name}, make sure that it is located in graphs/branching!")
        exit()

    for i in range(len(graphs[0])):
        for j in range(len(graphs[0])):
            if i < j:
                number = count_isomorphism(graphs[0][i] + Graph(False), graphs[0][j] + Graph(False))
                if number > 0:
                    print(f"Found {number} isomorphisms between graphs {i} and {j}\n")
