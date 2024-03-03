import streamlit as st
import networkx as nx
from graphviz import Digraph

def dfs(graph, node, visited, path, all_paths, end_node):
    visited.add(node)
    path.append(node)

    if node == end_node:
        all_paths.append(path.copy())
    else:
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(graph, neighbor, visited, path, all_paths, end_node)

    visited.remove(node)
    path.pop()

def generate_test_paths(graph, start_node, end_node, coverage_criteria):
    test_paths = []
    
    if coverage_criteria == "Node Coverage":
        visited = set()
        all_paths = []
        dfs(graph, start_node, visited, [], all_paths, end_node)
        test_paths = all_paths
    elif coverage_criteria == "Edge Coverage":
        if graph.has_node(start_node) and graph.has_node(end_node):
            test_paths = [p for p in nx.all_simple_paths(graph, start_node, end_node)]
        else:
            st.error("Start or end node does not exist in the graph.")
    else:
        st.error("Invalid coverage criteria selected.")

    return test_paths

def visualize_graph(graph, start_node, end_node, test_paths):
    dot = Digraph()

    for edge in graph.edges():
        dot.edge(*edge)

    dot.node(start_node, shape='circle', style='filled', color='blue')
    dot.node(end_node, shape='doublecircle', style='filled', color='red')

    colors = ['green', 'orange', 'purple', 'cyan', 'pink']
    for i, path in enumerate(test_paths):
        for j in range(len(path) - 1):
            if j == 0 and len(path) > 1:
                dot.edge(start_node, path[j+1], color=colors[i % len(colors)], penwidth='2', arrowhead='vee')
            else:
                dot.edge(path[j], path[j+1], color=colors[i % len(colors)], penwidth='2')

    st.subheader("Visuals and Notations:")
    st.write("""
        - The blue node represents the starting node.
        - The red node represents the ending node.
        - The colored edges represent different test paths.
        - An arrow indicates the direction of traversal starting from the blue node.
    """)

    st.graphviz_chart(dot.source)

def display_test_path_page():
    st.header("Test Path Generation")

    graph_input = st.text_area("Enter the graph (in adjacency list format):")
    start_node = st.text_input("Enter the starting node:")
    end_node = st.text_input("Enter the ending node:")

    coverage_criteria = st.radio("Select coverage criteria:", ["Node Coverage", "Edge Coverage"])

    if st.button("Generate Test Paths"):
        input_graph = [tuple(line.split()) for line in graph_input.split('\n') if line.strip()]
        graph = nx.DiGraph(input_graph)

        if not graph_input or not start_node or not end_node:
            st.error("Please fill in all the required fields.")
        else:
            test_paths = generate_test_paths(graph, start_node, end_node, coverage_criteria)
            st.subheader("Generated Test Paths:")
            if test_paths:
                st.write("\n".join([f"Test Path {i+1}: {path}" for i, path in enumerate(test_paths)]))
            else:
                st.write("No test paths generated.")
            st.write("")  # Add a space for better visualization

            # Visualize the graph
            visualize_graph(graph, start_node, end_node, test_paths)

# Display the test path generation page
display_test_path_page()
