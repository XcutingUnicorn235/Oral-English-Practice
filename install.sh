#!/usr/bin/env bash
# Oral English Practice — macOS / Linux installer (fallback)
# Usage: bash install.sh
#
# RECOMMENDED instead of this script: install as a Claude Code plugin —
#   /plugin marketplace add XcutingUnicorn235/Oral-English-Practice
#   /plugin install oral-english-practice@xcutingunicorn235
# (gives one-command install + automatic updates).
#
# This script is the manual fallback: it copies the skill folder into
# ~/.claude/skills/ so Claude Code can find it. Your practice DATA is created
# separately on first use (defaults to ~/oral-english-practice-log/) — this
# script does not touch any data, so re-running it is safe.

set -e

SRC="$(cd "$(dirname "$0")" && pwd)"
DST="$HOME/.claude/skills/oral-english-practice"

echo
echo "=== Oral English Practice — install ==="
echo
echo "Source: $SRC/plugins/oral-english-practice/skills/oral-english-practice"
echo "Target: $DST"
echo

mkdir -p "$HOME/.claude/skills"
mkdir -p "$DST"
cp -R "$SRC/plugins/oral-english-practice/skills/oral-english-practice/." "$DST/"
echo "[DONE] skill copied"

echo
echo "=== Install complete ==="
echo
echo "Next:"
echo "  1. Open Claude Code, type:  /oral-english-practice"
echo "     (or just say \"I want to practice spoken English\")"
echo "  2. It gives you the prompt to paste into the Claude APP (voice mode)."
echo "  3. After practicing, paste the app's report back into Claude Code —"
echo "     the skill logs it and tracks your progress."
echo
echo "Your practice-log folder will be created on first use at:  ~/oral-english-practice-log/"
echo "  (the skill prints the full path the first time it creates it.)"
echo "  (To use a different location, create ~/.oral-english-data-path"
echo "   containing the path you want.)"
echo
