all: update_examples upgrade

update_examples:
	@wget https://github.com/statycc/pymwp/releases/download/$(version)/examples.zip -O ex.zip \
	&& unzip -o ex.zip -d c_files \
	; rm -rf ex.zip c_files/readme.md

upgrade:
	@sed -i -e 's/pymwp==.*/pymwp==$(version)/g' requirements.txt && rm -rf requirements.txt-e