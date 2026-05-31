# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-01

Data-integrity hardening pass (introduces data **schema v2** — the release and
the on-disk data-format version are tracked separately). All changes are
backward compatible: existing v1.0 logs are migrated automatically on first use
(a backup is taken first), which is why this is a minor bump, not a major one.

### Added
- **Schema versioning.** A `DATA_DIR/.schema` file and a `v=2` tag on the DATA
  BLOCK make every log self-describing, so future format changes never silently
  mis-parse old data.
- **`session` primary key** in `data.csv` — sessions are no longer identified by
  row order alone (which broke when multiple sessions shared one date).
- **Integrity self-check** before each log: `data.csv` rows, `sessions/` files,
  and `transcripts.md` blocks must agree; a mismatch from an interrupted write is
  detected and reconciled instead of compounded.
- **DATA BLOCK validation** — keys, ranges (1–10 / 0–100), and `NA` are checked;
  a malformed or missing block stops the log and asks, rather than writing a
  guessed/partial row.
- **Mode D (amend)** — a guarded path to correct a past score, transcript, or
  mistake row, with a backup taken first.
- **Stable mistake keys + structural/lexical classes** in the mistake bank, so
  recurring errors are matched reliably and topic-dependent vocabulary items
  aren't auto-"resolved" just because a random topic never resurfaced them.
- **Closed-loop check** — the app acknowledges whether last session's focus was
  applied, and the skill nudges you if you forgot to carry it over.

### Changed
- **Backups no longer depend on Python.** The before-write safety snapshot is a
  plain file copy that always works; the bundled `backup_data.py` is now an
  optional helper (it also prunes old snapshots) for when Python is present.
  Charts remain the only Python/matplotlib use, and still fall back to a text
  trend when unavailable.

### Fixed
- **BOM / encoding hazard.** The data-path control file and CSV are read
  BOM-tolerant (`utf-8-sig`) and written as UTF-8 without BOM, fixing a case
  where a stray BOM could split data across two folders unnoticed.

## [1.0.0] - 2026-05-31

### Added
- Initial release: app coaching prompt, per-session scored report, `data.csv`
  trend logging with PNG/text charts, verbatim annotated transcript log, mistake
  bank with promotion/resolution, adaptive-difficulty signal, next-focus
  carry-over, before-write backups, and bilingual (EN / 中文) docs.

[1.1.0]: https://github.com/XcutingUnicorn235/Oral-English-Practice/releases/tag/v1.1.0
[1.0.0]: https://github.com/XcutingUnicorn235/Oral-English-Practice/releases/tag/v1.0.0
