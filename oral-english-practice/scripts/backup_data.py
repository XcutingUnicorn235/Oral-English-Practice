#!/usr/bin/env python3
"""Snapshot the data files before a logging write, and prune old snapshots.

Usage:
    python backup_data.py <DATA_DIR> [keep]

Copies data.csv, transcripts.md, mistakes.md, next-focus.md into
<DATA_DIR>/backups/<UTC-timestamp>/ so a bad parse can never lose history.
Keeps the most recent `keep` snapshots (default 10) and deletes older ones.

Deterministic, dependency-free (stdlib only) — safe to call on every Mode B
write. Missing source files are skipped silently (first run may not have all).
"""
import os
import shutil
import sys
from datetime import datetime, timezone

FILES = ["data.csv", "transcripts.md", "mistakes.md", "next-focus.md"]


def main():
    if len(sys.argv) < 2:
        print("Usage: python backup_data.py <DATA_DIR> [keep]")
        sys.exit(1)
    data_dir = sys.argv[1]
    keep = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    if not os.path.isdir(data_dir):
        print(f"DATA_DIR not found: {data_dir}")
        sys.exit(1)

    backups = os.path.join(data_dir, "backups")
    os.makedirs(backups, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = os.path.join(backups, stamp)
    os.makedirs(dest, exist_ok=True)

    copied = 0
    for name in FILES:
        src = os.path.join(data_dir, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dest, name))
            copied += 1

    # Prune: keep only the newest `keep` snapshot dirs.
    snaps = sorted(
        d for d in os.listdir(backups)
        if os.path.isdir(os.path.join(backups, d))
    )
    for old in snaps[:-keep]:
        shutil.rmtree(os.path.join(backups, old), ignore_errors=True)

    print(f"Backed up {copied} file(s) to {dest} ; kept last {keep} snapshots.")


if __name__ == "__main__":
    main()
