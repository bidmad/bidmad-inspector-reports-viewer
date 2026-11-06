#!/usr/bin/env python3
"""XOR-encode a GitHub read-only PAT into the A/B arrays for the viewer's GH config.

For the public viewer's embedded read-only PAT (Contents:Read on bidmad-inspector-reports).
Reads the token from stdin (NOT argv) so it never lands in shell history.

Usage:
    pbpaste | python3 -I tools/pat_xor.py   # token on clipboard, nothing echoed
    python3 -I tools/pat_xor.py             # then paste token, press Enter

Paste the printed A: / B: lines into index.html's `var GH = { ... }` (replacing the empty arrays).
"""
import sys

KEY = 0x5A  # must match GH.KEY in index.html


def main():
    tok = sys.stdin.readline().strip()
    if not tok:
        sys.exit("no token on stdin")
    enc = [b ^ KEY for b in tok.encode("ascii")]
    mid = (len(enc) + 1) // 2
    print("    A: [" + ", ".join(str(b) for b in enc[:mid]) + "],")
    print("    B: [" + ", ".join(str(b) for b in enc[mid:]) + "]")


if __name__ == "__main__":
    main()
