# Data Format Reference (schema v2)

Exact schemas and parsing rules for the oral-english-practice skill. SKILL.md
points here so its body stays lean — read this when logging a session (Mode B),
amending one (Mode D), or when unsure of a field.

## Encoding discipline (read this first)

All text files this skill reads or writes are **UTF-8 with NO BOM**, newline `\n`.
This matters: a stray BOM at the start of a file makes the first line begin with
an invisible `﻿`, which silently breaks path resolution and CSV parsing.

- When you read a control file (`~/.oral-english-data-path`, `data.csv`), **strip
  a leading BOM and surrounding whitespace** before using the value.
- When you write any file, write plain UTF-8 (no BOM). The Write/Edit tools do
  this by default — just never paste a BOM in yourself.
- The helper scripts open files with `encoding="utf-8-sig"` for the same reason.

## DATA_DIR resolution

Resolve the data directory before any read/write:

1. If `~/.oral-english-data-path` exists (home = `%USERPROFILE%` on Windows),
   read it, **strip BOM + whitespace**, and use the first non-empty line as
   DATA_DIR. This lets the user keep data on any drive (e.g.
   `E:\oral-english-practice-log`).
2. Otherwise DATA_DIR = `~/oral-english-practice-log`.
3. If DATA_DIR does not exist, create it, copy every file from this skill's
   `templates/` into it (`app-prompt.md`, `data.csv`, `transcripts.md`,
   `next-focus.md`, `mistakes.md`, and `gitignore` → renamed to `.gitignore`),
   create empty `sessions/` and `backups/` subdirectories, write `.schema`
   containing `2`, then clearly tell the user the FULL absolute path of the data
   folder, so they always know where their practice records are kept.

**Relocating on request:** if the user asks to move their data ("put my practice
log at X"), write X as the first line of `~/.oral-english-data-path` (UTF-8, no
BOM), move the existing DATA_DIR contents to X (create X if needed), and confirm
the new path.

## Schema version & auto-migration

`DATA_DIR/.schema` holds the schema version as a bare integer. Absent or `1`
means **legacy (pre-v2)**: `data.csv` has no `session` column and `mistakes.md`
has the old `id` column. Before the first write of a Mode B session, migrate a
legacy DATA_DIR to v2 (this is safe and idempotent — back up first, per Mode B):

- **data.csv** — prepend a `session` column; backfill values `1..N` in existing
  row order. New header is the v2 header below.
- **mistakes.md** — replace the `id` column with a stable `key` (see below) and
  add a `class` column.
- Write `.schema` = `2`.

A DATA BLOCK pasted from the app carries `v=2`. If `v` is absent, treat the
report as legacy v1 — the 11 scoring fields are identical across v1 and v2, so
it still parses; only the explicit version tag is new.

## File layout (under DATA_DIR)

| Path | Purpose |
|------|---------|
| `.schema` | Schema version (bare integer; `2` for current) |
| `app-prompt.md` | Prompt the user pastes into the Claude app (coach + topics + report spec) |
| `data.csv` | One scored row per session; the trend dataset |
| `transcripts.md` | Verbatim annotated error log, newest on top |
| `mistakes.md` | Mistake bank: confirmed recurring errors with frequency + status |
| `next-focus.md` | Carry-over card; contains a block the user pastes into the app |
| `sessions/` | Full report per session: `session-NN-YYYY-MM-DD.md` |
| `backups/` | Timestamped snapshots written before each Mode B / Mode D write |
| `.gitignore` | Excludes everything (data is private) if the folder is ever in a repo |

## Integrity invariant

At rest, these three counts MUST be equal:

```
data rows in data.csv (excluding header)  ==  files in sessions/  ==  session blocks in transcripts.md
```

Check this at the START of Mode B (see SKILL.md). If they disagree, a previous
write was interrupted — reconcile before writing anything new (the backups/ dir
holds the last good snapshots). The authoritative count of "sessions that
happened" is **`sessions/` file count**, because each session file is written
whole; `data.csv` and `transcripts.md` are reconciled up to match it.

## data.csv (schema v2)

Header (keep column order exactly):

```
session,date,cefr,ielts,native,fluency,lexis,grammar,pronunciation,discourse,interaction,listening
```

- `session` — integer session number NN (the primary key; assigned by the skill,
  not the app). Rows are kept in ascending session order.
- Scores `fluency`…`listening` are integers 1–10.
- `native` is distance-to-native, integer 0–100.
- `cefr` is text (e.g. `B1+`), `ielts` is a number (e.g. `5.5`).
- A dimension that genuinely could not be judged (e.g. pronunciation in a
  text-only session) is written as `NA` — never invent a number.

## DATA BLOCK (last line of the app report)

```
v=2 | date=YYYY-MM-DD | cefr=__ | ielts=__ | native=__/100 | fluency=__ | lexis=__ | grammar=__ | pronunciation=__ | discourse=__ | interaction=__ | listening=__
```

**Parse by key, never by position.** Split on `|`, then split each piece on the
first `=`; build a `{key: value}` map. Then:

1. `v` — schema version. Absent ⇒ treat as `1`. Unknown (>2) ⇒ stop and ask the
   user rather than guessing.
2. Require all 11 scoring keys: `date, cefr, ielts, native, fluency, lexis,
   grammar, pronunciation, discourse, interaction, listening`.
3. For `native=58/100` keep only the number before `/` (→ `58`). Pass `NA`
   through verbatim.
4. **Validate ranges**: `fluency`…`listening` ∈ 1–10 or `NA`; `native` ∈ 0–100
   or `NA`; `date` looks like `YYYY-MM-DD`.

**On any problem — a missing key, an out-of-range value, a malformed line, or no
DATA BLOCK at all — STOP and ask the user; do NOT write a partial or guessed row
to `data.csv`.** If the prose SESSION REPORT has the scores but the DATA BLOCK is
missing/garbled, offer to reconstruct the block from the report and confirm the
numbers with the user before writing. A bad row silently corrupts the trend
(the chart just drops the point) — so the bar is: parse cleanly or don't write.

The skill assigns `session` itself (= the new NN); the app does not send it.

## Annotation tags (transcripts.md)

Inline, the problem span is followed by a bracketed tag, e.g. `I go[G1] there`;
below the line each tag gets a one-line fix.

| Tag | Meaning | Class |
|-----|---------|-------|
| [G] | Grammar (tense, articles, agreement, prepositions…) | structural |
| [V] | Vocabulary gap — couldn't find / used the wrong word | lexical |
| [N] | Unnatural / not idiomatic | structural if a general habit, lexical if a one-off phrase |
| [F] | Fluency stumble — filler, false start, long pause | structural |
| [P] | Pronunciation | structural |

Number within a type to disambiguate: G1, G2, V1, N1…

"Class" (structural vs lexical) drives the resolution rule below.

## mistakes.md — the mistake bank (schema v2)

A compact table of confirmed recurring errors so they get re-drilled until
fixed (this is the review loop; it does not need a full spaced-repetition
algorithm). One row per distinct error pattern:

```
| key | pattern | example (wrong → right) | tag | class | count | first_seen | last_seen | clean_streak | status |
|-----|---------|-------------------------|-----|-------|-------|------------|-----------|--------------|--------|
| G-past-tense-slip | past tense slip | "I go there yesterday" → "I went" | G | struct | 3 | s1 | s3 | 0 | active |
```

- `key` — a **stable, human-readable identity** for the pattern: lowercase
  `tag-shortslug` (e.g. `G-past-tense-slip`, `F-fillers`, `V-tryon`). This is the
  match key: when deciding whether this session's error is "the same pattern"
  already in the bank, match on `key` / meaning, not on the exact words. One
  canonical key per pattern prevents both false merges (lumping distinct errors)
  and false splits (logging one recurring error as several rows).
- `pattern` — short human description.
- `tag` — the annotation tag (G/V/N/F/P).
- `class` — `struct` (structural, topic-independent: G, F, P, and general N) or
  `lex` (lexical/specific: V, and one-off idiom N). Governs resolution.
- `count` — **number of distinct sessions the pattern has appeared in** (not
  total occurrences). A pattern promoted via the intra-session rule (≥3× in one
  session) starts at `count = 1`.
- `first_seen` / `last_seen` — the **session number** it appeared in (e.g. `s1`,
  `s3`). Use session numbers, NOT dates — multiple sessions can share one date.
- `clean_streak` — consecutive *qualifying* sessions since `last_seen` in which
  the pattern did NOT appear (see resolution rule for what "qualifying" means).
- `status` — `active` (still drilling) or `resolved` (archived, not deleted).

### Promotion (a pattern enters the bank)

A pattern enters once it has appeared in **≥2 sessions**, OR **≥3 times within a
single session** (a strong intra-session signal). A lone one-off occurrence stays
noise, logged only in transcripts.md.

### Per-session update (deterministic)

- **Appears this session** → `count += 1`, `last_seen = sNN`, `clean_streak = 0`;
  if it was `resolved`, flip back to `active`.
- **Active row that did NOT appear** → advance toward resolution, but the rule
  differs by `class`, because topics are random and "didn't recur" can mean
  "fixed" OR merely "the topic never created the chance to fail":
  - `struct` (topic-independent): `clean_streak += 1`. When it reaches **2** →
    `status = resolved`. (A grammar/pronunciation/filler habit gets plenty of
    chances every session, so two clean sessions is real evidence.)
  - `lex` (topic-dependent): only count a session as "clean" (i.e. only
    `clean_streak += 1`) if **next-focus had flagged this item for re-test** that
    session — so we know it actually had a fair chance to resurface. Otherwise
    HOLD `clean_streak` unchanged. Resolve at **2** qualifying clean sessions.
    This stops specific-vocabulary items from being auto-"resolved" just because
    the random topic never required that word again.

When a `lex` item is `active`, next-focus should explicitly ask the app to create
a chance to use it again, so the streak can advance honestly.

## Adaptive difficulty signal

There is no numeric difficulty engine; instead, give the app an explicit,
evidence-based nudge in next-focus, derived from the last session's scores:
- A dimension scoring ≤4 → "go easier / scaffold more here."
- A dimension scoring ≥8 → "push harder here."
- Otherwise hold. Always cite the actual scores so the app calibrates from data,
  not vibes. Mirrors the success-rate targeting that mature tutors (e.g. Fluent's
  60–70% target) use, kept lightweight.

## Closed-loop check (was the focus actually applied?)

next-focus → app → report is a manual loop the user carries by hand; if they
forget to paste next-focus, the app (which has no memory) silently starts fresh.
The v2 app-prompt asks the coach to briefly acknowledge a FOCUS block at the
start of the report when one was given. In Mode B, if there were active stubborn
weaknesses but the report shows no sign the focus was applied, gently remind the
user to paste `next-focus.md` into the app before the next session.
