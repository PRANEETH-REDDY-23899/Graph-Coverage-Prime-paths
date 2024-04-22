
# Helper Functions

def extend_path(graph, path, start_node, end_node, visited=None):
        """
        Extend the given path from both ends to start_node and end_node.
        """
        if visited is None:
            visited = set()

        # Extend path to start_node
        while path[0] != start_node:
            current_node = path[0]
            # next_nodes = graph[current_node]
            # Check if the node has only one neighbor to avoid creating cycles
            next_nodes=[]
            for node, val in graph.items():
                if current_node in val:
                    next_nodes.append(node)
        
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
            next_nodes = graph[current_node]
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
    
def extending_paths(graph, prime_paths, start_node, end_node):
        prime_paths  = find_prime_paths(graph)

        """
        Extend prime paths to start from start_node and end at end_node.
        """

        if not graph:
            return ([], [])
        
        extended_paths = []
        un_extended_paths = []
        

        for path in prime_paths:
            extended_path = extend_path(graph, list(path), start_node, end_node)
            if extended_path[0] == start_node and extended_path[-1] == end_node:
                extended_paths.append(extended_path)
            else:
                un_extended_paths.append(extended_path)
        return (extended_paths, un_extended_paths)

def list_of_strings(extended_prime_test_paths, paths_list):
        for sub_list in extended_prime_test_paths:
            paths_list.append("".join(sub_list))
        return paths_list
    
def filter_unique_non_subpaths(extended_test_paths):
        string_paths = list_of_strings(extended_test_paths,[])
        duplicated =[]
        for i in range(len(string_paths)):
            for j in range(len(string_paths)):
                if i!=j:
                    if string_paths[i] in string_paths[j]:
                        duplicated.append(i)
                        break
                    
        updated_paths=[]
        for i in range(len(string_paths)):
            if i not in duplicated:
                path = [c for c in string_paths[i]]
                updated_paths.append(path)
        return updated_paths




# Node Coverage

def node_coverege_test_paths(graph,start_node,end_node):

    if not graph:
        return []
    if start_node not in graph or end_node not in graph:
        raise KeyError("Start or end node not in graph")

    def node_coverge(all_nodes,paths):
        covered_nodes= set()
        i=0
        node_coverage_test_paths=[]
        while i<len(paths):
            for node in paths[i][0]:
                covered_nodes.add(node)    
            node_coverage_test_paths.append(paths[i][0])
            if len(covered_nodes)==len(all_nodes):
                return node_coverage_test_paths
            i+=1 
        return []
    
    prime_paths = find_prime_paths(graph)
    
    (extended_prime_paths, un_extended_prime_test_paths) = extending_paths(graph, prime_paths, start_node, end_node)
    data =[]

    # print("Set paths")
    for path in extended_prime_paths:
        data.append((path,len(set(path)), len(path)))
    data_sorted = sorted(data, key=lambda x: (x[1], -x[2]), reverse=True)
    node_cover_paths= node_coverge(list(graph.keys()),data_sorted)

    return node_cover_paths, un_extended_prime_test_paths

# Edge Coverage

def edge_coverage_test_paths(graph, start_node, end_node):

    if not graph:
        return ([], [])
    
    if start_node not in graph or end_node not in graph:
        raise KeyError("Start or end node not in graph")
    

    edges=set()

    for key,val in graph.items():
        for node in val:
            edges.add((key,node))
    
    # print('Edges', edges)
            
    extended, unextended = extending_paths(graph,edges,start_node,end_node)

    unique_exteded = filter_unique_non_subpaths(extended)

    extended_set= set()
    for path in extended:
        extended_set.add(tuple(path))

    extended = [list(path) for path in extended_set]


    #exploring edges in the extended paths

    unique_extended_edges = set()
    unique_edge_covered_paths = []

    for path in extended:
        for i in range(len(path)-1):
            unique_extended_edges.add((path[i],path[i+1]))
        unique_edge_covered_paths.append(path)
        # check if edges are covered
        if unique_extended_edges == set(edges):
            break

    return (unique_edge_covered_paths, unextended)

    

# Prime Path Coverage
def find_prime_paths(graph):
    """
    Find the prime paths of a graph.
    """
    def is_prime_path(path):
        """
        Check if a path is a prime path.
        """
        # Check if the path is a cycle
        if len(path) >= 2 and path[0] == path[-1]:
            return True

        # Check if the path reaches both ends
        if reach_head(path) and can_extend_path_tail(path):
            return True

        return False

    def reach_head(path):
        """
        Check if the path can be extended at the head while remaining a simple path.
        """
        # Find nodes connected to the starting node of the path
        former_nodes = [n for n in graph if path[0] in graph[n]]

        # Check if any of these nodes can be added to the path without creating a cycle
        for node in former_nodes:
            if node not in path or node == path[-1]:
                return False
        return True

    def can_extend_path_tail(path):
        """
        Check if the path can be extended at the tail while remaining a simple path.
        """
        # Find nodes connected to the last node of the path
        connected_nodes = graph[path[-1]]

        # Check if any of these nodes can be added to the path without creating a cycle
        return all(node in path and node != path[0] for node in connected_nodes)

    def is_extendable(path):
        """
        Check if a path is extendable.
        """
        # If the path is a prime path or can be extended at the tail, it's not extendable
        return not (is_prime_path(path) or can_extend_path_tail(path))

    def find_simple_path(ex_paths, paths=[]):
        """
        Find the simple paths of a graph.
        """
        # Extend paths with prime paths
        paths.extend(filter(is_prime_path, ex_paths))

        # Filter extendable paths and generate new extendable paths
        ex_paths = filter(is_extendable, ex_paths)
        new_ex_paths = [path + (next_node,) for path in ex_paths for next_node in graph[path[-1]]
                        if next_node not in path or next_node == path[0]]

        # Recursively find simple paths
        if new_ex_paths:
            find_simple_path(new_ex_paths, paths)

        return paths

    ex_paths = [(node,) for node in graph.keys()]
    simple_paths = find_simple_path(ex_paths)
    prime_paths = sorted(simple_paths, key=lambda a: (len(a), a))
    return prime_paths




def prime_path_coverage_test_paths(graph,start_node,end_node):

    if not graph:
        return ([], [])
    
    if start_node not in graph or end_node not in graph:
        raise KeyError("Start or end node not in graph")
    
    def extend_path(graph, path, start_node, end_node, visited=None):
        """
        Extend the given path from both ends to start_node and end_node.
        """
        if visited is None:
            visited = set()

        # Extend path to start_node
        while path[0] != start_node:
            current_node = path[0]
            # next_nodes = graph[current_node]
            # Check if the node has only one neighbor to avoid creating cycles
            next_nodes=[]
            for node, val in graph.items():
                if current_node in val:
                    next_nodes.append(node)
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
            next_nodes = graph[current_node]
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
        un_extended_paths = []
        

        for path in prime_paths:
            extended_path = extend_path(graph, list(path), start_node, end_node)
            if extended_path[0] == start_node and extended_path[-1] == end_node:
                extended_paths.append(extended_path)
            else:
                un_extended_paths.append(extended_path)
        return (extended_paths, un_extended_paths)
    

    
    def list_of_strings(extended_prime_test_paths, paths_list):
        for sub_list in extended_prime_test_paths:
            paths_list.append("".join(sub_list))
        return paths_list
    
    def filter_unique_non_subpaths(string_paths):
        duplicated =[]
        for i in range(len(string_paths)):
            for j in range(len(string_paths)):
                if i!=j:
                    if string_paths[i] in string_paths[j]:
                        duplicated.append(i)
                        break
                    
        updated_paths=[]
        for i in range(len(string_paths)):
            if i not in duplicated:
                path = [c for c in string_paths[i]]
                updated_paths.append(path)
        return updated_paths
    
    prime_paths = find_prime_paths(graph)

    (extended_prime_test_paths, un_extended_prime_test_paths) = extend_prime_paths(graph, prime_paths, start_node, end_node)

    string_paths = list_of_strings(extended_prime_test_paths,[])

    unique_prime_coverage_test_paths = filter_unique_non_subpaths(string_paths)

    if extended_prime_test_paths and not unique_prime_coverage_test_paths:
        unique_exteden_paths = set()
        for path in extended_prime_test_paths:
            unique_exteden_paths.add(tuple(path))
        unique_prime_coverage_test_paths = [list(path) for path in unique_exteden_paths]
    
    return (unique_prime_coverage_test_paths, un_extended_prime_test_paths)



    


       
graph_input = {"A": ["B", "C"], "B": ["C", "A"], "C": ["B", "A"]}
graph= graph_input
start_node = "A"
end_node = "A"

# graph_input= {"A": ["B", "C"], "B": ["C", "A"], "C": []}
# graph = graph_input
# start_node = 'A'
# end_node = 'B'
# Nodes = list(graph_input.keys())
# print(Nodes)

# graph_input = {"A": ["B"], "B": ["C"], "C": ["D"], "D": ["A"]}
# graph = graph_input
# start_node = 'A'
# end_node = 'D'



# graph = {
#         'A': ['B', 'C'],
#         'B': ['C'],
#         'C': ['D'],
#         'D': []
#     }
# start_node = 'A'
# end_node = 'B'


prime_paths = find_prime_paths(graph)
print("\nPrime Paths:")
for path in prime_paths:
    print(list(path))
    
prime_test_paths, un_extended_prime_test_paths = prime_path_coverage_test_paths(graph,start_node,end_node)

print(" Prime test paths")
for path in prime_test_paths:
    print(path)

print('un_extended_prime_test_paths', un_extended_prime_test_paths)

(extended_prime_paths, un_extended_prime_test_paths) = extending_paths(graph, prime_paths, start_node, end_node)

node_coverage = node_coverege_test_paths(graph,start_node,end_node)



print('Node_Coverage path', node_coverage)


print('\n extend_prime_paths')
for path in extended_prime_paths:
    print(path)

print('edge_coverage')

edge_cover_path, un_extended = edge_coverage_test_paths(graph,start_node,end_node)

for path in edge_cover_path:
    print(path)

print('un covered')

print(un_extended)





