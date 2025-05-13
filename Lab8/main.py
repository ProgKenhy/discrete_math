from collections import defaultdict
import random

class Graph:
    def __init__(self, graph):
        self.graph = graph  # Остаточная пропускная способность
        self.original_graph = [row[:] for row in graph]  # Сохраняем исходные пропускные способности
        self.ROW = len(graph)

    def DFS(self, s, visited):
        stack = [s]
        visited[s] = True

        while stack:
            u = stack.pop()
            for ind, val in enumerate(self.graph[u]):
                if not visited[ind] and val > 0:
                    stack.append(ind)
                    visited[ind] = True

    def FordFulkerson(self, source, sink):
        parent = [-1] * (self.ROW)
        max_flow = 0
        paths = []

        while self.DFS_for_path(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            path = []

            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                path.append(s)
                s = parent[s]

            path.append(source)
            path.reverse()
            paths.append((path, path_flow))

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow, paths

    def DFS_for_path(self, s, t, parent):
        visited = [False] * (self.ROW)
        stack = [s]
        visited[s] = True

        while stack:
            u = stack.pop()
            for ind, val in enumerate(self.graph[u]):
                if not visited[ind] and val > 0:
                    stack.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return visited[t]

    def find_min_cut(self, source):
        visited = [False] * (self.ROW)
        self.DFS(source, visited)

        min_cut_edges = []
        for i in range(self.ROW):
            for j in range(self.ROW):
                if visited[i] and not visited[j] and self.original_graph[i][j] > 0:
                    min_cut_edges.append((i, j))

        return min_cut_edges

def create_graph(edges, nodes):
    graph = [[0] * len(nodes) for _ in range(len(nodes))]
    node_index = {node: i for i, node in enumerate(nodes)}
    edge_capacities = {}

    for u, v, w in edges:
        graph[node_index[u]][node_index[v]] = w
        edge_capacities[(u, v)] = w

    return graph, node_index, edge_capacities

edges = [
    ('A', 'B', 5), ('A', 'C', 9), ('A', 'I', 4), ('B', 'C', 2),
    ('B', 'G', 2), ('B', 'I', 2), ('D', 'C', 2), ('E', 'D', 7),
    ('F', 'C', 2), ('F', 'D', 7), ('F', 'E', 7), ('G', 'C', 7),
    ('G', 'D', 3), ('G', 'E', 3), ('G', 'F', 3), ('H', 'C', 7),
    ('H', 'G', 7), ('H', 'F', 7), ('I', 'H', 7), ('I', 'G', 2),
]

nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

# Оригинальные пропускные способности
print("Исходные пропускные способности рёбер:")
for u, v, w in edges:
    print(f"{u} -> {v}: {w}")

graph, node_index, edge_capacities = create_graph(edges, nodes)
g = Graph(graph)

source = node_index['A']
sink = node_index['C']

max_flow, paths = g.FordFulkerson(source, sink)
print("\nМаксимальный поток: %d" % max_flow)
print("Пути и их вклад в поток:")
for path, flow in paths:
    print(f"Путь: {' -> '.join(nodes[node] for node in path)}, Поток: {flow}")

min_cut_edges = g.find_min_cut(source)
print("\nМинимальный разрез:")
for u, v in min_cut_edges:
    print(f"{nodes[u]} -> {nodes[v]} (Исходная пропускная способность: {edge_capacities[(nodes[u], nodes[v])]})")

# Случайные пропускные способности
random_edges = [(u, v, random.randint(100, 1000)) for u, v, w in edges]
print("\nСлучайные пропускные способности рёбер:")
for u, v, w in random_edges:
    print(f"{u} -> {v}: {w}")

random_graph, _, random_edge_capacities = create_graph(random_edges, nodes)
g_random = Graph(random_graph)


max_flow_random, paths_random = g_random.FordFulkerson(source, sink)
print("\nМаксимальный поток с случайными пропускными способностями: %d" % max_flow_random)
print("Пути и их вклад в поток:")
for path, flow in paths_random:
    print(f"Путь: {' -> '.join(nodes[node] for node in path)}, Поток: {flow}")

min_cut_edges_random = g_random.find_min_cut(source)
print("\nМинимальный разрез для случайных пропускных способностей:")
for u, v in min_cut_edges_random:
    print(f"{nodes[u]} -> {nodes[v]} (Случайная пропускная способность: {random_edge_capacities[(nodes[u], nodes[v])]})")
