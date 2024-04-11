import heapq

# iPair ==> Integer Pair
iPair = tuple
 
# This class represents a directed graph using
# adjacency list representation
class Graph:
    def __init__(self, V: int): # Constructor
        self.V = V
        self.adj = [[] for _ in range(V)]
 
    def addEdge(self, u: int, v: int, w: int):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def graphAdj(self):
        return self.adj
