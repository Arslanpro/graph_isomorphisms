import unittest
from basicpermutationgroup import permutation
from auto_morphisms import compute_order, is_member


class MyTestCase(unittest.TestCase):

    def test_is_member(self):
        h = [
            permutation(6, cycles=[[0, 1, 2], [4, 5]]),
            permutation(6, cycles=[[2, 3]])
        ]
        self.assertTrue(is_member(h, permutation(6, cycles=[[0, 2]])))

        g = [
            permutation(7, cycles=[[4, 5]]),
            permutation(7, cycles=[[1, 2]]),
            permutation(7, cycles=[[3, 6], [1, 4], [2, 5]])
        ]
        self.assertTrue(is_member(g, permutation(7, cycles=[[1, 2], [4, 5]])))

    def test_computer_order(self):
        h = [
            permutation(6, cycles=[[0, 1, 2], [4, 5]]),
            permutation(6, cycles=[[2, 3]])
        ]
        self.assertEqual(compute_order(h), 48)
        g = [
            permutation(6, cycles=[[1, 2]]),
            permutation(6, cycles=[[3, 4, 5]])
        ]
        self.assertEqual(compute_order(g), 6)
        i = [
            permutation(7, cycles=[[4, 5]]),
            permutation(7, cycles=[[1, 2]]),
            permutation(7, cycles=[[3, 6], [1, 4], [2, 5]])
        ]
        self.assertEqual(compute_order(i), 8)


if __name__ == '__main__':
    unittest.main()
