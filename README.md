# Oral English Practice

*English | [中文（先看这里）](【先看这里】.md)*

A long-term spoken-English coaching tracker for Claude Code.

You practice **speaking and listening by voice in the Claude app**; this skill
runs in **Claude Code** and turns each session into durable progress: it logs a
verbatim annotated error transcript, records scores, tracks your trend toward
native level, and writes the focus for your next session.

It exists to fix the gap between the two tools: the app is a great practice
arena but has **no memory** of your past sessions; Claude Code has no voice but
**can be your long-term memory and analyst**. You carry two short text payloads
between them, and this skill does the rest.

**One subscription, two pastes, long-term practice.**

---

## Features

- 🎙️ **Ready-made coaching prompt** — paste it into the Claude app and start a native-level voice session (conversation + listening) right away.
- 📊 **Scored assessment report** every session: a CEFR/IELTS estimate, a "distance to native /100", and seven 1–10 dimensions.
- 📈 **Long-term progress tracking** — every session logged to `data.csv`, with trend charts (or a text trend if you have no Python).
- 📝 **Verbatim error transcript** — every stumble, grammar slip, vocab gap, and unnatural phrase tagged inline and explained.
- 🏦 **Mistake bank** — recurring errors are confirmed, counted, and re-drilled until you go clean, then archived.
- 🎚️ **Adaptive difficulty** — the next-session focus tells the coach what to ease or push, based on your actual scores.
- 🎭 **Fully customizable** — change the coach's tone, topics, and correction style in plain language (or by editing one file).
- 🌐 **Bilingual & language-adaptive** — English / 中文 docs, and the skill replies in whatever language you write in.
- 🔒 **Local-first & private** — your records stay on your machine; no uploads, telemetry, or third parties.
- 🪶 **Minimal setup** — just Claude Code + the Claude app; Python/matplotlib is optional (only for chart images).

---

## How it works

```
Claude app (practice, stateless)         Claude Code + this skill (long-term brain)
  · voice conversation + listening         · parse report, archive
  · outputs: annotated transcript      →   · append to data.csv, chart trends
    + report + DATA BLOCK                   · find stubborn weaknesses
                                            · write next-focus
  ← paste next-focus into the app  ───────  · continuity across sessions
```

1. **Get the prompt** — in Claude Code, run `/oral-english-practice` (or say
   "I want to practice spoken English"). It hands you the `app-prompt` plus
   last session's carry-over focus.
2. **Practice** — paste the prompt into the Claude app (voice mode), talk for
   15-30 min. The coach ends with an annotated transcript + a scored report +
   a one-line DATA BLOCK.
3. **Log it** — paste that whole output back into Claude Code. The skill files
   it, updates your trend data, and writes your next focus.
4. **Review** — every few sessions, ask for a trend review/chart.

---

## Install

**Windows:** double-click `install.bat`.
**macOS / Linux:** `bash install.sh`.
**Manual:** copy the `oral-english-practice/` folder into `~/.claude/skills/`.

Re-running the installer is safe — it never touches your data.

### Requirements

**Required — nothing beyond these two:**
- **Claude Code** — runs the skill (logging, mistake bank, backups, diagnosis).
- **Claude app** — voice practice + listening.

That's all you need. Every core feature works with just these — the skill uses
Claude's built-in file tools, and even backups work without Python (Claude
copies the files itself).

**Optional:**
- **Python 3 + `matplotlib`** — only for the visual PNG trend chart. Without it,
  the trend review still works, just as a text/markdown summary. You can add it
  anytime later with `pip install matplotlib`.

---

## Your data

Created on first use, in a clearly named folder so you always know where your
records are. Default location:
- Windows: `%USERPROFILE%\oral-english-practice-log\`
- macOS / Linux: `~/oral-english-practice-log/`

The skill prints the full path the first time it creates the folder.

**You can keep your records anywhere you like.** Two ways to change the location:
- **Easiest:** just tell your Claude, e.g. "move my practice log to `D:\English\`" —
  it sets it up and moves any existing records over.
- **Manual:** create a file `~/.oral-english-data-path` (in your home folder, a
  dot-file with no extension) whose first line is the path you want, e.g.
  `D:\oral-english-practice-log`. The skill uses that path from then on.

### Files

| File | Purpose |
|---|---|
| `app-prompt.md` | The prompt you paste into the Claude app (coach persona + topic pool + report format) |
| `data.csv` | One scored row per session — your trend dataset |
| `transcripts.md` | Verbatim error log; every stumble/error tagged inline and annotated |
| `mistakes.md` | Mistake bank — confirmed recurring errors with frequency + status, re-drilled until fixed |
| `sessions/` | Full report per session (`session-NN-YYYY-MM-DD.md`) |
| `next-focus.md` | Carry-over card; includes a block to paste into the app next time |
| `backups/` | Timestamped snapshots taken before each logging write (last 10 kept) |

### data.csv columns

```
date,cefr,ielts,native,fluency,lexis,grammar,pronunciation,discourse,interaction,listening
```

Scores are 1-10 per dimension; `native` is distance-to-native out of 100; a
dimension that couldn't be judged (e.g. pronunciation in a text-only session)
is recorded as `NA`.

---

## Annotation tags (in transcripts.md)

| Tag | Meaning |
|---|---|
| [G] | Grammar (tense, articles, agreement, prepositions...) |
| [V] | Vocabulary gap — couldn't find / used the wrong word |
| [N] | Unnatural / not idiomatic |
| [F] | Fluency stumble — filler, false start, long pause |
| [P] | Pronunciation |

---

## Privacy

- **Your records stay on your computer.** The skill has no network code — no
  uploads, no telemetry, no analytics, no cloud sync. Your data files
  (`data.csv`, transcripts, mistakes, sessions, backups) are written only to
  your local data folder, and `.gitignore` keeps them out of git.
- **But the skill runs through Claude, which is a cloud AI.** Using it means
  talking to Claude Code and the Claude app, so the text you actually process —
  your reports and your spoken practice — passes through Anthropic's servers as
  part of normal Claude usage, exactly like any Claude conversation. That's
  inherent to using an AI model, not the skill sending data anywhere extra.
- **No third parties.** Nothing goes anywhere beyond the Anthropic services you
  already use by running Claude; there is no separate cloud copy of your
  practice archive.

---

## Sharing

This whole folder is portable. Send it to a friend; they run the installer (or
drop `oral-english-practice/` into their `~/.claude/skills/`). Their data is
created fresh on their own machine — **the skill is the engine, the data is
personal**, so nothing of yours travels with it.

---

## Customizing

- **Coach tone / topics:** edit the prompt block in your `app-prompt.md`.
- **Scored dimensions:** if you change them, keep the DATA BLOCK line and the
  `data.csv` header in sync, or the skill can't parse new sessions.

---

## Credits

Built following Claude's official `skill-creator` best practices (progressive
disclosure, a trigger-focused description) and adapting patterns from the
`fluent` language-learning kit — a mistake bank, write-before-write backups, and
an adaptive-difficulty signal — while staying deliberately lightweight
(CSV + Markdown, no databases) for a single-user, native-level goal.
