import os
import pytest
from graph_builder import DirectNodeGraphWithParentNetworkBuilder
from graph import Graph


@pytest.fixture
def builder():
    """Creates and returns a DirectNodeGraphWithParentNetworkBuilder instance.
    
    Args:
        None
    
    """
    Generates the file path for the 'gleif_rr.csv' file.
    
    Args:
        request (object): The request object containing configuration information.
    
    Returns:
        str: The full path to the 'gleif_rr.csv' file.
    """
    """Tests the Samsung ultimate parent relationship in a graph structure.
    
    Args:
        builder (object): The builder object used to construct the graph.
        lookup_csv (str): Path to the CSV file containing lookup data.
        rr_csv (str): Path to the CSV file containing relationship data.
    
    Returns:
        None: This function doesn't return anything, it uses assertions to verify the graph structure.
    """
    Returns:
        DirectNodeGraphWithParentNetworkBuilder: A new instance of the DirectNodeGraphWithParentNetworkBuilder class.
    """    return DirectNodeGraphWithParentNetworkBuilder()


"""
Constructs the full path to the 'gleif_lei.csv' file in the 'data' directory.

Args:
    request: An object containing the test configuration.

Returns:
    str: The absolute path to the 'gleif_lei.csv' file.
"""
@pytest.fixture
def rr_csv(request):
    return os.path.join(request.config.rootdir, "data", "gleif_rr.csv")


@pytest.fixture
def lookup_csv(request):
    return os.path.join(request.config.rootdir, "data", "gleif_lei.csv")


def test_samsung_ultimate_parent(builder, lookup_csv, rr_csv):
    samsung_lei = "549300KYVNLA5XR0HT53"
    ultimate_parent_lei = "9884007ER46L6N7EI764"

    glei_network = Graph.from_csv(f=rr_csv, limit=None)
    Graph.set_lookup_table(f=lookup_csv)

    parent_graph, _ = builder.build(glei_network, samsung_lei)
    structure = parent_graph.set_levels(ultimate_parent_lei).to_array()

    samsung_node = [n for n in structure["nodes"] if n["id"] == samsung_lei][0]
    ultimate_parent_node = [
        n for n in structure["nodes"] if n["id"] == ultimate_parent_lei
    ][0]

    # nodes between ultimate parent and samsung
    intermediate_nodes = [n for n in structure["nodes"] if n["level"] == 1]

    assert ultimate_parent_node["level"] == 0
    assert len(intermediate_nodes) > 0
    assert samsung_node["level"] == 2

    # assert that the correct edges exist
    # samsung gmbh -> samsung holding gmbh
    assert (
        find_edge(structure["edges"], samsung_lei, "549300CWESV5NI78YL42") is not None
    )
    # samsung holding gmbh -> korean samsung / ultimate parent
    assert (
        find_edge(structure["edges"], "549300CWESV5NI78YL42", ultimate_parent_lei)
        is not None
    )


def find_edge(edges, from_lei, to_lei):
    """
    Finds an edge in a list of edges based on the given 'from' and 'to' LEI (Legal Entity Identifier) values.
    
    Args:
        edges (list): A list of edge dictionaries, where each edge contains 'from' and 'to' keys.
        from_lei (str): The LEI of the source node.
        to_lei (str): The LEI of the target node.
    
    Returns:
        dict or None: The edge dictionary if found, or None if no matching edge is found.
    """
    for e in edges:
        if e["from"] == from_lei and e["to"] == to_lei:
            return e
    return None

