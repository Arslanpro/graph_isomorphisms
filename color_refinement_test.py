import unittest
import os
import time
from color_refinement import load_graph, merge_graphs, refine_colors


class MyTestCase(unittest.TestCase):

    # def test_something(self):
    #     self.assertEqual(True, False)

    def test_refinement_time(self):
        graph_files = os.listdir('graphs/color refinement/')
        for graph_file in graph_files:
            with open('graphs/color refinement/' + graph_file) as f:
                print(f"Test started for graph {f.name}")
                graphs = load_graph(f, read_list=True)

                start_time = time.time()
                graph = merge_graphs(graphs[0])
                end_time = time.time()
                run_time = "{:.4f}".format(end_time - start_time)
                print(f"Merging graphs took {run_time} seconds")

                start_time = time.time()
                graph = refine_colors(graph)
                end_time = time.time()
                run_time = "{:.4f}".format(end_time - start_time)
                print(f"Color refinement took {run_time} seconds\n")


if __name__ == '__main__':
    unittest.main()
