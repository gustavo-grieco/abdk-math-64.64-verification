#!/usr/bin/env python3
"""
Usage:
    python prove_stats.py <log_file> [-o output.md]

Reads a log file, finds invariants whose name starts with `prove_`,
outputs a Markdown table of only the VERIFIED ones (✅) sorted alphabetically,
and prints the percentage of prove_ properties that were verified.
"""

import argparse
import sys
from typing import List


def parse_log(log_path: str):
    """
    Returns (verified_proves: List[str], total_prove_count: int)
    """
    verified = []
    total_prove = 0

    with open(log_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            # Extract the invariant name before the first colon (if any)
            if ":" in line:
                name = line.split(":", 1)[0].strip()
                rest = line.split(":", 1)[1].strip()
            else:
                # If no colon, treat whole line as name (unlikely for your logs)
                name = line
                rest = ""

            # Consider only invariants that start with "prove_"
            if name.startswith("prove_"):
                total_prove += 1
                # Consider verified if the word "verified" appears (case-insensitive).
                # This is tolerant to "verified ✅" or just "verified".
                if "verified" in rest.lower() or "verified" in name.lower():
                    verified.append(name)

    return verified, total_prove


def make_markdown_table(verified_proves: List[str], total_prove: int) -> str:
    verified_proves_sorted = sorted(verified_proves)
    md_lines = []
    md_lines.append("| Invariant | Result |")
    md_lines.append("| ----- | :---: |")
    for inv in verified_proves_sorted:
        md_lines.append(f"| `{inv}` | ✅ |")

    # Stats
    verified_count = len(verified_proves_sorted)
    if total_prove > 0:
        percent = (verified_count / total_prove) * 100
    else:
        percent = 0.0

    md_lines.append("")
    md_lines.append(f"**Verified:** {verified_count}/{total_prove} ({percent:.2f}%)")

    return "\n".join(md_lines)


def main():
    parser = argparse.ArgumentParser(description="Produce markdown table + stats for prove_ properties.")
    parser.add_argument("logfile", help="Path to the log file to parse.")
    parser.add_argument("-o", "--output", help="Write markdown output to this file (otherwise prints to stdout).")
    args = parser.parse_args()

    verified, total_prove = parse_log(args.logfile)
    md = make_markdown_table(verified, total_prove)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out:
            out.write(md + "\n")
        print(f"Wrote markdown to {args.output}")
    else:
        print(md)


if __name__ == "__main__":
    main()
