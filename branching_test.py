import os
import unittest
from time import time

from branching import count_isomorphism
from graph import Graph
from graph_io import load_graph


answers = {
    'torus24': {
        (0, 3): 96,
        (1, 2): 96
    },
    'torus72': {
        (0, 2): 288,
        (1, 5): 288,
        (3, 6): 288,
        (4, 7): 288
    },
    'torus144': {
        (0, 6): 576,
        (1, 7): 576,
        (2, 4): 576,
        (3, 10): 576,
        (5, 9): 1152,
        (8, 11): 576
    },
    'products72': {
        (0, 6): 288,
        (1, 5): 576,
        (2, 3): 576,
        (4, 7): 864
    },
    'products216': {
        (0, 6): 1728,
        (1, 7): 1728,
        (2, 9): 1728,
        (3, 8): 10368,
        (4, 5): 1728
    },
    'cographs1': {
        (0, 3): 5971968,
        (1, 2): 995328
    },
    'trees11': {
        (0, 3): 6,
        (1, 4): 1,
        (2, 5): 2
    },
    'trees36': {
        (0, 7): 2,
        (1, 4): 6,
        (2, 6): 2,
        (3, 5): 6
    },
    'trees90': {
        (0, 3): 6912,
        (1, 2): 20736
    },
    'modulesC': {
        (0, 7): 17915904,
        (1, 5): 17915904,
        (2, 4): 2488320,
        (3, 6): 2985984
    },
    'modulesD': {
        (0, 2): 24,
        (1, 3): 1,
        (4, 5): 24
    },
    'cubes3': {
        (0, 2): 48,
        (1, 3): 16
    },
    'cubes5': {
        (0, 1): 3840,
        (2, 3): 24
    },
    'cubes6': {
        (0, 1): 96,
        (2, 3): 46080
    },
    'cubes7': {
        (0, 3): 645120,
        (1, 2): 480
    },
    'cubes9': {
        (0, 1): 185794560,
        (2, 3): 20160
    },
    'bigtrees1': {
        (0, 2): 442368,
        (1, 3): 5308416
    },
    'bigtrees2': {
        (0, 3): 80244904034304,
        (1, 2): 160489808068608
    },
    'bigtrees3': {
        (0, 2): 2772351862699137701073289910157312,
        (1, 3): 462058643783189616845548318359552
    },
    'wheeljoin14': {
        (0, 1): 1600,
        (2, 3): 672,
        (4, 7): 1536,
        (5, 6): 720
    },
    'wheeljoin33': {
        (0, 4): 8257536,
        (1, 2): 7962624,
        (3, 5): 50577408,
        (6, 7): 1290240
    },
    'wheelstar12': {
        (0, 3): 1935360,
        (1, 2): 6718464
    },
    'wheelstar15': {
        (0, 7): 1703116800,
        (1, 4): 3009871872,
        (2, 3): 10642046976,
        (5, 6): 2890137600
    }
}


def get_files(partial_filename: str) -> list[str]:
    dir_content = os.listdir('../graphs/branching')
    files = []
    for file in dir_content:
        if partial_filename in file:
            files.append(file)
    return files


def get_instances(maximal_isomorphisms: int) -> list[str]:
    desired_filenames = [k for k in answers.keys()]
    for name in desired_filenames[::]:
        for tup in answers[name].values():
            if tup > maximal_isomorphisms and name in desired_filenames:
                desired_filenames.remove(name)
    return desired_filenames


class BranchingTest(unittest.TestCase):

    def test_instances_2000(self):
        """
        Only test instances with a maximum of 2000 isomorphisms.
        This test keeps track of the time spent, the nr of isomorphisms/second and if the answer is actually correct.
        """
        instances = get_instances(2000)
        for instance in instances:
            with open('graphs/branching/' + instance + '.grl') as f:
                print(f"\nTesting graphs instance {instance}.")
                graphs = load_graph(f, read_list=True)[0]

                start_time = time()
                for i in range(len(graphs)):
                    for j in range(len(graphs)):
                        if i < j:
                            start = time()
                            num = count_isomorphism(graphs[i] + Graph(False), graphs[j] + Graph(False))
                            end = time()
                            if num > 0:
                                print("Operation took {:.4f} seconds. On average {:.4f} isomorphisms/second"
                                      .format(end - start, num / (end - start)))
                            else:
                                print("Operation took {:.4f} seconds.".format(end - start))

                            instance_dict = answers[instance]
                            if (i, j) in instance_dict.keys():
                                self.assertEqual(instance_dict[(i, j)], num, f"For graphs {i} and {j}.")
                            else:
                                self.assertEqual(0, num, f"For graphs {i} and {j}")
                end_time = time()
                print(f"The entire graph instance {instance} took {end_time - start_time} seconds.")

if __name__ == '__main__':
    unittest.main()
