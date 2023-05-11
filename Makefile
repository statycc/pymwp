SHELL := /bin/bash

SRC_DIR = guide/
OUT_DIR = out/

WEB_SOURCES := $(wildcard $(SRC_DIR:%=%*.md))
PDF_SOURCES := $(filter-out guide/6_challenge_part_2.md,$(WEB_SOURCES))

OPTIONS = -f markdown+emoji --section-divs --file-scope --metadata-file=$(SRC_DIR)metadata.yaml
HTML_OPTS = $(OPTIONS) --template=$(SRC_DIR)template.html -t html --mathjax --shift-heading-level-by=0 --number-sections --number-offset=0
PDF_OPTS = $(OPTIONS) --pdf-engine=xelatex -V links-as-notes  --toc --toc-depth=2 --include-in-header=$(SRC_DIR)header.tex


all: clean main doc

.PHONY: clean
clean:
	rm -rf $(OUT_DIR)

.PHONY: main
main:
	 mkdir -p $(OUT_DIR) && pandoc $(HTML_OPTS) -s $(WEB_SOURCES) -o $(OUT_DIR)index.html


.PHONY: doc
doc:
	 mkdir -p $(OUT_DIR) && pandoc $(PDF_OPTS) -s $(PDF_SOURCES) -o $(OUT_DIR)guide.pdf
