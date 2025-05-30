import networkx as nx
import networkx.algorithms.matching as nxmatch
import itertools
import matplotlib.pyplot as plt

def generate_cycle_graph(n):
    return nx.cycle_graph(n)

def is_independent_set(G, nodes):
    for u, v in itertools.combinations(nodes, 2):
        if G.has_edge(u, v):
            return False
    return True

def find_all_independent_sets(G):
    nodes = list(G.nodes)
    independent_sets = []
    for r in range(1, len(nodes) + 1):  
        for subset in itertools.combinations(nodes, r):
            if is_independent_set(G, subset):
                independent_sets.append(set(subset))
    return independent_sets

def find_all_matchings(G):
    edges = list(G.edges)
    matchings = []
    for r in range(1, len(edges) + 1):  # only matchings of size ≥ 1
        for subset in itertools.combinations(edges, r):
            if nxmatch.is_matching(G, subset):
                matchings.append(set(subset))
    return matchings

def get_vertices_from_edges(edges):
    return set(u for edge in edges for u in edge)

def is_vertex_edge_disjoint(G, V_i, E_i):
    for v in V_i:
        for u, w in E_i:
            if G.has_edge(v, u) or G.has_edge(v, w):
                return False
    return True

def find_valid_T_sets_equal_size(independent_sets, matchings, G):
    T_sets = []
    for i, V_i in enumerate(independent_sets):
        for j, E_i in enumerate(matchings):
            if len(V_i) == len(E_i) and len(V_i) > 0:
                edge_vertices = get_vertices_from_edges(E_i)
                if V_i.isdisjoint(edge_vertices) and is_vertex_edge_disjoint(G, V_i, E_i):
                    T_sets.append((i, j, V_i, E_i))
    return T_sets

def filter_T_sets_by_size_proximity(T_sets):
    T_sizes = [len(V_i) + len(E_i) for (_, _, V_i, E_i) in T_sets]
    filtered_T = []

    for idx, (i, j, V_i, E_i) in enumerate(T_sets):
        size_i = T_sizes[idx]
        if any(abs(size_i - size_j) <= 1 for k, size_j in enumerate(T_sizes) if k != idx):
            filtered_T.append((i, j, V_i, E_i))
    
    return filtered_T

def visualize_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.title("Path Graph")
    plt.show()

if __name__ == "__main__":
    n = int(input("Enter the number of nodes for the path graph: "))
    G = generate_cycle_graph(n)
    visualize_graph(G)

    independent_sets = find_all_independent_sets(G)
    matchings = find_all_matchings(G)

    print(f"\nIndependent sets V_i (|V_i| ≥ 1):")
    for i, V_i in enumerate(independent_sets):
        print(f"V_{i}: {sorted(V_i)}")

    print(f"\nMatchings E_i (|E_i| ≥ 1):")
    for j, E_i in enumerate(matchings):
        print(f"E_{j}: {sorted(E_i)}")

    T_sets_all = find_valid_T_sets_equal_size(independent_sets, matchings, G)
    T_sets = filter_T_sets_by_size_proximity(T_sets_all)

    print(f"\nFiltered T_i = V_i ∪ E_i where |V_i| = |E_i| ≥ 1, disjoint and non-incident ({len(T_sets)} total):")
    for idx, (i, j, V_i, E_i) in enumerate(T_sets):
        print(f"T_{idx}: V_{i} ∪ E_{j} = {{Vertices: {sorted(V_i)}, Edges: {sorted(E_i)}}}")
