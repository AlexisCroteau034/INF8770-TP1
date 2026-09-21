# ==============================================================================
# Bibliothèque d'Algorithmes Fondamentaux et Structures de Données en Python
# ==============================================================================

import math
from typing import List, Dict, Optional, Tuple

class BinarySearchTree:
    """Arbre binaire de recherche ordonné."""
    def __init__(self, key: int, value: str):
        self.key = key
        self.value = value
        self.left: Optional['BinarySearchTree'] = None
        self.right: Optional['BinarySearchTree'] = None

    def insert(self, key: int, value: str):
        if key < self.key:
            if self.left is None:
                self.left = BinarySearchTree(key, value)
            else:
                self.left.insert(key, value)
        elif key > self.key:
            if self.right is None:
                self.right = BinarySearchTree(key, value)
            else:
                self.right.insert(key, value)
        else:
            self.value = value

    def search(self, key: int) -> Optional[str]:
        if key == self.key:
            return self.value
        elif key < self.key and self.left:
            return self.left.search(key)
        elif key > self.key and self.right:
            return self.right.search(key)
        return None

class GraphAdjacencyList:
    """Graphe oriente pondere represente par liste d adjacence."""
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.adj: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(num_vertices)}

    def add_edge(self, u: int, v: int, weight: float = 1.0):
        self.adj[u].append((v, weight))

    def dijkstra(self, source: int) -> Dict[int, float]:
        dist = {i: float('inf') for i in range(self.num_vertices)}
        dist[source] = 0.0
        visited = set()

        while len(visited) < self.num_vertices:
            u = None
            min_d = float('inf')
            for node in range(self.num_vertices):
                if node not in visited and dist[node] < min_d:
                    min_d = dist[node]
                    u = node

            if u is None:
                break

            visited.add(u)
            for v, weight in self.adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight

        return dist

def quick_sort(arr: List[int]) -> List[int]:
    """Tri rapide recursif avec pivot median."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def binary_search(arr: List[int], target: int) -> int:
    """Recherche dichotomique dans un tableau trie."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

class BoundedQueue:
    """File circulaire a capacite bornee."""
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.data = [None] * capacity
        self.head = 0
        self.tail = 0
        self.count = 0

    def enqueue(self, item) -> bool:
        if self.count == self.capacity:
            return False
        self.data[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        self.count += 1
        return True

    def dequeue(self):
        if self.count == 0:
            return None
        item = self.data[self.head]
        self.data[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.count -= 1
        return item
