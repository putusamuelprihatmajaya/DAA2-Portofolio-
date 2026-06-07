"""
Knuth-Morris-Pratt (KMP) String Search Algorithm
===================================================
Tiga pendekatan pencarian string:
1. KMP          – O(n + m)  ← optimal, menggunakan failure function
2. Naive/Brute  – O(n * m)  ← sederhana, tanpa preprocessing
3. Built-in     – Python str.find() sebagai pembanding

Fitur:
- Cari semua kemunculan pattern dalam teks
- Visualisasi tabel failure function (LPS array)
- Highlight posisi hasil pencocokan
- Perbandingan jumlah perbandingan karakter antar metode
"""


# ─────────────────────────────────────────────
# 1. KMP – Failure Function (LPS Array)
# ─────────────────────────────────────────────

def build_lps(pattern: str) -> list[int]:
    """
    Bangun Longest Proper Prefix which is also Suffix (LPS) array.

    lps[i] = panjang prefix terpanjang dari pattern[:i+1]
             yang sekaligus merupakan suffix-nya.

    Contoh: pattern = "ABABC"
            lps     = [0, 0, 1, 2, 0]

    Kompleksitas: O(m)  (m = panjang pattern)
    """
    m = len(pattern)
    lps = [0] * m
    length = 0   # panjang prefix-suffix terpanjang saat ini
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # Coba prefix lebih pendek
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> tuple[list[int], int]:
    """
    Cari semua kemunculan pattern dalam text menggunakan algoritma KMP.

    Returns:
        (posisi_ditemukan, jumlah_perbandingan_karakter)
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return [], 0

    lps = build_lps(pattern)
    positions = []
    comparisons = 0

    i = 0   # indeks text
    j = 0   # indeks pattern

    while i < n:
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                positions.append(i - m)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return positions, comparisons


# ─────────────────────────────────────────────
# 2. Naive / Brute Force
# ─────────────────────────────────────────────

def naive_search(text: str, pattern: str) -> tuple[list[int], int]:
    """
    Cari semua kemunculan pattern dalam text secara naif.

    Kompleksitas: O(n * m)

    Returns:
        (posisi_ditemukan, jumlah_perbandingan_karakter)
    """
    n, m = len(text), len(pattern)
    positions = []
    comparisons = 0

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            comparisons += 1
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            positions.append(i)

    return positions, comparisons


# ─────────────────────────────────────────────
# 3. Built-in Python (pembanding)
# ─────────────────────────────────────────────

def builtin_search(text: str, pattern: str) -> list[int]:
    """Cari semua kemunculan menggunakan str.find() bawaan Python."""
    positions = []
    start = 0
    while True:
        idx = text.find(pattern, start)
        if idx == -1:
            break
        positions.append(idx)
        start = idx + 1
    return positions


# ─────────────────────────────────────────────
# Helper: Visualisasi LPS
# ─────────────────────────────────────────────

def print_lps(pattern: str) -> None:
    lps = build_lps(pattern)
    print(f"\n  LPS (Failure Function) untuk pattern \"{pattern}\":")
    print(f"  {'Indeks':<8}", end="")
    for i in range(len(pattern)):
        print(f"{i:>4}", end="")
    print()
    print(f"  {'Pattern':<8}", end="")
    for ch in pattern:
        print(f"{ch:>4}", end="")
    print()
    print(f"  {'LPS':<8}", end="")
    for v in lps:
        print(f"{v:>4}", end="")
    print()


# ─────────────────────────────────────────────
# Helper: Highlight kemunculan dalam teks
# ─────────────────────────────────────────────

def highlight(text: str, positions: list[int], pattern: str, max_len: int = 80) -> str:
    """Tandai semua kemunculan pattern dengan tanda [ ] dalam teks."""
    if not positions:
        return text[:max_len] + ("..." if len(text) > max_len else "")

    m = len(pattern)
    result = []
    prev = 0
    for pos in positions:
        result.append(text[prev:pos])
        result.append(f"[{text[pos:pos + m]}]")
        prev = pos + m
    result.append(text[prev:])
    out = "".join(result)
    return out[:max_len + len(positions) * 2] + ("..." if len(out) > max_len else "")


def print_positions(positions: list[int], text: str, pattern: str) -> None:
    if not positions:
        print("    (tidak ditemukan)")
        return
    for pos in positions:
        end = pos + len(pattern)
        ctx_start = max(0, pos - 5)
        ctx_end   = min(len(text), end + 5)
        ctx = text[ctx_start:ctx_end]
        rel = pos - ctx_start
        marked = ctx[:rel] + "[" + ctx[rel:rel + len(pattern)] + "]" + ctx[rel + len(pattern):]
        print(f"    posisi {pos:>4} : ...{marked}...")


# ─────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────

def demo(text: str, pattern: str, label: str,
         show_lps: bool = True, show_highlight: bool = True) -> None:
    print(f"\n{'═' * 56}")
    print(f"  {label}")
    print(f"{'═' * 56}")

    # Tampilkan teks (potong jika panjang)
    text_preview = text if len(text) <= 60 else text[:57] + "..."
    print(f"  Teks    : \"{text_preview}\"  (panjang={len(text)})")
    print(f"  Pattern : \"{pattern}\"  (panjang={len(pattern)})")

    # LPS Array
    if show_lps:
        print_lps(pattern)

    # KMP
    pos_kmp,   cmp_kmp   = kmp_search(text, pattern)
    pos_naive, cmp_naive = naive_search(text, pattern)
    pos_builtin           = builtin_search(text, pattern)

    # Validasi konsistensi
    assert sorted(pos_kmp) == sorted(pos_naive) == sorted(pos_builtin), \
        "Inkonsistensi hasil antara metode!"

    print(f"\n  ► Hasil Pencarian")
    print(f"  {'Metode':<28} {'Ditemukan':>10} {'Perbandingan':>13}")
    print(f"  {'─'*26:<28} {'─'*9:>10} {'─'*12:>13}")
    print(f"  {'KMP':<28} {len(pos_kmp):>10} {cmp_kmp:>13}")
    print(f"  {'Naive / Brute Force':<28} {len(pos_naive):>10} {cmp_naive:>13}")
    print(f"  {'Built-in (str.find)':<28} {len(pos_builtin):>10} {'─':>13}")

    if pos_kmp:
        print(f"\n  ► Posisi kemunculan ({len(pos_kmp)} kali):")
        print_positions(pos_kmp, text, pattern)

    if show_highlight and len(text) <= 120:
        print(f"\n  ► Highlight:")
        print(f"    {highlight(text, pos_kmp, pattern)}")

    # Efisiensi KMP vs Naive
    if cmp_naive > 0:
        saving = (1 - cmp_kmp / cmp_naive) * 100
        print(f"\n  ► KMP lebih efisien {saving:.1f}% dari Naive "
              f"({cmp_kmp} vs {cmp_naive} perbandingan)")


def main():
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║     KNUTH-MORRIS-PRATT (KMP) STRING SEARCH          ║")
    print("╚══════════════════════════════════════════════════════╝")

    demo(
        text    = "ABABDABACDABABCABAB",
        pattern = "ABABCABAB",
        label   = "Contoh 1 – Teks Klasik",
    )

    demo(
        text    = "AAAAABAAAAAABAAAB",
        pattern = "AAAB",
        label   = "Contoh 2 – Pattern Repetitif (KMP unggul)",
    )

    demo(
        text    = "belajar algoritma KMP sangat menyenangkan karena KMP sangat efisien",
        pattern = "KMP",
        label   = "Contoh 3 – Kalimat Bahasa Indonesia",
    )

    demo(
        text    = "ABCDEFGHIJ",
        pattern = "XYZ",
        label   = "Contoh 4 – Pattern Tidak Ditemukan",
    )

    demo(
        text    = "mississippi",
        pattern = "issi",
        label   = "Contoh 5 – Overlap (mississippi)",
    )

    demo(
        text    = "ABAB" * 500 + "ABAC",
        pattern = "ABAC",
        label   = "Contoh 6 – Teks Panjang (2004 karakter)",
        show_lps       = True,
        show_highlight = False,
    )

    demo(
        text    = "to be or not to be that is the question whether to be",
        pattern = "to be",
        label   = "Contoh 7 – Multi Kemunculan",
    )

    print(f"\n{'═' * 56}\n")


if __name__ == "__main__":
    main()
