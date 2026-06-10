"""
Benchmark for the zlib compression library (Python built-in zlib module).
One unit of work: compress or decompress a single 1 MB buffer.
Each row in the output is one trial (one repeat of NUMBER calls).
"""

import json
import math
import timeit
import zlib

NUMBER = 200   # compress/decompress calls per trial
REPEAT = 10    # number of trials

DATA_SIZE_MB = 1
DATA_SIZE = DATA_SIZE_MB * 1024 * 1024


def _make_data(size: int) -> bytes:
    chunk = bytes(range(256)) * 4
    base = (chunk * (size // len(chunk) + 1))[:size]
    ba = bytearray(base)
    for i in range(0, size, 256):
        ba[i] = (i // 256) & 0xFF
    return bytes(ba)


def main():
    print(f"Preparing {DATA_SIZE_MB} MB input buffer ...")
    raw = _make_data(DATA_SIZE)
    compressed = zlib.compress(raw)
    compress_ratio = len(compressed) / DATA_SIZE

    print(f"number={NUMBER}  repeat={REPEAT}\n")

    comp_times = timeit.repeat(
        stmt="zlib.compress(raw)",
        globals={"zlib": zlib, "raw": raw},
        number=NUMBER,
        repeat=REPEAT,
    )
    decomp_times = timeit.repeat(
        stmt="zlib.decompress(compressed)",
        globals={"zlib": zlib, "compressed": compressed},
        number=NUMBER,
        repeat=REPEAT,
    )

    rows = [
        {
            "trial": i + 1,
            "number": NUMBER,
            "compress_mbps": round(NUMBER * DATA_SIZE_MB / comp_times[i], 2),
            "decompress_mbps": round(NUMBER * DATA_SIZE_MB / decomp_times[i], 2),
            "compress_ratio": round(compress_ratio, 6),
        }
        for i in range(REPEAT)
    ]

    for r in rows:
        print(f"trial {r['trial']:2d}: compress={r['compress_mbps']:.1f} MB/s  decompress={r['decompress_mbps']:.1f} MB/s  ratio={r['compress_ratio']:.4f}")

    with open("artemis_results.json", "w") as f:
        json.dump(rows, f, indent=2)

    print("\nResults written to artemis_results.json")


if __name__ == "__main__":
    main()
