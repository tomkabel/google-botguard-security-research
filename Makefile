PDF_ENGINE ?= lualatex

# Body font is DejaVu Sans (not Serif) because it is the only locally
# installed font carrying the ✓ (U+2713) and ✗ (U+2717) glyphs used in the
# comparison tables. DejaVu Serif lacks them, and luaotfload's
# `mainfontfallback` mechanism fails to resolve the fallback under the
# current TeX Live, so the fallback approach no longer builds.
paper.pdf: paper.md
	pandoc paper.md -o paper.pdf --pdf-engine=$(PDF_ENGINE) \
		-V geometry:margin=1in -V fontsize=11pt \
		-V mainfont="DejaVu Sans" \
		-V monofont="DejaVu Sans Mono"

.PHONY: clean
clean:
	rm -f paper.pdf
