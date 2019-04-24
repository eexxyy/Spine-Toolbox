######################################################################################################################
# Copyright (C) 2017 - 2018 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Unit tests for DirectedGraphHandler class.

:author: P. Savolainen (VTT)
:date:   18.4.2019
"""

import unittest
from unittest import mock
import logging
import sys
from PySide2.QtWidgets import QApplication, QWidget
import networkx as nx
from ui_main import ToolboxUI
from project import SpineToolboxProject
from executioner import DirectedGraphHandler
from test.mock_helpers import MockQWidget, qsettings_value_side_effect


class TestDirectedGraphHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before any tests in this class."""
        try:
            cls.app = QApplication().processEvents()
        except RuntimeError:
            pass
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    def setUp(self):
        """Runs before each test. Makes an instance of ToolboxUI class.
        We want the ToolboxUI to start with the default settings and without a project
        """
        with mock.patch("ui_main.JuliaREPLWidget") as mock_julia_repl, \
                mock.patch("ui_main.PythonReplWidget") as mock_python_repl, \
                mock.patch("project.create_dir") as mock_create_dir, \
                mock.patch("ui_main.ToolboxUI.save_project") as mock_save_project, \
                mock.patch("ui_main.QSettings.value") as mock_qsettings_value:
            # Replace Julia REPL Widget with a QWidget so that the DeprecationWarning from qtconsole is not printed
            mock_julia_repl.return_value = QWidget()
            mock_python_repl.return_value = MockQWidget()
            mock_qsettings_value.side_effect = qsettings_value_side_effect
            self.toolbox = ToolboxUI()
            self.toolbox.create_project("UnitTest Project", "")
            self.dag_handler = DirectedGraphHandler(self.toolbox)

    def tearDown(self):
        """Runs after each test. Use this to free resources after a test if needed."""
        self.toolbox.deleteLater()
        self.toolbox = None
        self.dag_handler = None

    def test_project_is_open(self):
        """Test that project is open and that it has no project items."""
        self.assertIsInstance(self.toolbox.project(), SpineToolboxProject)
        n = self.toolbox.project_item_model.n_items()
        self.assertTrue(n == 0)

    def test_dags(self):
        """Test that dag_handler has been created and dags() method returns an empty list."""
        d = self.dag_handler.dags()
        self.assertTrue(len(d) == 0)

    def test_add_dag_node(self):
        """Test creating a graph with one node."""
        self.dag_handler.add_dag_node("a")
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        g = self.dag_handler.dags()[0]
        self.assertTrue(g.has_node("a"))

    def test_add_graph_edge1(self):
        """Test adding an edge when src and dst nodes are in different graphs.
        Graph 1: Nodes: [a, b]. Edges: [a->b]
        Graph 2: Nodes: [c, d]. Edges: [c->d]
        Add edge: b->c
        Result graph: Nodes: [a, b, c, d]. Edges: [a->b, b->c, c->d]
        """
        d = nx.DiGraph()
        h = nx.DiGraph()
        d.add_edges_from([("a", "b")])
        h.add_edges_from([("c", "d")])
        self.dag_handler.add_dag(d)
        self.dag_handler.add_dag(h)
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        self.dag_handler.add_graph_edge("b", "c")
        # Now, there should only be one graph with nodes [a,b,c,d] and edges a->b, b->c, c->d
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        g = self.dag_handler.dags()[0]
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(g.nodes()), 4)
        self.assertEqual(len(g.edges()), 3)
        self.assertTrue(g.has_node("a"))
        self.assertTrue(g.has_node("b"))
        self.assertTrue(g.has_node("c"))
        self.assertTrue(g.has_node("d"))
        self.assertTrue(g.has_edge("a", "b"))
        self.assertTrue(g.has_edge("b", "c"))
        self.assertTrue(g.has_edge("c", "d"))

    def test_add_graph_edge2(self):
        """Test adding an edge when src and dst nodes are in the same graph.
        Graph 1: Nodes: [a, b, c]. Edges: [a->b, b->c]
        Add edge: a->c
        Result graph: Nodes: [a, b, c]. Edges: [a->b, b->c, a->c]
        """
        d = nx.DiGraph()
        d.add_edges_from([("a", "b"), ("b", "c")])
        self.dag_handler.add_dag(d)
        # Check that the graph was created successfully
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        self.assertEqual(len(d.nodes()), 3)  # a, b, c
        self.assertEqual(len(d.edges()), 2)  # a->b, b->c
        self.dag_handler.add_graph_edge("a", "c")
        # Now, there should only be one graph with nodes [a,b,c] and edges a->b, b->c, a->c
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        g = self.dag_handler.dags()[0]
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(g.nodes()), 3)
        self.assertEqual(len(g.edges()), 3)
        self.assertTrue(g.has_node("a"))
        self.assertTrue(g.has_node("b"))
        self.assertTrue(g.has_node("c"))
        self.assertTrue(g.has_edge("a", "b"))
        self.assertTrue(g.has_edge("b", "c"))
        self.assertTrue(g.has_edge("a", "c"))

    def test_add_graph_edge3(self):
        """Test adding an edge when src and dst nodes are in different graphs.
        Graph 1: Nodes: [a]. Edges: []
        Graph 2: Nodes: [b, c]. Edges: [b->c]
        Add edge: a->c
        Result graph: Nodes: [a, b, c]. Edges: [b->c, a->c]
        """
        d = nx.DiGraph()
        h = nx.DiGraph()
        d.add_node("a")
        h.add_edges_from([("b", "c")])
        self.dag_handler.add_dag(d)
        self.dag_handler.add_dag(h)
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        self.dag_handler.add_graph_edge("a", "c")
        # Now, there should only be one graph with nodes [a,b,c] and edges b->c, a->c
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        g = self.dag_handler.dags()[0]
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(g.nodes()), 3)
        self.assertEqual(len(g.edges()), 2)
        self.assertTrue(g.has_node("a"))
        self.assertTrue(g.has_node("b"))
        self.assertTrue(g.has_node("c"))
        self.assertTrue(g.has_edge("b", "c"))
        self.assertTrue(g.has_edge("a", "c"))

    def test_add_graph_edge4(self):
        """Test adding an edge when src and dst nodes are in different graphs.
        Graph 1: Nodes: [a, b]. Edges: [a->b]
        Graph 2: Nodes: [c]. Edges: []
        Add edge: a->c
        Result graph: Nodes: [a, b, c]. Edges: [a->b, a->c]
        """
        d = nx.DiGraph()
        h = nx.DiGraph()
        d.add_edges_from([("a", "b")])
        h.add_node("c")
        self.dag_handler.add_dag(d)
        self.dag_handler.add_dag(h)
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        self.dag_handler.add_graph_edge("a", "c")
        # Now, there should only be one graph with nodes [a,b,c] and edges a->b, a->c
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        g = self.dag_handler.dags()[0]
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(g.nodes()), 3)
        self.assertEqual(len(g.edges()), 2)
        self.assertTrue(g.has_node("a"))
        self.assertTrue(g.has_node("b"))
        self.assertTrue(g.has_node("c"))
        self.assertTrue(g.has_edge("a", "b"))
        self.assertTrue(g.has_edge("a", "c"))

    def test_add_graph_edge5(self):
        """Test adding an edge when src and dst nodes are in different graphs.
        Graph 1: Nodes: [a]. Edges: []
        Graph 2: Nodes: [b]. Edges: []
        Add edge: a->b
        Result graph: Nodes: [a, b]. Edges: [a->b]
        """
        d = nx.DiGraph()
        h = nx.DiGraph()
        d.add_node("a")
        h.add_node("b")
        self.dag_handler.add_dag(d)
        self.dag_handler.add_dag(h)
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        self.dag_handler.add_graph_edge("a", "b")
        # Now, there should only be one graph with nodes [a,b,c] and edges a->b, a->c
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        g = self.dag_handler.dags()[0]
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(g.nodes()), 2)
        self.assertEqual(len(g.edges()), 1)
        self.assertTrue(g.has_node("a"))
        self.assertTrue(g.has_node("b"))
        self.assertTrue(g.has_edge("a", "b"))

    def test_add_graph_edge6(self):
        """Test adding a feedback edge, i.e. src and dst nodes are the same.
        Graph 1: Nodes: [a]. Edges: []
        Add edge: a->a
        Result graph: Nodes: [a]. Edges: []
        """
        d = nx.DiGraph()
        d.add_node("a")
        self.dag_handler.add_dag(d)
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        self.dag_handler.add_graph_edge("a", "a")
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        g = self.dag_handler.dags()[0]
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(g.nodes()), 1)
        self.assertEqual(len(g.edges()), 1)
        self.assertTrue(g.has_node("a"))
        self.assertTrue(g.has_edge("a", "a"))

    def test_add_graph_edge7(self):
        """Test adding more feedback loops to more complex graphs.
        Graph 1: Nodes: [a, b, c]. Edges: [a->b, b->c]
        Graph 2: Nodes: [d, e, f]. Edges: [d->f, e->f]
        Add edges: a->a, b->b, c->c, d->d, e->e, f->f
        Result graph 1: Nodes: [a, b, c]. Edges: [a->b, b->c, a->a, b->b, c->c]
        Result graph 2: Nodes: [d, e, f]. Edges: [d->f, e->f, d->d, e->e, f->f]
        """
        d = nx.DiGraph()
        h = nx.DiGraph()
        d.add_edges_from([("a", "b"), ("b", "c")])
        h.add_edges_from([("d", "f"), ("e", "f")])
        self.dag_handler.add_dag(d)
        self.dag_handler.add_dag(h)
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        self.dag_handler.add_graph_edge("a", "a")
        self.dag_handler.add_graph_edge("b", "b")
        self.dag_handler.add_graph_edge("c", "c")
        self.dag_handler.add_graph_edge("d", "d")
        self.dag_handler.add_graph_edge("e", "e")
        self.dag_handler.add_graph_edge("f", "f")
        # There should still be two graphs
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        result_d = self.dag_handler.dag_with_node("a")
        result_h = self.dag_handler.dag_with_node("d")
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(result_d.nodes()), 3)
        self.assertEqual(len(result_d.edges()), 5)
        self.assertTrue(result_d.has_node("a"))
        self.assertTrue(result_d.has_node("b"))
        self.assertTrue(result_d.has_node("c"))
        self.assertTrue(result_d.has_edge("a", "b"))
        self.assertTrue(result_d.has_edge("b", "c"))
        self.assertTrue(result_d.has_edge("a", "a"))
        self.assertTrue(result_d.has_edge("b", "b"))
        self.assertTrue(result_d.has_edge("c", "c"))
        self.assertEqual(len(result_h.nodes()), 3)
        self.assertEqual(len(result_h.edges()), 5)
        self.assertTrue(result_h.has_node("d"))
        self.assertTrue(result_h.has_node("e"))
        self.assertTrue(result_h.has_node("f"))
        self.assertTrue(result_h.has_edge("d", "f"))
        self.assertTrue(result_h.has_edge("e", "f"))
        self.assertTrue(result_h.has_edge("d", "d"))
        self.assertTrue(result_h.has_edge("e", "e"))
        self.assertTrue(result_h.has_edge("f", "f"))

    def test_remove_graph_edge1(self):
        """Test removing an edge from a graph. Splits the graph
        into two separate graphs if the nodes are not connected
        after removing the edge.
        Graph 1: Nodes: [a, b]. Edges: [a->b]
        Remove edge: a->b
        Result graph 1: Nodes: [a]. Edges: []
        Result graph 2: Nodes: [b]. Edges: []
        """
        d = nx.DiGraph()
        d.add_edges_from([("a", "b")])
        self.dag_handler.add_dag(d)
        # Check that the graph was created successfully
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        d = self.dag_handler.dags()[0]
        self.assertEqual(len(d.nodes()), 2)  # a, b
        self.assertEqual(len(d.edges()), 1)  # a->b
        self.assertTrue(d.has_edge("a", "b"))
        # Now remove the edge
        self.dag_handler.remove_graph_edge("a", "b")
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        result_d = self.dag_handler.dag_with_node("a")
        result_h = self.dag_handler.dag_with_node("b")
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(result_d.nodes()), 1)
        self.assertEqual(len(result_d.edges()), 0)
        self.assertTrue(result_d.has_node("a"))
        self.assertEqual(len(result_h.nodes()), 1)
        self.assertEqual(len(result_h.edges()), 0)
        self.assertTrue(result_h.has_node("b"))

    def test_remove_graph_edge2(self):
        """Test removing an edge from a graph. Splits the graph
        into two separate graphs if the nodes are not connected
        after removing the edge.
        Graph 1: Nodes: [a, b, c]. Edges: [a->b->c]
        Remove edge: a->b
        Result graph 1: Nodes: [a]. Edges: []
        Result graph 2: Nodes: [b, c]. Edges: [b->c]
        """
        d = nx.DiGraph()
        d.add_edges_from([("a", "b"), ("b", "c")])
        self.dag_handler.add_dag(d)
        # Check that the graph was created successfully
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        d = self.dag_handler.dags()[0]
        self.assertEqual(len(d.nodes()), 3)  # a, b, c
        self.assertEqual(len(d.edges()), 2)  # a->b, b->c
        self.assertTrue(d.has_edge("a", "b"))
        self.assertTrue(d.has_edge("b", "c"))
        # Now remove the edge
        self.dag_handler.remove_graph_edge("a", "b")
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        result_d = self.dag_handler.dag_with_node("a")
        result_h = self.dag_handler.dag_with_node("b")
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(result_d.nodes()), 1)
        self.assertEqual(len(result_d.edges()), 0)
        self.assertTrue(result_d.has_node("a"))
        self.assertEqual(len(result_h.nodes()), 2)
        self.assertEqual(len(result_h.edges()), 1)
        self.assertTrue(result_h.has_node("b"))
        self.assertTrue(result_h.has_node("c"))
        self.assertTrue(result_h.has_edge("b", "c"))

    def test_remove_graph_edge3(self):
        """Test removing an edge from a graph. Splits the graph
        into two separate graphs if the nodes are not connected
        after removing the edge.
        Graph 1: Nodes: [a, b, c]. Edges: [a->b->c]
        Remove edge: b->c
        Result graph 1: Nodes: [a, b]. Edges: [a->b]
        Result graph 2: Nodes: [c]. Edges: []
        """
        d = nx.DiGraph()
        d.add_edges_from([("a", "b"), ("b", "c")])
        self.dag_handler.add_dag(d)
        # Check that the graph was created successfully
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        d = self.dag_handler.dags()[0]
        self.assertEqual(len(d.nodes()), 3)  # a, b, c
        self.assertEqual(len(d.edges()), 2)  # a->b, b->c
        self.assertTrue(d.has_edge("a", "b"))
        self.assertTrue(d.has_edge("b", "c"))
        # Now remove the edge
        self.dag_handler.remove_graph_edge("b", "c")
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        result_d = self.dag_handler.dag_with_node("a")
        result_h = self.dag_handler.dag_with_node("c")
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(result_d.nodes()), 2)
        self.assertEqual(len(result_d.edges()), 1)
        self.assertTrue(result_d.has_node("a"))
        self.assertTrue(result_d.has_node("b"))
        self.assertTrue(result_d.has_edge("a", "b"))
        self.assertEqual(len(result_h.nodes()), 1)
        self.assertEqual(len(result_h.edges()), 0)
        self.assertTrue(result_h.has_node("c"))

    def test_remove_graph_edge4(self):
        """Test removing an edge from a graph. Splits the graph
        into two separate graphs if the nodes are not connected
        after removing the edge.
        Graph 1: Nodes: [a, b, c, d]. Edges: [a->b->c->d]
        Remove edge: b->c
        Result graph 1: Nodes: [a, b]. Edges: [a->b]
        Result graph 2: Nodes: [c, d]. Edges: [c->d]
        """
        d = nx.DiGraph()
        d.add_edges_from([("a", "b"), ("b", "c"), ("c", "d")])
        self.dag_handler.add_dag(d)
        # Check that the graph was created successfully
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        d = self.dag_handler.dags()[0]
        self.assertEqual(len(d.nodes()), 4)  # a, b, c
        self.assertEqual(len(d.edges()), 3)  # a->b, b->c
        self.assertTrue(d.has_edge("a", "b"))
        self.assertTrue(d.has_edge("b", "c"))
        self.assertTrue(d.has_edge("c", "d"))
        # Now remove the edge
        self.dag_handler.remove_graph_edge("b", "c")
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        result_d = self.dag_handler.dag_with_node("a")
        result_h = self.dag_handler.dag_with_node("c")
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(result_d.nodes()), 2)
        self.assertEqual(len(result_d.edges()), 1)
        self.assertTrue(result_d.has_node("a"))
        self.assertTrue(result_d.has_node("b"))
        self.assertTrue(result_d.has_edge("a", "b"))
        self.assertEqual(len(result_h.nodes()), 2)
        self.assertEqual(len(result_h.edges()), 1)
        self.assertTrue(result_h.has_node("c"))
        self.assertTrue(result_h.has_node("d"))
        self.assertTrue(result_h.has_edge("c", "d"))

    def test_remove_graph_edge5(self):
        """Test removing an edge from a graph. Splits the graph
        into two separate graphs if the nodes are not connected
        after removing the edge.
        Graph 1: Nodes: [a, b, c, d, e]. Edges: [a->c, b->c, c->d, d->e]
        Remove edge: c->d
        Result graph 1: Nodes: [a, b, c]. Edges: [a->c, b->c]
        Result graph 2: Nodes: [d, e]. Edges: [d->e]
        """
        d = nx.DiGraph()
        d.add_edges_from([("a", "c"), ("b", "c"), ("c", "d"), ("d", "e")])
        self.dag_handler.add_dag(d)
        # Check that the graph was created successfully
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        d = self.dag_handler.dags()[0]
        self.assertEqual(len(d.nodes()), 5)
        self.assertEqual(len(d.edges()), 4)
        self.assertTrue(d.has_edge("a", "c"))
        self.assertTrue(d.has_edge("b", "c"))
        self.assertTrue(d.has_edge("c", "d"))
        self.assertTrue(d.has_edge("d", "e"))
        # Now remove the edge
        self.dag_handler.remove_graph_edge("c", "d")
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        result_d = self.dag_handler.dag_with_node("a")
        result_h = self.dag_handler.dag_with_node("d")
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(result_d.nodes()), 3)
        self.assertEqual(len(result_d.edges()), 2)
        self.assertTrue(result_d.has_edge("a", "c"))
        self.assertTrue(result_d.has_edge("b", "c"))
        self.assertEqual(len(result_h.nodes()), 2)
        self.assertEqual(len(result_h.edges()), 1)
        self.assertTrue(result_h.has_node("d"))
        self.assertTrue(result_h.has_node("e"))
        self.assertTrue(result_h.has_edge("d", "e"))

    def test_remove_graph_edge6(self):
        """Test removing an edge from a graph. Splits the graph
        into two separate graphs if the nodes are not connected
        after removing the edge.
        Graph 1: Nodes: [a, b, c, d]. Edges: [a->c, b->c, c->d, a->d]
        Remove edge: a->d
        Result graph 1: Nodes: [a, b, c, d]. Edges: [a->c, b->c, c->d]
        """
        d = nx.DiGraph()
        d.add_edges_from([("a", "c"), ("b", "c"), ("c", "d"), ("a", "d")])
        self.dag_handler.add_dag(d)
        # Check that the graph was created successfully
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        d = self.dag_handler.dags()[0]
        self.assertEqual(len(d.nodes()), 4)
        self.assertEqual(len(d.edges()), 4)
        self.assertTrue(d.has_edge("a", "c"))
        self.assertTrue(d.has_edge("b", "c"))
        self.assertTrue(d.has_edge("c", "d"))
        self.assertTrue(d.has_edge("a", "d"))
        # Now remove the edge
        self.dag_handler.remove_graph_edge("a", "d")
        # There should still be just one graph
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        result_d = self.dag_handler.dag_with_node("a")
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(result_d.nodes()), 4)
        self.assertEqual(len(result_d.edges()), 3)
        self.assertTrue(result_d.has_edge("a", "c"))
        self.assertTrue(result_d.has_edge("b", "c"))
        self.assertTrue(result_d.has_edge("c", "d"))

    def test_remove_graph_edge7(self):
        """Test removing an edge from a graph. Splits the graph
        into two separate graphs if the nodes are not connected
        after removing the edge.
        Graph 1: Nodes: [a, b, c]. Edges: [a->c, b->c, a->a, b->b, c->c]
        Remove edges: a->a, b->b, c->c
        Result graph 1: Nodes: [a, b, c]. Edges: [a->c, b->c]
        """
        d = nx.DiGraph()
        d.add_edges_from([("a", "c"), ("b", "c"), ("a", "a"), ("b", "b"), ("c", "c")])
        self.dag_handler.add_dag(d)
        # Check that the graph was created successfully
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        d = self.dag_handler.dags()[0]
        self.assertEqual(len(d.nodes()), 3)
        self.assertEqual(len(d.edges()), 5)
        self.assertTrue(d.has_edge("a", "c"))
        self.assertTrue(d.has_edge("b", "c"))
        self.assertTrue(d.has_edge("a", "a"))
        self.assertTrue(d.has_edge("b", "b"))
        self.assertTrue(d.has_edge("c", "c"))
        # Now remove all feedback links
        self.dag_handler.remove_graph_edge("a", "a")
        self.dag_handler.remove_graph_edge("b", "b")
        self.dag_handler.remove_graph_edge("c", "c")
        # There should still be just one graph
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        result_d = self.dag_handler.dag_with_node("a")
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(result_d.nodes()), 3)
        self.assertEqual(len(result_d.edges()), 2)
        self.assertTrue(result_d.has_edge("a", "c"))
        self.assertTrue(result_d.has_edge("b", "c"))

    def test_remove_graph_edge8(self):
        """Test removing an edge from a graph. Splits the graph
        into two separate graphs if the nodes are not connected
        after removing the edge. Test that self-loops remain in result graphs.
        Graph 1: Nodes: [a, b, c, d]. Edges: [a->c, b->c, c->d, a->a, b->b, c->c, d->d]
        Remove edge: c->d
        Result graph 1: Nodes: [a, b, c]. Edges: [a->c, b->c, a->a, b->b, c->c]
        Result graph 2: Nodes: [d]. Edges: [d->d]
        """
        d = nx.DiGraph()
        d.add_edges_from([("a", "c"), ("b", "c"), ("c", "d"), ("a", "a"), ("b", "b"), ("c", "c"), ("d", "d")])
        self.dag_handler.add_dag(d)
        # Check that the graph was created successfully
        self.assertTrue(len(self.dag_handler.dags()) == 1)
        d = self.dag_handler.dags()[0]
        self.assertEqual(len(d.nodes()), 4)
        self.assertEqual(len(d.edges()), 7)
        self.assertTrue(d.has_edge("a", "c"))
        self.assertTrue(d.has_edge("b", "c"))
        self.assertTrue(d.has_edge("c", "d"))
        self.assertTrue(d.has_edge("a", "a"))
        self.assertTrue(d.has_edge("b", "b"))
        self.assertTrue(d.has_edge("c", "c"))
        self.assertTrue(d.has_edge("d", "d"))
        # Now remove edge
        self.dag_handler.remove_graph_edge("c", "d")
        # There should be two graphs now
        self.assertTrue(len(self.dag_handler.dags()) == 2)
        result_d = self.dag_handler.dag_with_node("a")
        result_h = self.dag_handler.dag_with_node("d")
        # Check that the number of nodes and edges match and they are correct
        self.assertEqual(len(result_d.nodes()), 3)
        self.assertEqual(len(result_d.edges()), 5)
        self.assertTrue(result_d.has_edge("a", "c"))
        self.assertTrue(result_d.has_edge("b", "c"))
        self.assertTrue(result_d.has_edge("a", "a"))
        self.assertTrue(result_d.has_edge("b", "b"))
        self.assertTrue(result_d.has_edge("c", "c"))
        self.assertEqual(len(result_h.nodes()), 1)
        self.assertEqual(len(result_h.edges()), 1)
        self.assertTrue(result_h.has_edge("d", "d"))

    @unittest.skip("TODO")
    def test_remove_node_from_graph(self):
        self.fail()

    @unittest.skip("TODO")
    def test_execution_order(self):
        self.fail()
