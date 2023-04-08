import unittest

import numpy as np

from Graphics import Walls


def tile_matrix_4_x_3():
    return np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])


class MyTestCase(unittest.TestCase):

    def test_create_top_wall_matrix(self):
        wall_matrix = Walls.create_wall_matrix(tile_matrix_4_x_3(), 'top', 2, 1)

        expected = np.array([
            [1, 1, 1],
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0]])
        self.assertTrue(np.array_equal(expected, wall_matrix))

    def test_create_bottom_wall_matrix(self):
        wall_matrix = Walls.create_wall_matrix(tile_matrix_4_x_3(), 'bottom', 2, 1)

        expected = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 1, 0],
            [1, 1, 1]])
        self.assertTrue(np.array_equal(expected, wall_matrix))

    def test_create_left_wall_matrix(self):
        wall_matrix = Walls.create_wall_matrix(tile_matrix_4_x_3(), 'left', 2, 1)

        expected = np.array([
            [1, 0, 0],
            [1, 0, 1],
            [1, 0, 1],
            [1, 0, 0]])
        self.assertTrue(np.array_equal(expected, wall_matrix))

    def test_create_right_wall_matrix(self):
        wall_matrix = Walls.create_wall_matrix(tile_matrix_4_x_3(), 'right', 2, 1)

        expected = np.array([
            [0, 0, 1],
            [1, 0, 1],
            [1, 0, 1],
            [0, 0, 1]])
        self.assertTrue(np.array_equal(expected, wall_matrix))


if __name__ == '__main__':
    unittest.main()
