"""
Huffman Coding – Kompresi Data
================================
Implementasi lengkap algoritma Huffman:
1. Hitung frekuensi karakter
2. Bangun pohon Huffman dengan min-heap
3. Generate kode Huffman (prefix-free codes)
4. Encode string → bit string
5. Decode bit string → string asal
6. Hitung rasio kompresi

Kompleksitas: O(n log n) untuk membangun pohon
"""

import heapq
from dataclasses import dataclass, field
from typing import Optional


# ─────────────────────────────────────────────
# Node Pohon Huffman
# ─────────────────────────────────────────────

@dataclass(order=False)
class HuffmanNode:
    freq: int
    char: Optional[str] = None          # None untuk node internal
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

    # Perbandingan hanya berdasarkan frekuensi (untuk heapq)
    def __lt__(self, other: "HuffmanNode") -> bool:
        if self.freq != other.freq:
            return self.freq < other.freq
        # Tie-break: char lebih kecil duluan (konsistensi)
        sc = self.char or ""
        oc = other.char or ""
        return sc < oc

    def is_leaf(self) -> bool:
        return self.char is not None


# ─────────────────────────────────────────────
# Kelas Utama HuffmanCoding
# ─────────────────────────────────────────────

class HuffmanCoding:
    def __init__(self):
        self.root: Optional[HuffmanNode] = None
        self.codes: dict[str, str] = {}          # char → kode biner
        self.reverse: dict[str, str] = {}        # kode biner → char

    # ── Langkah 1: Hitung frekuensi ──────────

    @staticmethod
    def frequency(text: str) -> dict[str, int]:
        freq = {}
        for ch in text:
            freq[ch] = freq.get(ch, 0) + 1
        return freq

    # ── Langkah 2: Bangun pohon Huffman ──────

    def build_tree(self, freq: dict[str, int]) -> HuffmanNode:
        heap = [HuffmanNode(f, ch) for ch, f in freq.items()]
        heapq.heapify(heap)

        # Kasus khusus: hanya satu karakter unik
        if len(heap) == 1:
            only = heapq.heappop(heap)
            root = HuffmanNode(only.freq, left=only)
            heapq.heappush(heap, root)

        while len(heap) > 1:
            left  = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(
                freq  = left.freq + right.freq,
                left  = left,
                right = right,
            )
            heapq.heappush(heap, merged)

        self.root = heap[0]
        return self.root

    # ── Langkah 3: Generate kode ─────────────

    def _generate_codes(self, node: Optional[HuffmanNode], code: str) -> None:
        if node is None:
            return
        if node.is_leaf():
            self.codes[node.char] = code or "0"   # single-char edge case
            self.reverse[code or "0"] = node.char
            return
        self._generate_codes(node.left,  code + "0")
        self._generate_codes(node.right, code + "1")

    def generate_codes(self) -> dict[str, str]:
        self.codes.clear()
        self.reverse.clear()
        self._generate_codes(self.root, "")
        return self.codes

    # ── Langkah 4: Encode ────────────────────

    def encode(self, text: str) -> str:
        return "".join(self.codes[ch] for ch in text)

    # ── Langkah 5: Decode ────────────────────

    def decode(self, bits: str) -> str:
        result = []
        node   = self.root
        for bit in bits:
            node = node.left if bit == "0" else node.right
            if node.is_leaf():
                result.append(node.char)
                node = self.root
        return "".join(result)

    # ── Pipeline lengkap ─────────────────────

    def compress(self, text: str) -> tuple[str, dict[str, str]]:
        """Compress text → (encoded_bits, codes_table)."""
        freq = self.frequency(text)
        self.build_tree(freq)
        self.generate_codes()
        encoded = self.encode(text)
        return encoded, self.codes

    def decompress(self, bits: str) -> str:
        """Decompress encoded_bits → original text."""
        return self.decode(bits)


# ─────────────────────────────────────────────
# Visualisasi Pohon (ASCII)
# ─────────────────────────────────────────────

def print_tree(node: Optional[HuffmanNode], prefix: str = "", is_left: bool = True) -> None:
    if node is None:
        return
    connector = "├── " if is_left else "└── "
    if node.is_leaf():
        label = f"'{node.char}' ({node.freq})"
    else:
        label = f"[{node.freq}]"
    print(f"  {prefix}{connector}{label}")
    extension = "│   " if is_left else "    "
    print_tree(node.left,  prefix + extension, True)
    print_tree(node.right, prefix + extension, False)


# ─────────────────────────────────────────────
# Helper: statistik kompresi
# ─────────────────────────────────────────────

def compression_stats(text: str, encoded: str, codes: dict[str, str]) -> None:
    freq = HuffmanCoding.frequency(text)
    original_bits  = len(text) * 8                        # ASCII 8-bit
    compressed_bits = len(encoded)
    ratio = (1 - compressed_bits / original_bits) * 100 if original_bits else 0

    # Weighted average code length
    total_chars = len(text)
    avg_len = sum(freq[ch] * len(codes[ch]) for ch in freq) / total_chars if total_chars else 0

    print(f"\n  {'─'*48}")
    print(f"  {'Statistik Kompresi':^48}")
    print(f"  {'─'*48}")
    print(f"  {'Panjang teks asal':<30} {len(text):>8} karakter")
    print(f"  {'Ukuran asal (ASCII 8-bit)':<30} {original_bits:>8} bit")
    print(f"  {'Ukuran terkompresi':<30} {compressed_bits:>8} bit")
    print(f"  {'Rasio kompresi':<30} {ratio:>7.1f}%")
    print(f"  {'Rata-rata panjang kode':<30} {avg_len:>7.2f} bit/char")
    print(f"  {'─'*48}")


def print_codes(codes: dict[str, str], freq: dict[str, int]) -> None:
    print(f"\n  {'Karakter':<12} {'Frekuensi':>10} {'Kode Huffman':>14} {'Panjang':>8}")
    print(f"  {'─'*10:<12} {'─'*9:>10} {'─'*12:>14} {'─'*7:>8}")
    for ch in sorted(codes, key=lambda c: freq.get(c, 0), reverse=True):
        display = repr(ch) if ch in (' ', '\n', '\t') else ch
        print(f"  {display:<12} {freq.get(ch, 0):>10} {codes[ch]:>14} {len(codes[ch]):>8}")


# ─────────────────────────────────────────────
# Contoh penggunaan
# ─────────────────────────────────────────────

def demo(text: str, label: str, show_tree: bool = True, show_encoded: bool = True) -> None:
    print(f"\n{'═'*52}")
    print(f"  {label}")
    print(f"{'═'*52}")
    print(f"  Teks  : \"{text}\"")

    hc = HuffmanCoding()
    encoded, codes = hc.compress(text)
    decoded = hc.decompress(encoded)

    freq = HuffmanCoding.frequency(text)
    print_codes(codes, freq)

    if show_tree:
        print(f"\n  Pohon Huffman:")
        print_tree(hc.root)

    if show_encoded:
        MAX = 80
        preview = encoded[:MAX] + ("..." if len(encoded) > MAX else "")
        print(f"\n  Encoded ({len(encoded)} bit):")
        print(f"    {preview}")

    compression_stats(text, encoded, codes)

    # Verifikasi
    status = "✓ BERHASIL" if decoded == text else "✗ GAGAL"
    print(f"  Verifikasi decode : {status}")


def main():
    print("\n╔══════════════════════════════════════════════════╗")
    print("║          HUFFMAN CODING – KOMPRESI DATA         ║")
    print("╚══════════════════════════════════════════════════╝")

    demo(
        "ABRACADABRA",
        label="Contoh 1 – Teks Klasik",
    )

    demo(
        "aaabbbccddeeeefffff",
        label="Contoh 2 – Frekuensi Bervariasi",
    )

    demo(
        "AAAAAA",
        label="Contoh 3 – Satu Karakter Unik",
        show_tree=True,
    )

    demo(
        "the quick brown fox jumps over the lazy dog",
        label="Contoh 4 – Kalimat Bahasa Inggris",
        show_tree=False,
    )

    demo(
        "Belajar algoritma Huffman itu menyenangkan! "
        "Huffman digunakan untuk kompresi data.",
        label="Contoh 5 – Kalimat Bahasa Indonesia",
        show_tree=False,
        show_encoded=False,
    )

    print(f"\n{'═'*52}\n")


if __name__ == "__main__":
    main()
