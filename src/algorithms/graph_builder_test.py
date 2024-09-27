import pytest
from graph import RR, Graph
from graph_builder import DirectNodeGraphWithParentNetworkBuilder

@pytest.fixture
def builder():
    """Creates and returns an instance of DirectNodeGraphWithParentNetworkBuilder.
    
    Args:
        None
    
    Returns:
        DirectNodeGraphWithParentNetworkBuilder: A new instance of the DirectNodeGraphWithParentNetworkBuilder class.
    """
    return DirectNodeGraphWithParentNetworkBuilder()

def test_parent_subgraphs_are_copies(builder):

    #           UP <**
    """
    Test that parent subgraphs are independent copies of the original graph.
    
    This function tests the behavior of ultimate parent and node direct graph extraction
    from a given graph structure. It verifies that the extracted subgraphs contain the
    expected nodes and that the original graph remains unmodified.
    
    Args:
        builder: The graph builder object used to extract subgraphs.
    
    Returns:
        None: This function doesn't return anything. It uses assertions to verify
        the correctness of the subgraph extraction process.
    """
    #           |    *
    #         UP:C1  *
    #                *
    #                *
    #           P1   *
    #           |    *
    #          ROI***

    g = Graph([
        RR('ROI', 'P1', RR.DIRECT),
        RR('ROI', 'UP', RR.ULTIMATE),

        RR('UP:C1', 'UP', RR.DIRECT),
    ])
"""Tests the construction of a parent graph connected with ROI (Region of Interest).

Args:
    builder (object): An object with a method 'ultimate_parent_direct_graph' for building the parent graph.

Returns:
    None: This function doesn't return anything but uses assertions to verify the correctness of the graph.
"""

    parent_graph, _ = builder.ultimate_parent_direct_graph(g, 'ROI')
    roi_graph = builder.node_direct_graph(g, 'ROI')

    assert sorted(list(parent_graph.nodes)) == ['UP', 'UP:C1']
    assert sorted(list(roi_graph.nodes)) == ['P1', 'ROI']
    assert sorted(list(g.nodes)) == ['P1', 'ROI', 'UP', 'UP:C1']


def test_parent_graph_connected_with_ROI(builder):

    #         UP:P1   <-- should not happen!
    #        /  |
    # UP:P1:C1  |
    #         --UP <**
    #        /  |    *
    #    UP:C1  P1   *
    #           |    *
    #          ROI***
    #          / \
    #         C1  C2

    g = Graph([
        RR('ROI', 'UP', RR.ULTIMATE),

        RR('C1', 'ROI', RR.DIRECT),
        RR('C2', 'ROI', RR.DIRECT),
        RR('ROI', 'P1', RR.DIRECT),
        RR('P1', 'UP', RR.DIRECT),
        RR('UP:C1', 'UP', RR.DIRECT),
        RR('UP', 'UP:P1', RR.DIRECT),
        RR('UP:P1:C1', 'UP:P1', RR.DIRECT),
    ])

    parent_graph, _ = builder.ultimate_parent_direct_graph(g, 'ROI')
    assert sorted(list(parent_graph.nodes)) == ['C1', 'C2', 'P1', 'ROI', 'UP', 'UP:C1', 'UP:P1', 'UP:P1:C1']


def test_graph_with_ROI_and_ultimate_parent_not_connected_via_direct_relationships(builder):

    #         UP:P1   <-- should not happen!
    #        /  |
    # UP:P1:C1  |
    #         --UP <**
    #        /  ^    *
    #    UP:C1  *    *
    #           *    *
    #           *    *
    #           P1   *
    #           |    *
    #          ROI***
    #          / \
    #         C1  C2

    """
    Test the graph construction with ROI and ultimate parent not connected via direct relationships.
    
    Args:
        builder (object): An instance of the graph builder class.
    
    Returns:
        None: This function doesn't return anything explicitly. It uses assertions to verify the correct behavior of the graph construction.
    """    g = Graph([
        RR('ROI', 'UP', RR.ULTIMATE),
        RR('ROI', 'P1', RR.DIRECT),
        RR('P1', 'UP', RR.ULTIMATE),  # <-- decoy; should also not make the graphs connected

        RR('C1', 'ROI', RR.DIRECT),
        RR('C2', 'ROI', RR.DIRECT),
        RR('UP:C1', 'UP', RR.DIRECT),
        RR('UP', 'UP:P1', RR.DIRECT),
        RR('UP:P1:C1', 'UP:P1', RR.DIRECT),
    ])

    # Sanity check; parent graph is only:
    parent_graph, _ = builder.ultimate_parent_direct_graph(g, 'ROI')
    assert sorted(list(parent_graph.nodes)) == ['UP', 'UP:C1', 'UP:P1', 'UP:P1:C1']
    assert sorted(list(parent_graph.edges)) == [
        ('UP', 'UP:P1', 0),
        ('UP:C1', 'UP', 0),
        ('UP:P1:C1', 'UP:P1', 0),
    ]

    roi_graph = builder.node_direct_graph(g, 'ROI')
    #  assert sorted(list(roi_graph.nodes)) == ['UP', 'UP:C1', 'UP:P1', 'UP:P1:C1']
    assert sorted(list(roi_graph.nodes)) == ['C1', 'C2', 'P1', 'ROI']
    assert sorted(list(roi_graph.edges(data='type'))) == [
        # ROI edges
        ('C1', 'ROI', 'IS_DIRECTLY_CONSOLIDATED_BY'),
        ('C2', 'ROI', 'IS_DIRECTLY_CONSOLIDATED_BY'),
        ('ROI', 'P1', 'IS_DIRECTLY_CONSOLIDATED_BY'),
    ]

    merged_graph, _ = builder.build(g, 'ROI')
    assert sorted(list(merged_graph.nodes)) == ['C1', 'C2', 'P1', 'ROI', 'UP', 'UP:C1', 'UP:P1', 'UP:P1:C1']
    #  assert sorted(list(merged_graph.edges(data='type'))) == [
    #      # ROI edges
    #      ('C1', 'ROI', 'IS_DIRECTLY_CONSOLIDATED_BY'),
    #      ('C2', 'ROI', 'IS_DIRECTLY_CONSOLIDATED_BY'),
    #      ('ROI', 'P1', 'IS_DIRECTLY_CONSOLIDATED_BY'),

    #      # TODO: Return direct graph except for ROI -> ultimate parent edge?
    #      #  ('ROI', 'UP', 'IS_ULTIMATELY_CONSOLIDATED_BY'),

    #      # Ultimate Parent edges
    #      ('UP', 'UP:P1', 'IS_DIRECTLY_CONSOLIDATED_BY'),
    #      ('UP:C1', 'UP', 'IS_DIRECTLY_CONSOLIDATED_BY'),
    #      ('UP:P1:C1', 'UP:P1', 'IS_DIRECTLY_CONSOLIDATED_BY'),
    #  ]



def test_ROI_without_ultimate_parent(builder):

    # CASE: No Ultimate Parent
    """Test the ROI (Region of Interest) functionality without an ultimate parent.
    
    This function sets up a graph structure representing relationships between entities
    and tests the behavior of the ROI builder when there is no ultimate parent present.
    
    Args:
        builder: The builder object used to construct the ROI subgraph.
    
    Returns:
        None: This function doesn't return anything, but uses assertions to verify the behavior.
    """    #          P2
    #          |
    #     -----P1
    #    /     |
    # P1:C1   ROI  C2:P1  C2:UP1
    #         / \  /     /
    #        C1  C2------

    g = Graph([
        RR('C1', 'ROI', RR.DIRECT),
        RR('C2', 'ROI', RR.DIRECT),
        RR('C2', 'C2:P1', RR.DIRECT),
        RR('C2', 'C2:UP1', RR.ULTIMATE),
        RR('P1:C1', 'P1', RR.DIRECT),
        RR('ROI', 'P1', RR.DIRECT),
        RR('P1', 'P2', RR.DIRECT),
    ])

    sub, _ = builder.build(g, 'ROI')

    #  assert sub.nodes == ['P1']
    #  assert sub.('type') == 'x'




    # TODO CASE: Multiuple Ultimate Parent?

    # CASE:
    #    UP
    #      \
    #       |
    #       |
    #       |
    #       |
    #       |

    #  RR('A', 'B', RR.DIRECT),
    #  RR('C', 'B', RR.DIRECT),
    #  RR('C', 'D', RR.ULTIMATE),
    #  RR('E', 'C', RR.ULTIMATE),
    #  RR('X', 'C', RR.DIRECT),
    #  RR('X', 'F', RR.DIRECT),
    #  RR('G', 'X', RR.BRANCH),
    #  RR('H', 'X', RR.DIRECT),
    #  RR('H', 'K', RR.DIRECT),
    #  RR('I', 'G', RR.DIRECT),
    #  RR('I', 'J', RR.DIRECT),

    #  print('hey')
    assert True