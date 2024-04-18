from collections import deque

def read_graph(graph_input, start_node, end_node):
    """
    Read a graph structure from the given input.
    """
    nodes = list(graph_input.keys())
    init_nodes = [start_node]
    end_nodes = [end_node]
    edges = {node: graph_input[node] for node in nodes}
    return {'nodes': nodes, 'init': init_nodes, 'end': end_nodes, 'edges': edges}


def print_graph(graph):
    """
    Print graph structure information.
    """
    print("Nodes:     ", graph['nodes'])
    print("InitNodes: ", graph['init'])
    print("EndNodes:  ", graph['end'])
    print("Edges:")
    for node, neighbors in graph['edges'].items():
        print(f"{node} to {neighbors}")


def is_prime_path(path, graph):
    """
    Check if a path is a prime path.
    """
    if len(path) >= 2 and path[0] == path[-1]:
        return True
    elif reach_head(path, graph) and reach_end(path, graph):
        return True
    else:
        return False


def reach_head(path, graph):
    """
    Check if the path can be extended at the head while remaining a simple path.
    """
    former_nodes = [n for n in graph['nodes'] if path[0] in graph['edges'][n]]
    for node in former_nodes:
        if node not in path or node == path[-1]:
            return False
    return True


def reach_end(path, graph):
    """
    Check if the path can be extended at the tail while remaining a simple path.
    """
    later_nodes = graph['edges'][path[-1]]
    for node in later_nodes:
        if node not in path or node == path[0]:
            return False
    return True


def extendable(path, graph):
    """
    Check if a path is extendable.
    """
    if is_prime_path(path, graph) or reach_end(path, graph):
        return False
    else:
        return True


def find_simple_path(graph, ex_paths, paths=[]):
    """
    Find the simple paths of a graph.
    """
    paths.extend(filter(lambda p: is_prime_path(p, graph), ex_paths))
    ex_paths = filter(lambda p: extendable(p, graph), ex_paths)
    new_ex_paths = []
    for path in ex_paths:
        for next_node in graph['edges'][path[-1]]:
            if next_node not in path or next_node == path[0]:
                new_ex_paths.append(path + (next_node,))
    if len(new_ex_paths) > 0:
        find_simple_path(graph, new_ex_paths, paths)


def find_prime_paths(graph):
    """
    Find the prime paths of a graph.
    """
    ex_paths = [(node,) for node in graph['nodes']]
    simple_paths = []
    find_simple_path(graph, ex_paths, simple_paths)
    prime_paths = sorted(simple_paths, key=lambda a: (len(a), a))
    return prime_paths


def usage():
    print("Finding The Prime Paths.")
    print("Please make sure the format of graph input is correct.")
    print("The results cannot be guaranteed if the format is incorrect.\n")
    print("Usage: python PrimePath.py GRAPH")
    print("       GRAPH The graph input dictionary")


def extend_path(graph, path, start_node, end_node, visited=None):
    """
    Extend the given path from both ends to start_node and end_node.
    """
    if visited is None:
        visited = set()

    # Extend path to start_node
    while path[0] != start_node:
        current_node = path[0]
        next_nodes = graph['edges'][current_node]
        # Check if the node has only one neighbor to avoid creating cycles
        if len(next_nodes) == 1:
            path.insert(0, next_nodes[0])
        else:
            found_extension = False
            # If there are multiple next nodes, explore all possible paths
            
            if start_node in next_nodes:
                path.insert(0,start_node)
                break
            for next_node in next_nodes:
                if next_node == start_node:
                    path.insert(0, next_node)
                    found_extension = True
                    break
                if next_node not in visited:
                    visited.add(next_node)
                    new_path = [next_node] + path
                    extended_path = extend_path(graph, new_path, start_node, end_node, visited.copy())
                    if extended_path[0] == start_node:
                        found_extension = True
                        path = extended_path
                        break
            if not found_extension:
                break

    # Extend path to end_node
    while path[-1] != end_node:
        current_node = path[-1]
        next_nodes = graph['edges'][current_node]
        # Check if the node has only one neighbor to avoid creating cycles
        if len(next_nodes) == 1:
            path.append(next_nodes[0])
        else:
            found_extension = False
            # If there are multiple next nodes, explore all possible paths
            if end_node in next_nodes:
                path.append(end_node)
                break
            for next_node in next_nodes:
                if next_node == end_node:
                    path.append(next_node)
                    found_extension = True
                    break
                if next_node not in visited:
                    visited.add(next_node)
                    new_path = path + [next_node]
                    extended_path = extend_path(graph, new_path, start_node, end_node, visited.copy())
                    if extended_path[-1] == end_node:
                        found_extension = True
                        path = extended_path
                        break
            if not found_extension:
                break

    return path


def extend_prime_paths(graph, prime_paths, start_node, end_node):
    """
    Extend prime paths to start from start_node and end at end_node.
    """
    extended_paths = []
    

    for path in prime_paths:
        extended_path = extend_path(graph, list(path), start_node, end_node)
        if extended_path[0] == start_node and extended_path[-1] == end_node:
            extended_paths.append(extended_path)
    return extended_paths


def list_of_strings(x, paths_list):
    for sub_list in x:
        paths_list.append("".join(sub_list))
    return paths_list

def filter_unique_non_subpaths(paths):
    duplicated =[]
    for i in range(len(paths)):
        for j in range(len(paths)):
            if i!=j:
                if paths[i] in paths[j]:
                    duplicated.append(i)
                    break
                
    updated_paths=[]
    for i in range(len(paths)):
        if i not in duplicated:
            path = [c for c in paths[i]]
            updated_paths.append(path)
    return updated_paths


def node_coverge(all_nodes,paths):
    covered_nodes= set()
    i=0
    node_coverage_test_paths=[]
    while i<len(paths):
        
        for node in paths[i]:
            covered_nodes.add(node)
            
        node_coverage_test_paths.append(paths[i])
        if len(covered_nodes)==len(all_nodes):
            return node_coverage_test_paths
        i+=1 
    return []

def get_edges(graph_input):
    
    edges=[]
    for key,val in graph_input.items():
        for node in val:
            edges.append([key,node])
    return edges

    
# Update __name__ == "__main__" block to generate test paths
if __name__ == "__main__":
    graph_input = {"A": ["B", "C"], "B": ["C", "A"], "C": ["B", "A"]}
    start_node = "A"
    end_node = "A"

    graph = read_graph(graph_input, start_node, end_node)
    print_graph(graph)
    prime_paths = find_prime_paths(graph)

    print("\nPrime Paths:")
    for path in prime_paths:
        print(list(path))
        

    # Example usage
    extended_prime_paths = extend_prime_paths(graph, prime_paths, start_node, end_node)
    
    print("\nExtended Prime Paths:")
    for path in extended_prime_paths:
        print(path)

    string_paths = list_of_strings(extended_prime_paths,[])

    unique_test_paths = filter_unique_non_subpaths(string_paths)

    print("\nUnique Test Paths:")
            
    # print('extend_path',extend_path(graph, ['C', 'B', 'A', 'C'], start_node, end_node))
            
        
    unique_path_decreasing_order = sorted(unique_test_paths, key=len, reverse=True)
# print(unique_path_decreasing_order)

    Nodes= set(graph.keys())

    node_cover_paths= node_coverge(Nodes,unique_path_decreasing_order)

    print('/n')

    print("Node Coverage test path",node_cover_paths)

    print('/n')

    unique_edges = get_edges(graph_input)

    print('unique_edges', get_edges(graph_input))

    edge_cover_paths = extend_prime_paths(graph,unique_edges,start_node,end_node)

    print('extended edges', extend_prime_paths(graph,unique_edges,start_node,end_node))

    all_edge_paths = set()

    for path in edge_cover_paths:
        all_edge_paths.add(tuple(path))
    print('all_edge_paths',all_edge_paths)