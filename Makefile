# paper.pdf: IEEE S&P submission build (IEEEtran compsoc, see docs/venue.md).
# ieee/ieee.lua maps the markdown structure onto IEEEtran; ieee/template.tex maps the Unicode
# symbols used in the text (✓ ✗ ∼ × € …) for pdflatex.
paper.pdf: paper.md ieee/ieee.lua ieee/template.tex figures/cost_shift.pdf
	mkdir -p build
	pandoc paper.md -o build/paper.tex --lua-filter ieee/ieee.lua --template ieee/template.tex --syntax-highlighting=none
	cd build && pdflatex -interaction=nonstopmode -halt-on-error paper.tex >/dev/null && pdflatex -interaction=nonstopmode -halt-on-error paper.tex >/dev/null
	cp build/paper.pdf paper.pdf
	@python3 ieee/pages.py build/paper.pdf

.PHONY: clean numbers artifact
clean:
	rm -rf paper.pdf build/paper.* build/artifact.zip

numbers:
	python3 analysis/cost_model.py
	python3 measurement/analyze.py --check-paper

# Anonymized artifact: tracked files only; HEAD^{tree} so the zip carries no commit id, history or author metadata.
artifact:
	mkdir -p build
	git archive --format=zip -o build/artifact.zip HEAD^{tree} analysis measurement figures ieee docs/corpus.csv paper.md Makefile
