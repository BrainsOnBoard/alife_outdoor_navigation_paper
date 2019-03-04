# Simple Xe/LaTeX Makefile
# (C) Andrew Mundy 2012

# Configuration
TEX=pdflatex
BIB=bibtex
TEXFLAGS=--shell-escape
BIBFLAGS=
COMMIT?=5d8b8cdd51fd05a4699d24d5ff4afd7ed983eb95
texdoc=alife

.PHONY: clean bib count all

# Make all items
all : $(texdoc).pdf

$(texdoc).pdf : $(texdoc).tex
	$(TEX) $(TEXFLAGS) $(texdoc)

# Generate reference requirements
$(texdoc).aux : $(texdoc).tex
	$(TEX) $(TEXFLAGS) $(texdoc)

# Generate the bibliography
bib : $(texdoc).aux
	$(BIB) $(BIBFLAGS) $(texdoc)
	$(TEX) $(TEXFLAGS) $(texdoc)
	$(TEX) $(TEXFLAGS) $(texdoc)

# Clean
clean :
	find . -type f -regex ".*$(texdoc).*\.\(aux\|bbl\|bcf\|blg\|log\|png\|out\|toc\|lof\|lot\|count\)" -delete
	rm -f $(texdoc).pdf $ $(texdoc).run.xml $(texdoc)-blx.bib
