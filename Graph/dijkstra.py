"""
Dijkstra's Shortest Path Algorithm
=====================================
Dua implementasi algoritma Dijkstra:
1. Min-Heap (Priority Queue) – O((V + E) log V)  ← direkomendasikan
2. Linear Search              – O(V²)             ← sederhana, cocok untuk graf kecil

Mendukung:
- Graf berbobot tak berarah maupun berarah
- Rekonstruksi jalur terpendek
- Visualisasi adjacency list & hasil
"""

import heapq
from collections import defaultdict
from math import inf


# ─────────────────────────────────────────────
# Kelas Graf
# ─────────────────────────────────────────────

class Graph:
    def __init__(self, directed: bool = False):
        """
        Args:
            directed: True = graf berarah, False = tak berarah
        """
        self.adj: dict[str, list[tuple[str, float]]] = defaultdict(list)
        self.directed = directed
        self.nodes: set[str] = set()

    def add_edge(self, u: str, v: str, weight: float) -> None:
        """Tambah sisi antara simpul u dan v dengan bobot weight."""
        self.nodes.update([u, v])
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def add_node(self, node: str) -> None:
        """Tambah simpul tanpa sisi."""
        self.nodes.add(node)

    def __str__(self) -> str:
        lines = [f"Graf {'Berarah' if self.directed else 'Tak Berarah'}:"]
        for node in sorted(self.nodes):
            neighbors = self.adj.get(node, [])
            conn = ", ".join(f"{v}({w})" for v, w in sorted(neighbors))
            lines.append(f"  {node} → [{conn}]")
        return "\n".join(lines)


# ─────────────────────────────────────────────
# 1. Dijkstra dengan Min-Heap (Priority Queue)
# ─────────────────────────────────────────────

def dijkstra_heap(graph: Graph, source: str) -> tuple[dict, dict]:
    """
    Dijkstra menggunakan min-heap (heapq).
    Kompleksitas: O((V + E) log V)

    Returns:
        dist  : dict simpul → jarak terpendek dari source
        prev  : dict simpul → simpul sebelumnya dalam jalur terpendek
    """
    dist = {node: inf for node in graph.nodes}
    prev = {node: None for node in graph.nodes}
    dist[source] = 0

    # Min-heap: (jarak, simpul)
    heap = [(0, source)]

    visited = set()

    while heap:
        d, u = heapq.heappop(heap)

        if u in visited:
            continue
        visited.add(u)

        for v, w in graph.adj.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))

    return dist, prev


# ─────────────────────────────────────────────
# 2. Dijkstra dengan Linear Search
# ─────────────────────────────────────────────

def dijkstra_linear(graph: Graph, source: str) -> tuple[dict, dict]:
    """
    Dijkstra menggunakan linear search untuk menemukan simpul minimum.
    Kompleksitas: O(V²)

    Returns:
        dist  : dict simpul → jarak terpendek dari source
        prev  : dict simpul → simpul sebelumnya dalam jalur terpendek
    """
    dist = {node: inf for node in graph.nodes}
    prev = {node: None for node in graph.nodes}
    dist[source] = 0

    unvisited = set(graph.nodes)

    while unvisited:
        # Pilih simpul dengan jarak terkecil dari unvisited
        u = min(unvisited, key=lambda node: dist[node])
        if dist[u] == inf:
            break  # Simpul sisa tidak terjangkau
        unvisited.remove(u)

        for v, w in graph.adj.get(u, []):
            if v in unvisited and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

    return dist, prev


# ─────────────────────────────────────────────
# Helper: rekonstruksi jalur
# ─────────────────────────────────────────────

def reconstruct_path(prev: dict, source: str, target: str) -> list[str]:
    """Rekonstruksi jalur dari source ke target menggunakan tabel prev."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    if path[0] != source:
        return []  # Tidak ada jalur
    return path


def format_path(path: list[str]) -> str:
    if not path:
        return "(tidak terjangkau)"
    return " → ".join(path)


# ─────────────────────────────────────────────
# Helper: cetak hasil
# ─────────────────────────────────────────────

def print_result(dist: dict, prev: dict, source: str, label: str = "") -> None:
    if label:
        print(f"\n  ► {label}")
    print(f"  {'Tujuan':<10} {'Jarak':<10} {'Jalur'}")
    print(f"  {'─'*8:<10} {'─'*8:<10} {'─'*30}")
    for node in sorted(dist):
        if node == source:
            continue
        d = dist[node]
        d_str = f"{d:.1f}" if d != inf else "∞"
        path = reconstruct_path(prev, source, node)
        print(f"  {node:<10} {d_str:<10} {format_path(path)}")


def print_single_path(dist: dict, prev: dict, source: str, target: str) -> None:
    d = dist.get(target, inf)
    path = reconstruct_path(prev, source, target)
    d_str = f"{d:.1f}" if d != inf else "∞"
    print(f"    {source} → {target}  :  jarak={d_str}  |  jalur: {format_path(path)}")


# ─────────────────────────────────────────────
# Contoh penggunaan
# ─────────────────────────────────────────────

def demo_basic():
    """Graf klasik 5 simpul."""
    print("\n╔══════════════════════════════════════════════════╗")
    print("║         DIJKSTRA – Contoh 1: Graf Klasik        ║")
    print("╚══════════════════════════════════════════════════╝")

    g = Graph(directed=False)
    edges = [
        ("A", "B", 4), ("A", "C", 2),
        ("B", "C", 5), ("B", "D", 10),
        ("C", "E", 3), ("E", "D", 4),
        ("D", "F", 11), ("E", "F", 7),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    print(f"\n{g}")

    source = "A"
    print(f"\n  Sumber: {source}")

    dist_h, prev_h = dijkstra_heap(g, source)
    print_result(dist_h, prev_h, source, label="Min-Heap (Priority Queue)")

    dist_l, prev_l = dijkstra_linear(g, source)
    print_result(dist_l, prev_l, source, label="Linear Search")


def demo_city():
    """Graf kota – jarak antar kota di Jawa."""
    print("\n╔══════════════════════════════════════════════════╗")
    print("║       DIJKSTRA – Contoh 2: Jarak Antar Kota    ║")
    print("╚══════════════════════════════════════════════════╝")

    g = Graph(directed=False)
    edges = [
        ("Jakarta",   "Bogor",     60),
        ("Jakarta",   "Bandung",   150),
        ("Bogor",     "Bandung",   120),
        ("Bogor",     "Sukabumi",  90),
        ("Bandung",   "Cirebon",   130),
        ("Bandung",   "Yogyakarta",310),
        ("Cirebon",   "Semarang",  200),
        ("Sukabumi",  "Cianjur",   50),
        ("Cianjur",   "Bandung",   60),
        ("Semarang",  "Yogyakarta",130),
        ("Yogyakarta","Surabaya",  330),
        ("Semarang",  "Surabaya",  400),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    print(f"\n{g}")

    source = "Jakarta"
    dist, prev = dijkstra_heap(g, source)

    print(f"\n  Sumber: {source}")
    print_result(dist, prev, source, label="Jarak Terpendek dari Jakarta (km)")

    # Jalur spesifik
    print(f"\n  ► Jalur Spesifik:")
    for target in ["Surabaya", "Yogyakarta", "Semarang"]:
        print_single_path(dist, prev, source, target)


def demo_directed():
    """Graf berarah – jalur satu arah."""
    print("\n╔══════════════════════════════════════════════════╗")
    print("║       DIJKSTRA – Contoh 3: Graf Berarah         ║")
    print("╚══════════════════════════════════════════════════╝")

    g = Graph(directed=True)
    edges = [
        ("S", "A", 10), ("S", "C", 3),
        ("A", "B", 2),  ("A", "C", 4),
        ("C", "A", 4),  ("C", "D", 8), ("C", "B", 15),
        ("D", "B", 5),  ("B", "T", 1), ("D", "T", 7),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    print(f"\n{g}")

    source = "S"
    dist, prev = dijkstra_heap(g, source)

    print(f"\n  Sumber: {source}")
    print_result(dist, prev, source, label="Jarak Terpendek (Graf Berarah)")

    print(f"\n  ► Jalur ke T:")
    print_single_path(dist, prev, source, "T")


def demo_unreachable():
    """Graf dengan simpul yang tidak terjangkau."""
    print("\n╔══════════════════════════════════════════════════╗")
    print("║   DIJKSTRA – Contoh 4: Simpul Tidak Terjangkau  ║")
    print("╚══════════════════════════════════════════════════╝")

    g = Graph(directed=False)
    g.add_edge("1", "2", 5)
    g.add_edge("2", "3", 3)
    g.add_edge("4", "5", 2)   # Komponen terpisah

    print(f"\n{g}")

    source = "1"
    dist, prev = dijkstra_heap(g, source)

    print(f"\n  Sumber: {source}")
    print_result(dist, prev, source, label="Hasil (∞ = tidak terjangkau)")


def main():
    demo_basic()
    demo_city()
    demo_directed()
    demo_unreachable()
    print()


if __name__ == "__main__":
    main()
