import os
import pytest
from graph_builder import DirectNodeGraphWithParentNetworkBuilder
from graph import Graph


@pytest.fixture(scope="class")
def setup(request):
    """
    Sets up the test environment and builds a parent network graph.
    
    Args:
        request (pytest.FixtureRequest): The pytest request object containing configuration information.
    
    Returns:
        tuple: A tuple containing:
            - list: The hierarchical structure of the parent network as an array.
            - str: The Legal Entity Identifier (LEI) used for building the network.
    """
    rr_csv = os.path.join(request.config.rootdir, "data", "gleif_rr.csv")
    lookup_csv = os.path.join(request.config.rootdir, "data", "gleif_lei.csv")
    lei = "969500WU8KVE8U3TL824"
    builder = DirectNodeGraphWithParentNetworkBuilder()

    glei_network = Graph.from_csv(f=rr_csv, limit=None)
    Graph.set_lookup_table(f=lookup_csv)

    parent_graph, ultimate_parent = builder.build(glei_network, lei)

    if ultimate_parent:
        structure = parent_graph.set_levels(ultimate_parent).to_array()
    else:
        structure = parent_graph.set_levels(lei).to_array()

    return structure, lei


def test_structure_exists(setup):
```
"""Test if the A2 node is at level 0.

This test checks if a specific LEI (Legal Entity Identifier) node in the structure
does not have an ultimate parent, and therefore is at level 0.

Args:
    setup (tuple): A tuple containing the structure and LEI for testing.

Returns:
    None: This test function doesn't return anything explicitly.
          It uses assertions to validate the expected behavior.
"""
```

    """
    Verifies the existence and structure of a test setup.
    
    Args:
        setup (tuple): A tuple containing the structure and other test setup elements.
    
    Returns:
        None: This function doesn't return anything, it uses assertions to check conditions.
    """
    structure, _ = setup

    assert len(structure["nodes"]) > 0
    # this LEI does not have children nor a parent
    assert len(structure["edges"]) == 0


def test_a2_node_is_level_0(setup):
    # this LEI does not have an ultimate parent

    structure, lei = setup

    a2_node = [n for n in structure["nodes"] if n["id"] == lei][0]

    assert a2_node["level"] == 0

