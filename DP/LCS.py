"""
Longest Common Subsequence (LCS)
==================================
Tiga pendekatan untuk menyelesaikan LCS:
1. Dynamic Programming    – O(m*n) waktu, O(m*n) ruang
2. Rekursi + Memoization  – O(m*n) waktu, top-down
3. Rekursi Murni          – O(2^(m+n)) waktu, tanpa cache (demo saja)
"""

from functools import lru_cache


# ─────────────────────────────────────────────
# 1. Dynamic Programming (bottom-up)
# ─────────────────────────────────────────────

def lcs_dp(s1: str, s2: str) -> tuple[int, str]:
    """
    Hitung panjang LCS dan kembalikan salah satu subsequence-nya
    menggunakan Dynamic Programming (bottom-up).

    Returns:
        (panjang_lcs, string_lcs)
    """
    m, n = len(s1), len(s2)
    # Tabel DP: dp[i][j] = panjang LCS dari s1[:i] dan s2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Rekonstruksi string LCS
    lcs_str = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs_str.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcs_str.reverse()

    return dp[m][n], "".join(lcs_str)


def print_dp_table(s1: str, s2: str) -> None:
    """Cetak tabel DP untuk visualisasi."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Header
    header = "      " + "  ".join(f" {c}" for c in s2)
    print(f"\n  Tabel DP:")
    print(f"        {'   '.join([' '] + list(s2))}")
    print(f"      {'─' * (len(s2) * 4 + 2)}")
    for i in range(m + 1):
        label = " " if i == 0 else s1[i - 1]
        row = "  ".join(str(dp[i][j]) for j in range(n + 1))
        print(f"    {label} │ {row}")


# ─────────────────────────────────────────────
# 2. Rekursi + Memoization (top-down)
# ─────────────────────────────────────────────

def lcs_memo(s1: str, s2: str) -> tuple[int, str]:
    """
    Hitung LCS dengan rekursi + memoization (top-down DP).
    """
    @lru_cache(maxsize=None)
    def helper(i: int, j: int) -> str:
        if i == 0 or j == 0:
            return ""
        if s1[i - 1] == s2[j - 1]:
            return helper(i - 1, j - 1) + s1[i - 1]
        left = helper(i - 1, j)
        right = helper(i, j - 1)
        return left if len(left) >= len(right) else right

    result = helper(len(s1), len(s2))
    return len(result), result


# ─────────────────────────────────────────────
# 3. Rekursi Murni (tanpa cache)
# ─────────────────────────────────────────────

def lcs_recursive(s1: str, s2: str, i: int = None, j: int = None) -> int:
    """
    Hitung PANJANG LCS secara rekursif murni (tanpa memoization).
    Hanya untuk demonstrasi – sangat lambat untuk input besar.
    """
    if i is None:
        i = len(s1)
    if j is None:
        j = len(s2)

    if i == 0 or j == 0:
        return 0
    if s1[i - 1] == s2[j - 1]:
        return 1 + lcs_recursive(s1, s2, i - 1, j - 1)
    return max(lcs_recursive(s1, s2, i - 1, j), lcs_recursive(s1, s2, i, j - 1))


# ─────────────────────────────────────────────
# Helper: highlight karakter yang cocok
# ─────────────────────────────────────────────

def highlight_lcs(s: str, lcs_str: str) -> str:
    """Tandai posisi karakter LCS dalam string s dengan tanda [ ]."""
    result = []
    lcs_idx = 0
    for ch in s:
        if lcs_idx < len(lcs_str) and ch == lcs_str[lcs_idx]:
            result.append(f"[{ch}]")
            lcs_idx += 1
        else:
            result.append(ch)
    return "".join(result)


# ─────────────────────────────────────────────
# Contoh penggunaan
# ─────────────────────────────────────────────

def demo(s1: str, s2: str, label: str = "") -> None:
    print(f"\n{'═' * 52}")
    if label:
        print(f"  {label}")
    print(f"{'═' * 52}")
    print(f"  S1 : \"{s1}\"")
    print(f"  S2 : \"{s2}\"")

    # DP
    length_dp, lcs_str = lcs_dp(s1, s2)
    print(f"\n  ► Dynamic Programming")
    print(f"    Panjang LCS : {length_dp}")
    print(f"    LCS         : \"{lcs_str}\"")
    print(f"    S1 highlight: {highlight_lcs(s1, lcs_str)}")
    print(f"    S2 highlight: {highlight_lcs(s2, lcs_str)}")

    # Tampilkan tabel DP hanya jika string tidak terlalu panjang
    if len(s1) <= 10 and len(s2) <= 10:
        print_dp_table(s1, s2)

    # Memoization
    length_memo, lcs_memo_str = lcs_memo(s1, s2)
    print(f"\n  ► Rekursi + Memoization")
    print(f"    Panjang LCS : {length_memo}")
    print(f"    LCS         : \"{lcs_memo_str}\"")

    # Rekursi murni (hanya untuk string pendek)
    if len(s1) <= 15 and len(s2) <= 15:
        length_rec = lcs_recursive(s1, s2)
        print(f"\n  ► Rekursi Murni")
        print(f"    Panjang LCS : {length_rec}")
    else:
        print(f"\n  ► Rekursi Murni  →  dilewati (string terlalu panjang)")


def main():
    print("\n╔══════════════════════════════════════════════════╗")
    print("║       LONGEST COMMON SUBSEQUENCE (LCS)          ║")
    print("╚══════════════════════════════════════════════════╝")

    demo("ABCBDAB", "BDCAB",
         label="Contoh 1 – Klasik")

    demo("AGGTAB", "GXTXAYB",
         label="Contoh 2 – Acak")

    demo("ABCDEF", "ACBCF",
         label="Contoh 3 – Sebagian sama")

    demo("MZJAWXU", "XMJYAUZ",
         label="Contoh 4 – Dua string berbeda")

    demo("", "HELLO",
         label="Contoh 5 – String kosong")

    demo("SAMA", "SAMA",
         label="Contoh 6 – String identik")

    # Contoh string panjang (rekursi murni dilewati)
    demo("ABCDEFGHIJKLMNOPQRST", "AEIOUABCDEFG",
         label="Contoh 7 – String panjang")

    print(f"\n{'═' * 52}\n")


if __name__ == "__main__":
    main()
