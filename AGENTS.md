# AGENTS.md — google-botguard-security-research

This is an academic Systematization of Knowledge (SoK) paper repository. No code, no tests, no CI. The only build target is the compiled PDF.

## Structure

- `paper.md` — the complete, self-contained manuscript (8 sections in two parts, with the full 85-reference bibliography inlined at the end). Canonical deliverable.
- `README.md` — abstract, build instructions, changelog.
- `Makefile` — builds `paper.pdf` from `paper.md` via pandoc + lualatex.

## Workflow

- All edits happen in `paper.md`. References are inline at the bottom — there is no separate bibliography file.
- `make` produces `paper.pdf`; `make clean` removes it. The PDF is a git-ignored build artifact — do not commit it.

## Editing rules

- Inline `[N]` citations must match the `**[N]**` entries in the References section. Adding or removing a reference requires renumbering every inline citation.
- Preserve the two-part structure (Part I: historical retrospective; Part II: VLM/Operator Synthesis analysis).
- Tone is analytically neutral SoK — no prescriptive "defenders should" language, no fabricated numeric estimates.

## Build pitfall

The Makefile uses `mainfont="DejaVu Sans"` (not Serif) because it is the only locally installed font carrying the ✓ (U+2713) and ✗ (U+2717) glyphs in the comparison tables. DejaVu Serif lacks them, and luaotfload's `mainfontfallback` mechanism fails to resolve under the current TeX Live — do not reintroduce it.
