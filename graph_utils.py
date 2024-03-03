import streamlit as st
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to execute Depth-First Search (DFS)
def dfs(graph, start, end):
    visited = set()
    path = []

    def dfs_recursive(node):
        if node == end:
            path.append(node)
            return True
        if node not in visited:
            visited.add(node)
            path.append(node)
            for neighbor in graph[node]:
                if dfs_recursive(neighbor):
                    return True
            path.pop()
        return False

    dfs_recursive(start)
    return path  # Return the path

# Function to execute Breadth-First Search (BFS)
def bfs(graph, start, end):
    visited = set()
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == end:
            return path  # Return the path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

# Function to visualize DFS
def visualize_dfs(graph, start, end):
    dfs_path = dfs(graph, start, end)  # Get the DFS path
    visited = set()
    path = []

    fig, ax = plt.subplots()
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, ax=ax)

    def update(i):
        ax.clear()
        nx.draw(graph, pos, with_labels=True, ax=ax)
        if i < len(dfs_path):
            visited.add(dfs_path[i])
            path.append(dfs_path[i])
            nx.draw_networkx_nodes(graph, pos, nodelist=list(visited), node_color='r', ax=ax)
            nx.draw_networkx_edges(graph, pos, ax=ax)
            if i > 0:
                nx.draw_networkx_edges(graph, pos, edgelist=[(path[i-1], path[i])], edge_color='r', ax=ax)

    ani = animation.FuncAnimation(fig, update, frames=len(dfs_path)+1, repeat=False)
    st.pyplot(plt)

# Function to visualize BFS
def visualize_bfs(graph, start, end):
    bfs_path = bfs(graph, start, end)  # Get the BFS path
    visited = set()
    path = []

    fig, ax = plt.subplots()
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, ax=ax)

    def update(i):
        ax.clear()
        nx.draw(graph, pos, with_labels=True, ax=ax)
        if i < len(bfs_path):
            visited.add(bfs_path[i])
            path.append(bfs_path[i])
            nx.draw_networkx_nodes(graph, pos, nodelist=list(visited), node_color='r', ax=ax)
            nx.draw_networkx_edges(graph, pos, ax=ax)
            if i > 0:
                nx.draw_networkx_edges(graph, pos, edgelist=[(path[i-1], path[i])], edge_color='r', ax=ax)

    ani = animation.FuncAnimation(fig, update, frames=len(bfs_path)+1, repeat=False)
    st.pyplot(plt)


# Function to display the home page
# def display_home_page():
#     st.title("Graph Coverage Prime Paths")
#     st.write("Welcome to the Graph Coverage Prime Paths application!")
#     st.write("This application demonstrates graph algorithms and coverage criteria for test path generation.")


def display_graph_algorithms():
    st.header("Graph Algorithms")
    st.markdown("- **Graph algorithms are procedures or formulas for solving problems on graphs.**")
    st.markdown("- **Some common graph algorithms include:**")
    st.subheader("Depth-First Search (DFS)")
    st.markdown("To demonstrate DFS, please enter the graph and specify the start and end nodes.")
    # Input graph and starting/ending nodes for DFS
    graph_dfs = st.text_area("Enter the graph for DFS (format: {'node': ['neighbor1', 'neighbor2', ...]})", value="{'A': ['B', 'C'], 'B': ['D'], 'C': ['E'], 'D': ['F'], 'E': ['F'], 'F': []}", key="dfs_graph_input")
    start_node_dfs = st.text_input("Enter the starting node for DFS", value='A', key="dfs_start_node_input")
    end_node_dfs = st.text_input("Enter the ending node for DFS", value='F', key="dfs_end_node_input")
    if st.button("Run DFS"):
        st.write("Running DFS...")
        graph_dict = eval(graph_dfs)
        graph = nx.DiGraph(graph_dict)
        start_time = time.time()
        dfs_path = dfs(graph_dict, start_node_dfs, end_node_dfs)
        end_time = time.time()
        st.write("DFS Path:", dfs_path)
        st.write("Time taken:", round(end_time - start_time, 6), "seconds")
        visualize_dfs(graph, start_node_dfs, end_node_dfs)

    st.subheader("Breadth-First Search (BFS)")
    st.markdown("To demonstrate BFS, please enter the graph and specify the start and end nodes.")
    # Input graph and starting/ending nodes for BFS
    graph_bfs = st.text_area("Enter the graph for BFS (format: {'node': ['neighbor1', 'neighbor2', ...]})", value="{'A': ['B', 'C'], 'B': ['D'], 'C': ['E'], 'D': ['F'], 'E': ['F'], 'F': []}", key="bfs_graph_input")
    start_node_bfs = st.text_input("Enter the starting node for BFS", value='A', key="bfs_start_node_input")
    end_node_bfs = st.text_input("Enter the ending node for BFS", value='F', key="bfs_end_node_input")
    if st.button("Run BFS"):
        st.write("Running BFS...")
        graph_dict = eval(graph_bfs)
        graph = nx.DiGraph(graph_dict)
        start_time = time.time()
        bfs_path = bfs(graph_dict, start_node_bfs, end_node_bfs)
        end_time = time.time()
        st.write("BFS Path:", bfs_path)
        st.write("Time taken:", round(end_time - start_time, 6), "seconds")
        visualize_bfs(graph, start_node_bfs, end_node_bfs)

def display_coverage_criteria():
    st.header("Coverage Criteria")
    st.markdown("- **Node Coverage:** Node coverage aims to design a test path that reaches every node at least once.")
    st.markdown("- **Edge Coverage:** Edge coverage ensures that test paths reach every edge at least once.")
    st.markdown("- **Prime Path Coverage:** Prime path coverage focuses on simple paths with no loops that are not sub-paths of another prime path.")


def display_welcome_message():
    st.title("Graph Coverage Prime Paths")
    st.write("Graph coverage prime paths is a software tool that generates test paths to satisfy graph coverage test criteria.")
    st.write("Graphs are essential data structures for representing connections between various entities.")
    st.write("Some keywords related to graphs include nodes, edges, algorithms, etc.")
    st.write("Algorithms related to graph coverage include Depth-First Search (DFS) and Breadth-First Search (BFS).")
    st.write("Node coverage ensures reaching every node at least once, edge coverage ensures reaching every edge at least once, and prime path coverage focuses on simple paths with no loops.")

def display_graph_concepts():
    st.header("Graph Concepts")
    st.markdown("- **A graph is a mathematical structure consisting of nodes (vertices) and edges (connections). It is used to model pairwise relationships between objects.**")
    st.markdown("- **Types of Graphs:**")
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5b/6n-graf.svg", use_column_width=True)
    st.markdown("  - **Directed Graph (Digraph)**: A graph where edges have a direction.")
    st.markdown("  - **Undirected Graph**: A graph where edges have no direction.")
    st.markdown("  - **Weighted Graph**: A graph where edges have weights (e.g., distance, cost).")
    st.markdown("  - **Cyclic Graph**: A graph containing a cycle (i.e., a closed loop).")
    st.markdown("  - **Acyclic Graph**: A graph with no cycles.")
    st.markdown("  - **Connected Graph**: A graph where there is a path between every pair of vertices.")
    st.markdown("  - **Disconnected Graph**: A graph with at least two vertices that are not connected by a path.")



def display_home_page():
    display_welcome_message()
    st.markdown("---")
    display_graph_concepts()
    st.markdown("---")
    display_graph_algorithms()
    st.markdown("---")
    display_coverage_criteria()

display_home_page()
