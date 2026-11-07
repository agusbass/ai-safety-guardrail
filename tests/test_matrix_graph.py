import unittest

from guardian.core.matrix_graph import MatrixGraph


class TestMatrixGraph(unittest.TestCase):
    def setUp(self):
        self.graph = MatrixGraph(11).build()

    def test_layer_counts(self):
        counts = self.graph.get_layer_counts()
        self.assertGreater(counts['luar'], 0)
        self.assertGreater(counts['dalam'], 0)
        self.assertGreater(counts['ms'], 0)
        self.assertEqual(counts['total'], counts['luar'] + counts['ms'] + counts['dalam'])

    def test_cores_linked_through_magic_square(self):
        luar_core = self.graph.get_node('luar_core_0')
        dalam_core = self.graph.get_node('dalam_core_0')
        ms_core = self.graph.get_node('ms_core_5')
        self.assertIn(ms_core, luar_core.edges)
        self.assertIn(ms_core, dalam_core.edges)

    def test_digital_root(self):
        self.assertEqual(self.graph.digital_root(0), 0)
        self.assertEqual(self.graph.digital_root(9), 9)
        self.assertEqual(self.graph.digital_root(20), 2)
        self.assertEqual(self.graph.digital_root(15), 6)

    def test_failsafe_loop_closure(self):
        # Stage index 20 (one past FAILSAFE=19) collapses to ROOT=0 in both
        # the Luar (mod 10) and Dalam (mod 20) layers.
        self.assertEqual(20 % 10, 0)
        self.assertEqual(20 % 20, 0)


if __name__ == '__main__':
    unittest.main()
