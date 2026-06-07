"""
Knapsack Problem Solver
========================
Tiga pendekatan untuk menyelesaikan 0/1 Knapsack Problem:
1. Dynamic Programming (optimal, O(n*W))
2. Brute Force (eksak tapi lambat, O(2^n))
3. Greedy (cepat tapi tidak selalu optimal, O(n log n))
"""

from itertools import combinations


# ─────────────────────────────────────────────
# 1. Dynamic Programming
# ─────────────────────────────────────────────

def knapsack_dp(capacity: int, weights: list[int], values: list[int]) -> tuple[int, list[int]]:
    """
    Selesaikan 0/1 Knapsack dengan Dynamic Programming.

    Args:
        capacity : kapasitas maksimum knapsack
        weights  : daftar berat tiap item
        values   : daftar nilai tiap item

    Returns:
        (nilai_maksimum, indeks_item_yang_dipilih)
    """
    n = len(weights)
    # Buat tabel DP berukuran (n+1) x (capacity+1)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Tidak ambil item i
            dp[i][w] = dp[i - 1][w]
            # Ambil item i jika muat
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])

    # Lacak item yang dipilih
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
    selected.reverse()

    return dp[n][capacity], selected


# ─────────────────────────────────────────────
# 2. Brute Force
# ─────────────────────────────────────────────

def knapsack_brute_force(capacity: int, weights: list[int], values: list[int]) -> tuple[int, list[int]]:
    """
    Selesaikan 0/1 Knapsack dengan Brute Force (coba semua kombinasi).

    Kompleksitas: O(2^n) – hanya cocok untuk n kecil (<= 20).
    """
    n = len(weights)
    best_value = 0
    best_selected = []

    for r in range(n + 1):
        for combo in combinations(range(n), r):
            total_weight = sum(weights[i] for i in combo)
            total_value = sum(values[i] for i in combo)
            if total_weight <= capacity and total_value > best_value:
                best_value = total_value
                best_selected = list(combo)

    return best_value, best_selected


# ─────────────────────────────────────────────
# 3. Greedy (rasio nilai/berat)
# ─────────────────────────────────────────────

def knapsack_greedy(capacity: int, weights: list[int], values: list[int]) -> tuple[int, list[int]]:
    """
    Selesaikan 0/1 Knapsack dengan Greedy (urutkan berdasarkan rasio nilai/berat).

    Catatan: Tidak selalu menghasilkan solusi optimal untuk 0/1 Knapsack,
             tetapi sangat cepat – O(n log n).
    """
    n = len(weights)
    # Urutkan berdasarkan rasio nilai/berat secara menurun
    indices = sorted(range(n), key=lambda i: values[i] / weights[i] if weights[i] > 0 else 0, reverse=True)

    total_weight = 0
    total_value = 0
    selected = []

    for i in indices:
        if total_weight + weights[i] <= capacity:
            selected.append(i)
            total_weight += weights[i]
            total_value += values[i]

    selected.sort()
    return total_value, selected


# ─────────────────────────────────────────────
# Helper: cetak hasil
# ─────────────────────────────────────────────

def print_result(method: str, value: int, selected: list[int],
                 weights: list[int], values: list[int], items: list[str] = None) -> None:
    print(f"\n{'=' * 50}")
    print(f"  Metode : {method}")
    print(f"{'=' * 50}")
    print(f"  Nilai Maksimum : {value}")
    print(f"  Item yang dipilih:")
    total_w = 0
    for idx in selected:
        name = items[idx] if items else f"Item {idx}"
        print(f"    [{idx}] {name}  |  berat={weights[idx]}  |  nilai={values[idx]}")
        total_w += weights[idx]
    print(f"  Total Berat    : {total_w}")


# ─────────────────────────────────────────────
# Contoh penggunaan
# ─────────────────────────────────────────────

def main():
    print("\n╔══════════════════════════════════════════════╗")
    print("║         KNAPSACK PROBLEM SOLVER              ║")
    print("╚══════════════════════════════════════════════╝")

    # ── Contoh 1: Klasik ──────────────────────────
    print("\n▶ Contoh 1 – Knapsack Klasik")
    capacity = 50
    weights  = [10, 20, 30, 40]
    values   = [60, 100, 120, 140]
    items    = ["Laptop Kecil", "Kamera", "Sepatu", "Buku Tebal"]

    print(f"  Kapasitas : {capacity}")
    for i, (n, w, v) in enumerate(zip(items, weights, values)):
        print(f"  [{i}] {n:<15} berat={w}  nilai={v}")

    val_dp,  sel_dp  = knapsack_dp(capacity, weights, values)
    val_bf,  sel_bf  = knapsack_brute_force(capacity, weights, values)
    val_gr,  sel_gr  = knapsack_greedy(capacity, weights, values)

    print_result("Dynamic Programming", val_dp, sel_dp, weights, values, items)
    print_result("Brute Force",         val_bf, sel_bf, weights, values, items)
    print_result("Greedy",              val_gr, sel_gr, weights, values, items)

    # ── Contoh 2: Lebih banyak item ───────────────
    print("\n\n▶ Contoh 2 – Knapsack dengan 6 Item")
    capacity2 = 15
    weights2  = [1, 3, 4, 5, 2, 6]
    values2   = [1, 4, 5, 7, 3, 8]
    items2    = ["Pensil", "Buku Kecil", "Tempat Minum", "Payung", "Dompet", "Tablet"]

    print(f"  Kapasitas : {capacity2}")
    for i, (n, w, v) in enumerate(zip(items2, weights2, values2)):
        print(f"  [{i}] {n:<18} berat={w}  nilai={v}")

    val_dp2, sel_dp2 = knapsack_dp(capacity2, weights2, values2)
    val_bf2, sel_bf2 = knapsack_brute_force(capacity2, weights2, values2)
    val_gr2, sel_gr2 = knapsack_greedy(capacity2, weights2, values2)

    print_result("Dynamic Programming", val_dp2, sel_dp2, weights2, values2, items2)
    print_result("Brute Force",         val_bf2, sel_bf2, weights2, values2, items2)
    print_result("Greedy",              val_gr2, sel_gr2, weights2, values2, items2)

    print("\n")


if __name__ == "__main__":
    main()
