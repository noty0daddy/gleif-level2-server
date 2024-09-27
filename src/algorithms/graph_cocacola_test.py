import os
import pytest
from graph_builder import DirectNodeGraphWithParentNetworkBuilder
from graph import Graph


@pytest.fixture(scope="class")
def setup(request):
    """Sets up the test environment and builds a parent network graph.
    
    Args:
        request (pytest.FixtureRequest): The pytest request object containing configuration information.
    
    Returns:
        tuple: A tuple containing:
            - list: The array representation of the parent network graph structure.
            - str: The LEI (Legal Entity Identifier) used as the starting point for the graph.
    """
    rr_csv = os.path.join(request.config.rootdir, "data", "gleif_rr.csv")
    lookup_csv = os.path.join(request.config.rootdir, "data", "gleif_lei.csv")
    lei = "UWJKFUJFZ02DKWI3RY53"
    builder = DirectNodeGraphWithParentNetworkBuilder()

    glei_network = Graph.from_csv(f=rr_csv, limit=None)
    Graph.set_lookup_table(f=lookup_csv)

    parent_graph, _ = builder.build(glei_network, lei)

    structure = parent_graph.set_levels(lei).to_array()
    return structure, lei


def test_nodes_edges_more_than_0(setup):
    """
    Tests if the number of nodes and edges in the setup structure is greater than zero.
    
    Args:
        setup (tuple): A tuple containing the structure and other setup data.
    
    Returns:
        ```
        """Tests if the LEI (Legal Entity Identifier) is present in the nodes of the structure.
        
        Args:
            setup (tuple): A tuple containing the structure dictionary and LEI string.
        
        Returns:
            None: This function doesn't return anything, it uses assertions for testing.
        """
        ```
        None: This function doesn't return anything, it uses assertions.
    """
    structure, _ = setup

    assert len(structure["nodes"]) > 0
    assert len(structure["edges"]) > 0


def test_lei_in_nodes(setup):
    structure, lei = setup
    cocacolacompany_node = [n for n in structure["nodes"] if n["id"] == lei][0]

    assert cocacolacompany_node["level"] == 0


def test_direct_children(setup):
    """Tests the direct children of the root node in the structure.
    
    Args:
        setup (tuple): A tuple containing the structure and other setup information.
    
    Returns:
        None: This function doesn't return anything, it uses assertions for testing.
    """
    structure, _ = setup
    # direct children
    direct_children = [n for n in structure["nodes"] if n["level"] == 1]
    assert len(direct_children) == 8

