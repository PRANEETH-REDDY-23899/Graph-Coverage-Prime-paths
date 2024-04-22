'''
                                CSI 680 Milestone 4
                                        Team K
Team Members:
    1. Praneeth Reddy Nakka (pnakka@albany.edu)
    2. Praneeth Yennam (pyennam@albany.edu)
    3. Rohith Jellipalli (rjellipalli@albany.edu)
    4. Ajay Kumar Reddy Boreddy (aboreddy@albany.edu)

Project:Graph Coverage prime paths.
        Graph coverage prime paths is a software tool that we are going to build 
        that will help the users by generating test paths to satisfy graph coverage 
        test criteria. The tool will prompt the user to enter the graph and choose 
        the start and end nodes appropriately.

'''
# -------------------------------------------------------------------------------------

# File: test_coverage.py

import pytest # Importing pytest module
from coverage_criteria import node_coverege_test_paths,edge_coverage_test_paths, prime_path_coverage_test_paths
from graph_coverage import remove_empty_spaces, check_graph_syntax
from coverage_criteria import find_prime_paths

# -------------------------------------------------------------------------------------
                    # Test Cases.
                    # pytest module is used for testing.
                    # open terminal and run the command 'pytest' to run the test cases.  
# -------------------------------------------------------------------------------------

# Test Case : 1
# Unit Test - To test node coverage with a simple graph scenario and check if all nodes are covered.
'''
Purpose : The purpose of this test is to ensure that the `node_coverege_test_paths` 
          function behaves correctly at a granular level by providing the expected 
          paths for node coverage testing in a simple graph scenario.The test checks 
          whether the paths returned by the function cover all nodes in the graph.
'''
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

    # Calling the function
    result, un_covered_paths = node_coverege_test_paths(graph, start_node, end_node)

    # Checking if the returned paths cover all nodes in the graph
    assert set.union(*[set(path) for path in result]) == set(graph.keys())
# -------------------------------------------------------------------------------------

# Test Case : 2
# Unit Test - To test edge coverage with a simple graph scenario and check if all edges are covered.
'''
Purpose : The purpose of this test is to ensure that the `edge_coverage_test_paths` 
          function behaves correctly at a granular level by providing the expected 
          extended paths for edge coverage testing in a simple graph scenario. 
          The test checks whether the extended paths cover all edges in the graph.
'''
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

    # Calling the function
    result = edge_coverage_test_paths(graph, start_node, end_node)

    # Checking if the extended paths cover all edges in the graph
    extended_paths = result[0]
    covered_edges = set()
    for path in extended_paths:
        for i in range(len(path) - 1):
            covered_edges.add((path[i], path[i+1]))
    
    assert covered_edges == {(node, next_node) for node in graph for next_node in graph[node]}

# -------------------------------------------------------------------------------------------
# Test Case : 3
# Integration Test - To test prime path coverage 

'''
Purpose : The purpose of this test is to validate the integration and functionality of 
          the `prime_path_coverage_test_paths` function by ensuring that it generates 
          the expected extended prime coverage test paths in a simple graph scenario. 
          The test evaluates the behavior of the function in conjunction with its 
          internal components.
'''
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

    prime_paths = find_prime_paths(graph)

    # Call the function
    result = prime_path_coverage_test_paths(graph, start_node, end_node)
    # Checking if the returned paths are extended prime coverage test paths
    extended_paths = result[0]

    # explore the extended paths and see if it contains the prime paths as subpaths
    # extend path is a list of paths
    covered_prime_paths = []
    for path in extended_paths:
        for prime_path in prime_paths:
            if "".join(prime_path) in "".join(path):
                if prime_path not in covered_prime_paths:
                    covered_prime_paths.append(prime_path)

    assert covered_prime_paths == prime_paths
    
        
# -------------------------------------------------------------------------------------------

# Test Case : 4
# Unit test - Test Node coverage with empty graph
'''
Purpose : The purpose of this test is to ensure that the `node_coverege_test_paths` 
          function behaves as expected when given an empty graph as input. The test 
          checkswhether the function returns an empty list as expected when the graph 
          has no nodes.
'''
def test_empty_graph():
    graph = {}
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = node_coverege_test_paths(graph, start_node, end_node)

    # Check if the result is empty
    assert result == []
#-------------------------------------------------------------------------------------------

# Test Case : 5
# Unit Test - Test Node coverage with a graph with loops
'''
Purpose : The purpose of this test is to verify how the `node_coverege_test_paths` 
          function behaves when it encounters a graph with loops. The assertion 
          checks whether the function correctly handles such cases by ensuring that 
          the output paths cover all nodes in the graph, despite the presence of the loop.
'''
def test_node_coverage_graph_with_loops():
    
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['D'],
        'D': ['A']  # Loop back to A
    }
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result, un_covered = node_coverege_test_paths(graph, start_node, end_node)

    # Check if the result is empty (shouldn't be able to cover all nodes due to the loop)
    assert set.union(*[set(path) for path in result]) == set(graph.keys())

# -------------------------------------------------------------------------------------------

# Test Case : 6
# Unit Test - Test Node coverage with isolated nodes
'''
Purpose: The purpose of this test is to verify how the `node_coverege_test_paths` 
         function handles graphs with isolated nodes. The assertion checks whether 
         the function correctly handles such cases by ensuring that no paths are returned 
         since the isolated nodes cannot be reached.
'''
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
    result, un_covered_paths = node_coverege_test_paths(graph, start_node, end_node)

    # Check if the result is empty (isolated nodes cannot be reached)
    # print(result)
    assert result == []
# -------------------------------------------------------------------------------------------

# Test Case : 7
# Unit Test- Test with invalid start_node or end_node
'''
Purpose :  The purpose of this test is to ensure that the `node_coverege_test_paths` 
           function correctly raises a KeyError when provided with an invalid start node
           that does not exist in the graph. The test uses pytest.raises to check whether
           the function raises the expected exception.
'''
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

# -------------------------------------------------------------------------------------------
# Test Case : 8
# Unit Test - Test with a graph with spaces in node names and neighbor names
'''
Purpose : The purpose of this test is to ensure that the `remove_empty_spaces` function 
          behaves as expected by removing leading and trailing whitespace from node 
          names and neighbor names. The test compares the cleaned graph returned by 
          the function with the expected cleaned graph.
'''
def test_remove_empty_spaces():
    # Test case to ensure that leading and trailing whitespace is removed from node names and neighbor names
    graph_input = {
        '   A   ': ['  B  ', 'C  '],
        '  B ': ['  C  ', 'D'],
        ' C  ': [' D', ' E '],
        'D  ': ['  E ', ' F'],
        '  E  ': [' F ', '   G   '],
        ' F ': ['   G', 'H'],
        ' G ': ['   H  ', 'I'],
        '  H  ': ['  I  '],
        '  I  ': ['  J  '],
        '  J  ': ['  K  ']
    }

    # Expected cleaned graph
    expected_cleaned_graph = {
        'A': ['B', 'C'],
        'B': ['C', 'D'],
        'C': ['D', 'E'],
        'D': ['E', 'F'],
        'E': ['F', 'G'],
        'F': ['G', 'H'],
        'G': ['H', 'I'],
        'H': ['I'],
        'I': ['J'],
        'J': ['K']
    }

    # Call the function
    cleaned_graph = remove_empty_spaces(graph_input)

    # Checking if the cleaned graph matches the expected result
    assert cleaned_graph == expected_cleaned_graph

# -------------------------------------------------------------------------------------------

# Test Case : 9
# Unit Test - Test with incorrect graph syntax
'''
Purpose :  The purpose of this test is to ensure that the `check_graph_syntax` function 
           behaves as expected by correctly identifying whether the syntax of the input 
           graph is valid or not. The test compares the boolean results returned by the 
           function for both correct and incorrect input graphs.
'''
def test_check_graph_syntax():
    # Test case to check the syntax of the graph input
    # Input graph with correct syntax
    graph_input_correct = "{'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B']}"
    # Input graph with incorrect syntax (missing quotes for keys and values)
    graph_input_incorrect = "{A: [B, C], B: [A, C], C: [A, B]}"

    # Call the function with correct input
    result_correct = check_graph_syntax(graph_input_correct)
    # Call the function with incorrect input
    result_incorrect = check_graph_syntax(graph_input_incorrect)

    # Check if the function correctly identifies the syntax of the graph input
    assert result_correct == True
    assert result_incorrect == False
# -------------------------------------------------------------------------------------------

# Test Case :   10
# System Test - Test whether the node_coverage_test_paths function works correctly with the entire system.
'''
Purpose : The purpose of this test is to ensure that the `node_coverege_test_paths` 
          function behaves correctly within the context of a larger system by providing 
          the expected paths for coverage testing. The test compares the paths returned 
          by the function with the expected paths based on the system graph structure.
'''
def test_node_coverage_system():
    # Define a more complex graph representing a system
    system_graph = {
        'A': ['B', 'C'],
        'B': ['C', 'D'],
        'C': ['D', 'E'],
        'D': ['E'],
        'E': ['F', 'G'],
        'F': ['G'],
        'G': []
    }
    # Define start and end nodes
    start_node = 'A'
    end_node = 'G'

    # Call the function
    result = node_coverege_test_paths(system_graph, start_node, end_node)

    # Define expected paths based on the graph structure
    expected_paths = [['A', 'B', 'C', 'D', 'E', 'F', 'G']]

    # Check if the returned paths match the expected paths
    assert result[0] == expected_paths

# -------------------------------------------------------------------------------------------

# Test Case : 11
# Unit Test - Test edge coverage with a graph with loops

'''
Purpose : The purpose of this test is to validate the behavior of the 
          `edge_coverage_test_paths` function in covering all edges of a graph, 
          including those involved in loops. It checks whether the extended paths 
          cover all edges as expected, ensuring comprehensive edge coverage.
'''
def test_edge_coverage_graph_with_loops():
    # Define a graph with a loop
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['D'],
        'D': ['A'] 
        }
    start_node = 'A'
    end_node = 'D'

    # Call the function
    result = edge_coverage_test_paths(graph, start_node, end_node)

    # Extract extended paths from the result
    extended_paths = result[0]

    # Extract covered edges from the extended paths
    covered_edges = set()
    for path in extended_paths:
        for i in range(len(path) - 1):
            covered_edges.add((path[i], path[i+1]))
        

    # Define the expected covered edges
    expected_covered_edges = {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')}

    # Check if the covered edges match the expected covered edges
    assert covered_edges == expected_covered_edges

# ----------------------------------------------------------------------------------

# Test Case : 12
# Unit Test - Test the prime_path_coverage_test_paths function with a graph with loops

'''
Purpose : The purpose of the test case is to verify that the
          `prime_path_coverage_test_paths`function correctly handles graphs with loops 
          and generates extended paths that cover all prime paths in the graph. 
'''

def test_prime_path_coverage_with_loops():
    # Define a graph with a loop
    graph = {
             'A': ['B', 'C'], 
             'B': ['C'], 
             'C': ['D','E'],
             'D': ['F'], 
             'E': ['G','F'],  
             'G':['E'], 
             'F': []
             }
    start_node = 'A'
    end_node = 'F'

    # Call the function
    result = prime_path_coverage_test_paths(graph, start_node, end_node)

    # Extract extended paths from the result
    extended_paths = result[0]

    # Define the expected paths based on the graph structure
    expected_paths = [
                        ['A', 'C', 'E', 'G', 'E', 'G', 'E', 'F'],
                        ['A', 'C', 'D', 'F'],
                        ['A', 'C', 'E', 'F'],
                        ['A', 'B', 'C', 'D', 'F'],
                        ['A', 'B', 'C', 'E', 'F'],
                        ['A', 'B', 'C', 'E', 'G', 'E', 'F']
                      ]
    for path in extended_paths:
        print(path)

    # Check if the returned paths match the expected paths
    assert extended_paths == expected_paths


# -----------------------------------------------------------------------------------

# Test Case : 13
# Unit Test - Test the prime_path_coverage_test_paths function with a graph with same start and end node 

'''
Purpose : The purpose of this test case is to verify that the `prime_path_coverage_test_paths` 
          function correctly handles scenarios where the start and end nodes are the same. It ensures that 
          the function can generate extended paths covering all prime paths in the graph, considering 
          loops and the same start and end node.
'''
def test_prime_path_coverage_same_start_end_node():
    # Define a graph with a loop
    graph = {
             "A": ["B", "C"], "B": ["C", "A"], "C": ["B", "A"]
             }
    start_node = "A"
    end_node = "A"

    # Call the function
    result = prime_path_coverage_test_paths(graph, start_node, end_node)

    # Extract extended paths from the result
    extended_paths = result[0]

    # Define the expected paths based on the graph structure
    expected_paths = [
                        ['A', 'B', 'A', 'B', 'A'],
                        ['A', 'B', 'C', 'B', 'A'],
                        ['A', 'C', 'A', 'C', 'A'],
                        ['A', 'C', 'B', 'C', 'A'],
                        ['A', 'B', 'A', 'C', 'B', 'A'],
                        ['A', 'B', 'C', 'A', 'B', 'A'],
                        ['A', 'C', 'A', 'B', 'C', 'A'],
                        ['A', 'C', 'B', 'A', 'C', 'A']  
                      ]
    for path in extended_paths:
        print(path)

    # Check if the returned paths match the expected paths
    assert extended_paths == expected_paths

# -------------------------------------------------------------------------------------

# Test Case : 14
# Unit Test - To test prime path with unreached end node
'''
Purpose: The purpose of this test case is to verify that the 
         `prime_path_coverage_test_paths` function behaves correctly when the 
         end node cannot be reached from the start node in the graph.
'''
def test_prime_path_coverage_unreached_end_node():
    # Define a graph with a loop
    graph = {
             'A': ['B', 'C'], 
             'B': ['C'], 
             'C': ['D','E'],
             'D': ['F'], 
             'E': ['G','F'],  
             'G':['E'], 
             'F': []
             }
    start_node = 'A'
    end_node = 'A'

    # Call the function
    result = prime_path_coverage_test_paths(graph, start_node, end_node)

    # Extract extended paths from the result
    extended_paths = result[0]

    # Define the expected paths based on the graph structure
    expected_paths = []

    # Check if the returned paths match the expected paths
    assert extended_paths == expected_paths

# --------------------------------------------------------------------------------------