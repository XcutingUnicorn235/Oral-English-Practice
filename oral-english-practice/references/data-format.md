# Data Format Reference

Exact schemas and parsing rules for the oral-english-practice skill. SKILL.md
points here so its body stays lean — read this when logging a session (Mode B)
or when unsure of a field.

## DATA_DIR resolution

Resolve the data directory before any read/write:

1. If `~/.oral-english-data-path` exists (home = `%USERPROFILE%` on Windows),
   use its first non-empty line as DATA_DIR. This lets the user keep data on
   any drive (e.g. `D:\oral-english-practice-log`).
2. Otherwise DATA_DIR = `~/oral-english-practice-log`.
3. If DATA_DIR does not exist, create it, copy every file from this skill's
   `templates/` into it (`app-prompt.md`, `data.csv`, `transcripts.md`,
   `next-focus.md`, `mistakes.md`, and `gitignore` → renamed to `.gitignore`),
   create empty `sessions/` and `backups/` subdirectories, then clearly tell
   the user the FULL absolute path of the data folder, so they always know
   where their practice records are kept.

**Relocating on request:** if the user asks to move their data ("put my practice
log at X"), write X as the first line of `~/.oral-english-data-path`, move the
existing DATA_DIR contents to X (create X if needed), and confirm the new path.

## File layout (under DATA_DIR)

| Path | Purpose |
|------|---------|
| `app-prompt.md` | Prompt the user pastes into the Claude app (coach + topics + report spec) |
| `data.csv` | One scored row per session; the trend dataset |
| `transcripts.md` | Verbatim annotated error log, newest on top |
| `mistakes.md` | Mistake bank: confirmed recurring errors with frequency + status |
| `next-focus.md` | Carry-over card; contains a block the user pastes into the app |
| `sessions/` | Full report per session: `session-NN-YYYY-MM-DD.md` |
| `backups/` | Timestamped snapshots written before each Mode B write |
| `.gitignore` | Excludes everything (data is private) if the folder is ever in a repo |

## data.csv

Header (keep column order exactly):

```
date,cefr,ielts,native,fluency,lexis,grammar,pronunciation,discourse,interaction,listening
```

- Scores `fluency`…`listening` are integers 1–10.
- `native` is distance-to-native, integer 0–100.
- A dimension that genuinely could not be judged (e.g. pronunciation in a
  text-only session) is written as `NA` — never invent a number.

## DATA BLOCK (last line of the app report)

```
date=YYYY-MM-DD | cefr=__ | ielts=__ | native=__/100 | fluency=__ | lexis=__ | grammar=__ | pronunciation=__ | discourse=__ | interaction=__ | listening=__
```

Parse rule: split on `|`, take the value after each `=`. For `native=58/100`
keep only the number before `/` (→ `58`). Pass through `NA` verbatim. Map the
eleven values straight onto the CSV columns.

## Annotation tags (transcripts.md)

Inline, the problem span is followed by a bracketed tag, e.g. `I go[G1] there`;
below the line each tag gets a one-line fix.

| Tag | Meaning |
|-----|---------|
| [G] | Grammar (tense, articles, agreement, prepositions…) |
| [V] | Vocabulary gap — couldn't find / used the wrong word |
| [N] | Unnatural / not idiomatic |
| [F] | Fluency stumble — filler, false start, long pause |
| [P] | Pronunciation |

Number within a type to disambiguate: G1, G2, V1, N1…

## mistakes.md — the mistake bank

A compact table of confirmed recurring errors so they get re-drilled until
fixed (this is the review loop; it does not need a full spaced-repetition
algorithm). One row per distinct error pattern:

```
| id | pattern | example (wrong → right) | tag | count | first_seen | last_seen | clean_streak | status |
|----|---------|-------------------------|-----|-------|------------|-----------|--------------|--------|
| 1  | past tense slip | "I go there yesterday" → "I went" | G | 3 | s1 | s3 | 0 | active |
```

- `count` — how many sessions it has appeared in.
- `first_seen` / `last_seen` — the **session number** it appeared in (e.g. `s1`,
  `s3`). Use session numbers, NOT dates — multiple sessions can share one date.
- `clean_streak` — consecutive sessions since `last_seen` in which the pattern
  did NOT appear. This is the field that drives resolution deterministically,
  so the rule can be executed from stored state alone (no re-reading history).
- `status` — `active` (still drilling) or `resolved` (archived, not deleted).

Per-session update (deterministic):
- **Appears this session** → `count += 1`, `last_seen = sNN`, `clean_streak = 0`;
  if it was `resolved`, flip back to `active`.
- **Active row that did NOT appear** → `clean_streak += 1`; when it reaches **2**,
  set `status = resolved`.
- Promotion rule: a pattern enters the bank once it has appeared in **≥2
  sessions**, OR **≥3 times within a single session** (a strong intra-session
  signal). A lone one-off occurrence stays noise, logged only in transcripts.md.

## Adaptive difficulty signal

There is no numeric difficulty engine; instead, give the app an explicit,
evidence-based nudge in next-focus, derived from the last session's scores:
- A dimension scoring ≤4 → "go easier / scaffold more here."
- A dimension scoring ≥8 → "push harder here."
- Otherwise hold. Always cite the actual scores so the app calibrates from data,
  not vibes. Mirrors the success-rate targeting that mature tutors (e.g. Fluent's
  60–70% target) use, kept lightweight.
