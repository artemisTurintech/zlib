"""
Benchmark for the zlib compression library (Python built-in zlib module).
One unit of work: compress or decompress a single 1 MB buffer.
Each row in the output is one trial; a summary row with mean/stdev is appended.

Usage:
    python run_benchmark.py [--runs N]
"""

import json
import math
import sys
import timeit
import zlib

NUMBER = 200   # compress/decompress calls per trial

DATA_SIZE_MB = 1
DATA_SIZE = DATA_SIZE_MB * 1024 * 1024


def _make_data(size: int) -> bytes:
    chunk = bytes(range(256)) * 4
    base = (chunk * (size // len(chunk) + 1))[:size]
    ba = bytearray(base)
    for i in range(0, size, 256):
        ba[i] = (i // 256) & 0xFF
    return bytes(ba)


def _mean(values):
    return sum(values) / len(values)


def _stdev(values):
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def main():
    repeat = 1
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--runs" and i + 1 < len(sys.argv[1:]):
            repeat = int(sys.argv[i + 2])

    print(f"Preparing {DATA_SIZE_MB} MB input buffer ...")
    raw = _make_data(DATA_SIZE)
    compressed = zlib.compress(raw)
    compress_ratio = len(compressed) / DATA_SIZE

    print(f"number={NUMBER}  runs={repeat}\n")

    comp_times = timeit.repeat(
        stmt="zlib.compress(raw)",
        globals={"zlib": zlib, "raw": raw},
        number=NUMBER,
        repeat=repeat,
    )
    decomp_times = timeit.repeat(
        stmt="zlib.decompress(compressed)",
        globals={"zlib": zlib, "compressed": compressed},
        number=NUMBER,
        repeat=repeat,
    )

    comp_mbps   = [round(NUMBER * DATA_SIZE_MB / t, 2) for t in comp_times]
    decomp_mbps = [round(NUMBER * DATA_SIZE_MB / t, 2) for t in decomp_times]

    c_mean, c_std   = _mean(comp_mbps),   _stdev(comp_mbps)
    d_mean, d_std   = _mean(decomp_mbps), _stdev(decomp_mbps)

    print(f"  runs={repeat}  number={NUMBER}")
    print(f"  compress   mean={c_mean:.1f} MB/s  stdev={c_std:.1f} MB/s")
    print(f"  decompress mean={d_mean:.1f} MB/s  stdev={d_std:.1f} MB/s")
    print(f"  overall score  {math.sqrt(c_mean * d_mean):.1f}  (geometric mean of throughputs, higher is better)")

    overall_score = round(math.sqrt(c_mean * d_mean), 2)

    result = [
        {
            "runs":                       repeat,
            "overall_score":              overall_score,
            "overall_score_better_when":  "higher",
            "compress_mbps_mean":         round(c_mean, 2),
            "compress_mbps_stdev":        round(c_std,  2),
            "compress_mbps_better_when":  "higher",
            "decompress_mbps_mean":       round(d_mean, 2),
            "decompress_mbps_stdev":      round(d_std,  2),
            "decompress_mbps_better_when":"higher",
            "compress_ratio_mean":        round(compress_ratio, 6),
            "compress_ratio_stdev":       0.0,
            "compress_ratio_better_when": "lower",
        }
    ]

    with open("artemis_results.json", "w") as f:
        json.dump(result, f, indent=2)

    print("\nResults written to artemis_results.json")


if __name__ == "__main__":
    main()
