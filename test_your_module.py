import networkx as nx
import pytest
from graph_coverage import generate_test_paths

# Define test cases for Node Coverage
@pytest.mark.parametrize("graph_input, start_node, end_node, expected_test_paths", [
    # Test case 1: Simple graph with single node coverage
    ({"A": ["B"], "B": ["C"], "C": []}, "A", "C", [["A", "B", "C"]]),
    # Test case 2: Graph with multiple paths from start to end node
    ({"A": ["B", "C"], "B": ["C"], "C": []}, "A", "C", [["A", "B", "C"], ["A", "C"]]),
    # Test case 3: Graph with loops
    ({"A": ["B", "C"], "B": ["C", "A"], "C": ["B"]}, "A", "C", [["A", "B", "C"], ["A", "C"]]),
    # Test case 4: Single node graph
    ({"A": []}, "A", "A", [["A"]]),
    # Test case 5: Graph with isolated nodes
    ({"A": ["B"], "B": [], "C": []}, "A", "B", [["A", "B"]]),
    # Test case 6: Graph with multiple paths from start to end node with different lengths
    ({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, "A", "D", [["A", "B", "D"], ["A", "C", "D"]]),
])

def test_node_coverage(graph_input, start_node, end_node, expected_test_paths):
    graph = nx.DiGraph(graph_input)
    test_paths = generate_test_paths(graph, start_node, end_node, "Node Coverage")
    assert test_paths == expected_test_paths

# Define test cases for Edge Coverage
@pytest.mark.parametrize("graph_input, start_node, end_node, expected_test_paths", [
    # Test case 1: Simple graph with single edge coverage
    ({"A": ["B"], "B": ["C"], "C": []}, "A", "C", [["A", "B", "C"]]),
    # Test case 2: Graph with multiple paths from start to end node
    ({"A": ["B", "C"], "B": ["C"], "C": []}, "A", "C", [["A", "B", "C"], ["A", "C"]]),
    # Test case 3: Graph with loops
    ({"A": ["B", "C"], "B": ["C", "A"], "C": ["B"]}, "A", "C", [["A", "B", "C"], ["A", "C"]]),
    # Test case 4: Single node graph
    ({"A": []}, "A", "A", []),
    # Test case 5: Graph with isolated nodes
    ({"A": ["B"], "B": [], "C": []}, "A", "B", [["A", "B"]]),
    # Test case 6: Graph with multiple paths from start to end node with different lengths
    ({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, "A", "D", [["A", "B", "D"], ["A", "C", "D"]]),
])

def test_edge_coverage(graph_input, start_node, end_node, expected_test_paths):
    graph = nx.DiGraph(graph_input)
    test_paths = generate_test_paths(graph, start_node, end_node, "Edge Coverage")
    assert test_paths == expected_test_paths

# Define test cases for Prime Path Coverage
@pytest.mark.parametrize("graph_input, start_node, end_node, expected_test_paths", [
    # Test case 1: Simple graph with single prime path coverage
    ({"A": ["B", "C"], "B": ["C"], "C": []}, "A", "C", [["A", "B", "C"], ["A", "C"]]),
    # Test case 2: Graph with multiple paths from start to end node
    ({"A": ["B", "C"], "B": ["C"], "C": []}, "A", "C", [["A", "B", "C"], ["A", "C"]]),
    # Test case 3: Graph with loops
    ({"A": ["B", "C"], "B": ["C", "A"], "C": ["B"]}, "A", "C", [["A", "B", "C"], ["A", "C"]]),
    # Test case 4: Single node graph
    ({"A": []}, "A", "A", [["A"]]),
    # Test case 5: Graph with isolated nodes
    ({"A": ["B"], "B": [], "C": []}, "A", "B", [["A", "B"]]),
    # Test case 6: Graph with multiple paths from start to end node with different lengths
    ({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, "A", "D", [["A", "B", "D"], ["A", "C", "D"]]),
])

def test_prime_path_coverage(graph_input, start_node, end_node, expected_test_paths):
    graph = nx.DiGraph(graph_input)
    test_paths = generate_test_paths(graph, start_node, end_node, "Prime Path Coverage")
    assert test_paths == expected_test_paths

# Define test case for invalid coverage criteria in Node Coverage
'''

def test_invalid_node_coverage():
    graph = {"A": ["B"], "B": ["C"], "C": []}
    start_node = "A"
    end_node = "C"
    invalid_coverage_criteria = "Invalid Coverage Criteria"

    with pytest.raises(ValueError):
        generate_test_paths(graph, start_node, end_node, invalid_coverage_criteria)

# Define test case for invalid coverage criteria in Edge Coverage
def test_invalid_edge_coverage():
    graph = {"A": ["B"], "B": ["C"], "C": []}
    start_node = "A"
    end_node = "C"
    invalid_coverage_criteria = "Invalid Coverage Criteria"

    with pytest.raises(ValueError):
        generate_test_paths(graph, start_node, end_node, invalid_coverage_criteria)

# Define test case for invalid coverage criteria in Prime Path Coverage
def test_invalid_prime_path_coverage():
    graph = {"A": ["B"], "B": ["C"], "C": []}
    start_node = "A"
    end_node = "C"
    invalid_coverage_criteria = "Invalid Coverage Criteria"

    with pytest.raises(ValueError):
        generate_test_paths(graph,start_node, end_node, invalid_coverage_criteria)

'''

def run_all_tests():
    # Call each test function
    test_node_coverage()
    test_edge_coverage()
    test_prime_path_coverage()
    # test_invalid_node_coverage()
    # test_invalid_edge_coverage()
    # test_invalid_prime_path_coverage()

if __name__ == "__main__":
    run_all_tests()