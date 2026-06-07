"""
Prim's Minimum Spanning Tree (MST) Algorithm
===============================================
Dua implementasi algoritma Prim:
1. Min-Heap (Priority Queue) – O((V + E) log V)  ← direkomendasikan
2. Linear Search              – O(V²)             ← sederhana, cocok untuk graf kecil

Mendukung:
- Graf berbobot tak berarah
- Rekonstruksi pohon rentang minimum (MST)
- Visualisasi adjacency list & sisi-sisi MST
"""

import heapq
from collections import defaultdict
from math import inf


# ─────────────────────────────────────────────
# Kelas Graf (Tak Berarah)
# ─────────────────────────────────────────────

class Graph:
    def __init__(self):
        self.adj: dict[str, list[tuple[str, float]]] = defaultdict(list)
        self.nodes: set[str] = set()

    def add_edge(self, u: str, v: str, weight: float) -> None:
        self.nodes.update([u, v])
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))

    def add_node(self, node: str) -> None:
        self.nodes.add(node)

    def total_edges(self) -> int:
        return sum(len(nbrs) for nbrs in self.adj.values()) // 2

    def __str__(self) -> str:
        lines = ["Graf Tak Berarah:"]
        for node in sorted(self.nodes):
            neighbors = self.adj.get(node, [])
            conn = ", ".join(f"{v}({w})" for v, w in sorted(neighbors))
            lines.append(f"  {node} → [{conn}]")
        return "\n".join(lines)


# ─────────────────────────────────────────────
# 1. Prim dengan Min-Heap (Priority Queue)
# ─────────────────────────────────────────────

def prim_heap(graph: Graph, start: str) -> tuple[float, list[tuple[str, str, float]]]:
    """
    Prim's MST menggunakan min-heap.
    Kompleksitas: O((V + E) log V)

    Returns:
        (total_bobot, daftar_sisi_mst)
        daftar_sisi_mst : list of (u, v, weight)
    """
    in_mst = set()
    # Min-heap: (bobot, simpul_asal, simpul_tujuan)
    heap = [(0, start, None)]
    mst_edges = []
    total_weight = 0.0

    while heap and len(in_mst) < len(graph.nodes):
        w, u, parent = heapq.heappop(heap)

        if u in in_mst:
            continue
        in_mst.add(u)

        if parent is not None:
            mst_edges.append((parent, u, w))
            total_weight += w

        for v, weight in graph.adj.get(u, []):
            if v not in in_mst:
                heapq.heappush(heap, (weight, v, u))

    return total_weight, mst_edges


# ─────────────────────────────────────────────
# 2. Prim dengan Linear Search
# ─────────────────────────────────────────────

def prim_linear(graph: Graph, start: str) -> tuple[float, list[tuple[str, str, float]]]:
    """
    Prim's MST menggunakan linear search untuk menemukan sisi minimum.
    Kompleksitas: O(V²)

    Returns:
        (total_bobot, daftar_sisi_mst)
    """
    key   = {node: inf  for node in graph.nodes}
    parent= {node: None for node in graph.nodes}
    in_mst= {node: False for node in graph.nodes}

    key[start] = 0
    mst_edges   = []
    total_weight = 0.0

    for _ in range(len(graph.nodes)):
        # Pilih simpul dengan key terkecil yang belum masuk MST
        u = min((n for n in graph.nodes if not in_mst[n]), key=lambda n: key[n])
        in_mst[u] = True

        if parent[u] is not None:
            mst_edges.append((parent[u], u, key[u]))
            total_weight += key[u]

        for v, w in graph.adj.get(u, []):
            if not in_mst[v] and w < key[v]:
                key[v]    = w
                parent[v] = u

    return total_weight, mst_edges


# ─────────────────────────────────────────────
# Helper: cetak MST
# ─────────────────────────────────────────────

def print_mst(total: float, edges: list[tuple[str, str, float]], label: str = "") -> None:
    if label:
        print(f"\n  ► {label}")
    print(f"  {'Sisi':<22} {'Bobot':>7}")
    print(f"  {'─'*22} {'─'*7}")
    for u, v, w in sorted(edges, key=lambda e: (e[0], e[1])):
        print(f"  {u} ─── {v:<16} {w:>7.1f}")
    print(f"  {'─'*22} {'─'*7}")
    print(f"  {'Total Bobot MST':<22} {total:>7.1f}")
    print(f"  Jumlah Sisi MST : {len(edges)}")


# ─────────────────────────────────────────────
# Contoh penggunaan
# ─────────────────────────────────────────────

def demo_classic():
    print("\n╔══════════════════════════════════════════════════╗")
    print("║          PRIM – Contoh 1: Graf Klasik           ║")
    print("╚══════════════════════════════════════════════════╝")

    g = Graph()
    edges = [
        ("A", "B", 2), ("A", "C", 3), ("A", "D", 3),
        ("B", "C", 4), ("B", "E", 3),
        ("C", "D", 5), ("C", "E", 1), ("C", "F", 6),
        ("D", "F", 7),
        ("E", "F", 8),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    print(f"\n{g}")
    print(f"\n  Total simpul : {len(g.nodes)}  |  Total sisi : {g.total_edges()}")

    total_h, edges_h = prim_heap(g, "A")
    total_l, edges_l = prim_linear(g, "A")

    print_mst(total_h, edges_h, label="Min-Heap (Priority Queue)")
    print_mst(total_l, edges_l, label="Linear Search")


def demo_city():
    print("\n╔══════════════════════════════════════════════════╗")
    print("║     PRIM – Contoh 2: Jaringan Kabel Antar Kota  ║")
    print("╚══════════════════════════════════════════════════╝")
    print("  (Cari kabel terpendek untuk menghubungkan semua kota)")

    g = Graph()
    edges = [
        ("Jakarta",    "Bogor",      60),
        ("Jakarta",    "Bandung",   150),
        ("Jakarta",    "Cirebon",   280),
        ("Bogor",      "Sukabumi",   90),
        ("Bogor",      "Bandung",   120),
        ("Sukabumi",   "Cianjur",    50),
        ("Cianjur",    "Bandung",    60),
        ("Bandung",    "Cirebon",   130),
        ("Bandung",    "Yogyakarta",310),
        ("Cirebon",    "Semarang",  200),
        ("Semarang",   "Yogyakarta",130),
        ("Yogyakarta", "Surabaya",  330),
        ("Semarang",   "Surabaya",  400),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    print(f"\n{g}")
    print(f"\n  Total simpul : {len(g.nodes)}  |  Total sisi : {g.total_edges()}")

    total, mst_edges = prim_heap(g, "Jakarta")
    print_mst(total, mst_edges, label="MST – Jaringan Kabel Minimum (km)")

    all_edges_weight = sum(w for _, _, w in edges)
    print(f"\n  Total semua sisi     : {all_edges_weight} km")
    print(f"  Penghematan MST      : {all_edges_weight - total:.1f} km "
          f"({(all_edges_weight - total) / all_edges_weight * 100:.1f}%)")


def demo_network():
    print("\n╔══════════════════════════════════════════════════╗")
    print("║     PRIM – Contoh 3: Topologi Jaringan Komputer ║")
    print("╚══════════════════════════════════════════════════╝")
    print("  (Bobot = biaya pemasangan kabel, dalam jutaan rupiah)")

    g = Graph()
    edges = [
        ("Server",  "Switch1",  5),
        ("Server",  "Switch2",  8),
        ("Server",  "Router",  10),
        ("Switch1", "PC1",      3),
        ("Switch1", "PC2",      4),
        ("Switch1", "Switch2",  2),
        ("Switch2", "PC3",      3),
        ("Switch2", "PC4",      6),
        ("Switch2", "Router",   4),
        ("Router",  "PC5",      7),
        ("PC1",     "PC2",      1),
        ("PC3",     "PC4",      2),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    print(f"\n{g}")
    print(f"\n  Total simpul : {len(g.nodes)}  |  Total sisi : {g.total_edges()}")

    total, mst_edges = prim_heap(g, "Server")
    print_mst(total, mst_edges, label="MST – Topologi Minimum (juta Rp)")

    all_cost = sum(w for _, _, w in edges)
    print(f"\n  Biaya pasang semua kabel : Rp {all_cost} juta")
    print(f"  Biaya MST (minimum)      : Rp {total:.0f} juta")
    print(f"  Penghematan              : Rp {all_cost - total:.0f} juta")


def demo_disconnected():
    print("\n╔══════════════════════════════════════════════════╗")
    print("║   PRIM – Contoh 4: Graf Tidak Terhubung         ║")
    print("╚══════════════════════════════════════════════════╝")
    print("  (MST hanya mencakup komponen yang terhubung dengan start)")

    g = Graph()
    g.add_edge("A", "B", 3)
    g.add_edge("B", "C", 5)
    g.add_edge("A", "C", 4)
    g.add_edge("D", "E", 2)   # Komponen terpisah
    g.add_node("F")            # Simpul terisolasi

    print(f"\n{g}")
    print(f"\n  Total simpul : {len(g.nodes)}  |  Total sisi : {g.total_edges()}")

    total, mst_edges = prim_heap(g, "A")

    print(f"\n  ► MST dari simpul 'A':")
    print_mst(total, mst_edges)

    visited = {u for u, _, _ in mst_edges} | {v for _, v, _ in mst_edges} | {"A"}
    unreachable = g.nodes - visited
    if unreachable:
        print(f"\n  ⚠  Simpul tidak terjangkau dari 'A': {', '.join(sorted(unreachable))}")
        print(f"     (Graf tidak terhubung – MST tidak mencakup seluruh graf)")


def main():
    demo_classic()
    demo_city()
    demo_network()
    demo_disconnected()
    print()


if __name__ == "__main__":
    main()
