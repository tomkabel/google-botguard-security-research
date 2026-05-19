# AGENTS.md — google-botguard-security-research

This is an academic Systematization of Knowledge (SoK) paper repository, not a software project. There is no build system, CI, tests, or code.

## Structure

- **`paper.md`** — single-file manuscript (479 lines, 9 sections)
- **`notes/bibliography.md`** — complete bibliography (78 references); paper.md defers to it
- **`notes/outline.md`** — detailed section-level outline
- **`notes/qa-report.md`** — empirical claim audit, neutrality audit, SoK checklist
- **`notes/content-audit.md`** — classification of prior README content
- **`figures/*.tex`** — LaTeX/TikZ figures (prisma-flow, taxonomy-table, auth-spectrum)
- **`paper_TODO.md`** — authoritative revision tracker: completed revisions and remaining pre-submission tasks
- **`README.md`** — paper abstract, repository structure, changelog (v1.0 → v2.0 SoK pivot)

## Workflow

- The manuscript is v2.0 (May 2026 SoK pivot from v1.0 predictive/empirical draft)
- Fifth revision addressing senior PC member code review; see `paper_TODO.md` for remaining items
- Bibliography is maintained in `notes/bibliography.md`, not inline in paper.md
- LaTeX figures are standalone `.tex` files; no compiled PDFs in the repo
- There are no scripts, Makefiles, or automation — all work is manual editing
