import streamlit as st
import networkx as nx
from graphviz import Digraph
import matplotlib.pyplot as plt
from io import BytesIO
import networkx as nx
from coverage_criteria import node_coverege_test_paths, edge_coverage_test_paths, prime_path_coverage_test_paths


# # Display the test path generation page
# display_test_path_page()
import streamlit as st
import networkx as nx
from graphviz import Digraph
import matplotlib.pyplot as plt


'''
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



def dfs(graph, current_node, visited, path, all_paths,end_node):
    path.append(current_node)

    visited.add(current_node)

    # Check if there are unvisited neighbors
    unvisited_neighbors = [neighbor for neighbor in graph.neighbors(current_node) if neighbor not in visited]

    if not unvisited_neighbors:
        # If there are no unvisited neighbors, this is a dead-end, add the current path to all_paths
        all_paths.append(path.copy())
    else:
        # Explore each unvisited neighbor
        for neighbor in unvisited_neighbors:
            dfs(graph, neighbor, visited.copy(), path, all_paths,end_node)

    path.pop()


def generate_prime_paths(graph, start_node, end_node):
    all_paths = []
    dfs(graph, start_node, set(), [], all_paths, end_node)
    prime_paths = []
    for path in all_paths:
        if len(set(path)) == len(path) + 1:  # For prime path coverage, allow starting node to be repeated
            is_prime = True
            for i in range(len(path)):
                for j in range(i+1, len(path)):
                    if path[i] in graph.neighbors(path[j]):
                        is_prime = False
                        break
                if not is_prime:
                    break
            if is_prime:
                prime_paths.append(path)
    return prime_paths
'''

def generate_test_paths(graph, start_node, end_node, coverage_criteria):

   
    
    if coverage_criteria == "Node Coverage":
        # visited = set()
        # all_paths = []
        # dfs(graph, start_node, visited, [], all_paths, end_node)
        # test_paths = all_paths
        node_coverage, un_covered_paths = node_coverege_test_paths(graph, start_node, end_node)

        return node_coverage, un_covered_paths


    elif coverage_criteria == "Edge Coverage":
        # if graph.has_node(start_node) and graph.has_node(end_node):
        #     test_paths = [p for p in nx.all_simple_paths(graph, start_node, end_node)]
        # else:
        #     print("Start or end node does not exist in the graph.")

        (edge_coverage, not_covered) = edge_coverage_test_paths(graph, start_node, end_node)

        for path in not_covered:
            if len(path)==2:
                return []
        return edge_coverage, not_covered
    
        
    elif coverage_criteria == "Prime Path Coverage":
        # prime_paths = generate_prime_paths(graph, start_node, end_node)
        # test_paths = prime_paths
        (prime_path_coverage, un_covered_paths) = prime_path_coverage_test_paths(graph, start_node, end_node)

        return prime_path_coverage, un_covered_paths

    else:
        print("Invalid coverage criteria selected.")

    



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

def display_input_graph(graph, start_node, end_node):
    G = nx.DiGraph(graph)
    pos = nx.circular_layout(G)  # positions for all nodes

    plt.figure(figsize=(8, 6))

    # Draw edges
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20)

    # Draw nodes
    node_labels = {}
    for node in G.nodes:
        if node == start_node:
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color="lightgreen", node_size=500, alpha=0.5)
            node_labels[node] = node
        elif node == end_node:
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color="red", node_size=500, alpha=0.5)
            node_labels[node] = node
        else:
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color="lightblue", node_size=500, alpha=0.5)
            node_labels[node] = node

    # Draw start node with inward horizontal arrow
    nx.draw_networkx_nodes(G, pos, nodelist=[start_node], node_color="lightgreen", node_size=500, alpha=0.5)
    plt.annotate("", xy=pos[start_node], xytext=(pos[start_node][0]-0.2, pos[start_node][1]), arrowprops=dict(arrowstyle="->", color='black'))

    # Draw end node with double circle
    nx.draw_networkx_nodes(G, pos, nodelist=[end_node], node_color="red", node_size=500, alpha=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=[end_node], node_color="red", node_size=1000, alpha=0.2, linewidths=2.0)

    # Draw labels
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, font_weight="bold")

    plt.title("Input Graph")
    plt.axis("off")

    # Save plot to BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

def display_test_path_page():
    st.header("Test Path Generation")

    # graph_input = st.text_area("Enter the graph (in adjacency list format):")
    graph_input = st.text_area("Enter the graph for DFS (format: {'node': ['neighbor1', 'neighbor2', ...]})", value="{'A': ['B', 'C'], 'B': ['D'], 'C': ['E'], 'D': ['F'], 'E': ['F'], 'F': []}")
    start_node = st.text_input("Enter the starting node: format: A", value= 'A')
    end_node = st.text_input("Enter the ending node: format: F ", value= 'F')

    if not graph_input or not start_node or not end_node:
        st.error("Please fill in all the required fields.")

    if st.button("Display Graph") and graph_input and start_node and end_node:
        if start_node in graph_input and end_node in graph_input:
            graph = eval(graph_input)
            st.image(display_input_graph(graph,start_node,end_node), caption="Input Graph", use_column_width=True)
        else:
            # Display the message in red color
            st.error("Please enter valid starting and ending nodes to display the graph./ Start Node {} and end Node {} should be present in the graph.".format(start_node,end_node))
            # st.write("Please enter valid starting and ending nodes to display the graph./ Start and end nodes should be present in the graph.")
    


        # graph = eval(graph_input)
        # graph_nx = nx.DiGraph()

        # # Add nodes
        # graph_nx.add_nodes_from(graph.keys())

        # # Add directed edges
        # for node, neighbors in graph.items():
        #     for neighbor in neighbors:
        #         graph_nx.add_edge(node, neighbor)

        # if not graph_input or not start_node or not end_node:
        #     st.error("Please fill in all the required fields.")
        # else:
        #     plt.figure(figsize=(10, 8))
        #     pos = nx.spring_layout(graph_nx, seed=42)  # Positions for all nodes

        #     # Draw edges with directions
        #     nx.draw_networkx_edges(graph_nx, pos, arrows=True)

        #     # Draw nodes
        #     nx.draw_networkx_nodes(graph_nx, pos, node_size=1000, node_color='skyblue', edgecolors='black')

        #     # Draw start node with inward arrow pointing left
        #     nx.draw_networkx_nodes(graph_nx, pos, nodelist=[start_node], node_size=1000, node_color='blue', edgecolors='black')
        #     start_x, start_y = pos[start_node]
        #     plt.arrow(start_x - 0.2, start_y, 0.1, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
        #     plt.text(start_x - 0.3, start_y, start_node, fontsize=12, ha='right', va='center')

        #     # Draw end node with double circle
        #     nx.draw_networkx_nodes(graph_nx, pos, nodelist=[end_node], node_size=1000, node_color='red', edgecolors='black')
        #     end_x, end_y = pos[end_node]
        #     circle = plt.Circle((end_x, end_y), 0.1, color='red', fill=False)
        #     plt.gca().add_patch(circle)
        #     plt.text(end_x + 0.1, end_y, end_node, fontsize=12, ha='left', va='center')

        #     # Draw node names
        #     for node, (x, y) in pos.items():
        #         plt.text(x, y + 0.1, node, fontsize=12, ha='center', va='center')

        #     plt.title("Graph with Start and End Nodes")
        #     plt.axis('off')
        #     st.pyplot()


    # coverage_criteria = st.radio("Select coverage criteria:", ["Node Coverage", "Edge Coverage", "Prime Path Coverage"])


    coverage_criteria = st.radio("Select coverage criteria:", ["Node Coverage", "Edge Coverage", "Prime Path Coverage"])

    

    if st.button("Generate Test Paths") and graph_input and start_node and end_node and coverage_criteria:
        # input_graph = [tuple(line.split()) for line in graph_input.split('\n') if line.strip()]
        graph = eval(graph_input)  # Convert string input to dictionary
        # print(graph)
        if not graph_input:
            st.error("Please enter a valid graph.")

        if not graph or not start_node or not end_node:
            st.error("Please fill in all the required fields.")

        if start_node not in graph or end_node not in graph:
            st.error("Start or end node does not exist in the graph.")
        
        else:
            # Convert graph to NetworkX DiGraph
            st.image(display_input_graph(graph,start_node,end_node), caption="Input Graph", use_column_width=True)
            graph_nx = nx.DiGraph(graph)

            test_paths, un_covered_paths = generate_test_paths(graph, start_node, end_node, coverage_criteria)

            All_Node = set(list(graph.keys()))

            set_of_test_paths = []
            for path in test_paths:
                set_of_test_paths.extend(path)
            # print(set(set_of_test_paths))
            # print(test_paths)

            check_final_node_paths=[]

            for path in test_paths:
                if path[-1] != end_node:
                    check_final_node_paths.append(path)
                    
            unvisited_nodes = All_Node - set(set_of_test_paths)

            if unvisited_nodes:
                st.error("The graph is invalid")
                st.error("Can not generate test path as some of the paths do not have final node at end {}".format(un_covered_paths))
                st.write("Can not generate a set of test paths to satisfy the {} coverage criteria".format(coverage_criteria))

            elif check_final_node_paths:
                st.error("Some paths do not contain the end node. The paths that do not contain the end node are: {}".format(check_final_node_paths))
                st.error("Can not generate a set of test paths to satisfy the {} coverage criteria".format(un_covered_paths))

            else:
                st.subheader("Generated Test Paths:")
                if test_paths:
                    st.write("\n\n".join([f"Test Path  {i+1}: {' -> '.join(path)}" for i, path in enumerate(test_paths)]))

                    # st.write ("set of test paths",set(set_of_test_paths))
                else:
                    st.write("No test paths generated.")
                st.write(" ")

                # Visualize the graph
                visualize_graph(graph_nx, start_node, end_node, test_paths)

# Display the test path generation page
display_test_path_page()
