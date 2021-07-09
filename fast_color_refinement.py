from graph import Graph, Vertex
from color_refinement import are_isomorphic
from graph_io import load_graph, write_dot


def give_start_labelling(graphs: list[Graph]) -> dict[int, list[Vertex]]:
    """Give every vertex an initial color label and return a dict from color to all vertices with that color."""
    degree_to_color = dict()
    color_classes = dict()

    for graph in graphs:
        for vertex in graph.vertices:
            if not hasattr(vertex, 'colornum'):
                if vertex.degree not in degree_to_color:
                    degree_to_color[vertex.degree] = len(color_classes)
                vertex.colornum = degree_to_color[vertex.degree]

            color_class = color_classes.get(vertex.colornum, [])
            color_class.append(vertex)
            color_classes[vertex.colornum] = color_class

    return color_classes


def old_refine(color_classes: dict[int, list[Vertex]], color: int,
               stack: list[int]):

    # Identify all neighbouring colours
    neighbours = set()
    for vertex in color_classes.get(color):
        for vertex2 in vertex.neighbours:
            neighbours.add(vertex2.colornum)

    changes = dict()

    # Detect changes for all neighbours based on the amount of neighbours with color color
    for neighbour in neighbours:
        vertices = color_classes.get(neighbour)
        new_colors = dict()

        # Split vertices based on number of neighbours with colour color
        for vertex in vertices:
            count = list(v.colornum for v in vertex.neighbours).count(color)
            result = new_colors.get(count, [])
            result.append(vertex)
            new_colors[count] = result

        # Add the changes to the changes dictionary
        if len(new_colors.keys()) > 1:
            changes[neighbour] = new_colors.values()

    # Apply all the changes
    for old_color, new_color_classes in changes.items():

        # Assign the vertices to their new colors
        for count, new_color_vertices in enumerate(list(new_color_classes)):
            if count > 0:
                new_color = len(color_classes.keys())
                for vertex in new_color_vertices:
                    vertex.colornum = new_color
            color_classes[new_color_vertices[0].colornum] = new_color_vertices

        # Add the colors to the queue
        add_to_queue = new_color_classes
        # If the original partition was stable leave the biggest partition out of the queue
        if old_color not in stack:
            add_to_queue = sorted(add_to_queue, key=lambda x: len(x), reverse=True)[1:]
        for new_color in add_to_queue:
            color = new_color[0].colornum
            if color not in stack:
                stack.append(color)


def fast_color_refinement(graphs: list[Graph]):
    """Alter the given list of graphs to have color labels reflecting color refinement."""

    # Start with pi = {F, Q\F} = {C0, C1}
    # For a DFA we would split 2 ways, but in general we can split more efficiently on degree.
    color_classes = give_start_labelling(graphs)

    # Maintain a queue (or stack) that will be used for refining operations, starting with [0].
    # The queue is guaranteed to work if all classes are included.
    add_to_queue = sorted(list(color_classes.values()), key=lambda x: len(x), reverse=True)
    stack = list(vertices[0].colornum for vertices in add_to_queue)[1:]

    # Refine the stack until it is empty
    while len(stack) > 0:
        color = stack[0]
        stack.pop(0)
        old_refine(color_classes, color, stack)


def do_fast_color_refinement_with_user_input():
    """
    Allows the user to do color refinement on a set of graphs of choice and make a dot file of it

    This testing function is stolen from Fabian's implementation since I only care about the logic.
    """
    graph_name = input(
        "Please enter the name of the graph file (leave empty for cref9vert_4_9.grl): "
    )
    if graph_name == "":
        graph_name = "cref9vert_4_9.grl"

    # Read the graph file.
    try:
        with open('graphs/color refinement/' + graph_name) as f:
            graphs = load_graph(f, read_list=True)
    except FileNotFoundError:
        print(
            f"Unable to open {graph_name}, make sure that it's located in the graphs directory!"
        )
        exit()

    # Ask the user if we should create a .dot file
    create_dot = input(
        "Should the refined graph be exported as .dot? (default: no) ")
    if 'y' in create_dot or 'Y' in create_dot:
        create_dot = True
    else:
        create_dot = False

    # Merges the graphs vertices into a disjoint union, refines the colors and checks if a graph iso-
    # morphism is found. Not all isomorphisms can be found! Only if a graph is distinct we can reliably check for
    # isomorphism .
    graphs = graphs[0]
    fast_color_refinement(graphs)

    graphs_copy = graphs[::]
    for g1 in graphs:
        graphs_copy.remove(g1)
        for g2 in graphs_copy:
            if are_isomorphic(g1, g2):
                print(f"Isomorphism found between:\n{g1}\nAND\n{g2}\n")

    # create a disjunct union of all the graphs
    graph = graphs[0]
    for g in graphs[1:]:
        graph = graph + g

    # TODO: At this moment the isomorphisms are simply printed to the screen. Maybe save them somewhere.

    if create_dot:
        # Write the color refined disjoint union to a .dot file, for visual checks and debugging purposes.
        file_name = 'graphs/dot_files/' + graph_name.replace(".grl", "") + "_.dot"
        with open(file_name, 'w') as g:
            write_dot(graph, g)


if __name__ == '__main__':
    do_fast_color_refinement_with_user_input()
