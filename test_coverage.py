import pytest
# Import your functions here
from coverage_criteria import node_coverege_test_paths, edge_coverage_test_paths, prime_path_coverage_test_paths



# Node Coverage Test Cases

# Unit Test - Test whether the node_coverage_test_paths function returns the correct list of paths covering all nodes in the graph
def test_node_coverage_unit():
    # Define a simple graph
    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = node_coverege_test_paths(graph, start_node, end_node)

    # Check if the returned paths cover all nodes in the graph
    assert set.union(*[set(path) for path in result]) == set(graph.keys())

# Edge Coverage Test Cases

# Unit Test - Test whether the edge_coverage_test_paths function returns the correct extended paths covering all edges in the graph
def test_edge_coverage_unit():
    # Define a simple graph
    graph = {
        'A': ['B','C'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = edge_coverage_test_paths(graph, start_node, end_node)

    print(result)
    # Check if the extended paths cover all edges in the graph
    extended_paths = result[0]
    covered_edges = set()
    for path in extended_paths:
        for i in range(len(path) - 1):
            covered_edges.add((path[i], path[i+1]))
    
    assert covered_edges == {(node, next_node) for node in graph for next_node in graph[node]}

# Prime Path Coverage Test Cases

# Unit Test - Test whether the prime_path_coverage_test_paths function returns unique prime coverage test paths
def test_prime_path_coverage_unit():
    # Define a simple graph
    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = prime_path_coverage_test_paths(graph, start_node, end_node)

    # Check if the returned paths are unique prime coverage test paths
    unique_paths = result[0]
    assert len(unique_paths) == len(set("".join(path) for path in unique_paths))




# Integration Test - Test whether the prime_path_coverage_test_paths function integrates well with extending_paths function
def test_prime_path_coverage_integration():
    # Define a simple graph
    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = prime_path_coverage_test_paths(graph, start_node, end_node)
    # Check if the returned paths are extended prime coverage test paths
    extended_paths = result[0]
    assert all(len(path) > 1 for path in extended_paths)  # Ensure paths are extended


# Prime Path Coverage Test Cases

# Unit Test - Test whether the prime_path_coverage_test_paths function returns unique prime coverage test paths
def test_prime_path_coverage_unit():
    # Define a simple graph
    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = prime_path_coverage_test_paths(graph, start_node, end_node)

    # Check if the returned paths are unique prime coverage test paths
    unique_paths = result[0]
    assert len(unique_paths) == len(set("".join(path) for path in unique_paths))

# Integration Test - Test whether the prime_path_coverage_test_paths function integrates well with extending_paths function
def test_prime_path_coverage_integration():
    # Define a simple graph
    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = prime_path_coverage_test_paths(graph, start_node, end_node)

    # Check if the returned paths are extended prime coverage test paths
    extended_paths = result[0]
    assert all(len(path) > 1 for path in extended_paths)  # Ensure paths are extended

# Edge Cases

# Edge Case - Test with empty graph
def test_empty_graph():
    graph = {}
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = node_coverege_test_paths(graph, start_node, end_node)

    # Check if the result is empty
    assert result == []

# Edge Case - Test with graph containing loops
def test_graph_with_loops():
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['D'],
        'D': ['A']  # Loop back to A
    }
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = node_coverege_test_paths(graph, start_node, end_node)

    # Check if the result is empty (shouldn't be able to cover all nodes due to the loop)
    assert set.union(*[set(path) for path in result]) == set(graph.keys())

# Edge Case - Test with isolated nodes
def test_graph_with_isolated_nodes():
    graph = {
        'A': ['B', 'C'],
        'B': [],
        'C': [],
        'D': ['A']  
    }
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = node_coverege_test_paths(graph, start_node, end_node)

    # Check if the result is empty (isolated nodes cannot be reached)
    print(result)
    assert result == []


# Edge Case - Test with invalid start_node or end_node
def test_invalid_start_or_end_node():
    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    start_node = 'X'  # Invalid start node
    end_node = 'D'

    # Call the function
    with pytest.raises(KeyError):
        node_coverege_test_paths(graph, start_node, end_node)



# System Test - Test whether the node_coverage_test_paths function works correctly with the entire system
def test_node_coverage_system():
    # Write system-level test case here, if applicable
    pass

# Repeat similar tests for edge_coverage_test_paths and prime_path_coverage_test_paths

