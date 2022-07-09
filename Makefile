VENV = venv
VBIN = $(VENV)/bin

all: start

clean:
	rm -rf venv
	rm -rf *.egg-info
	rm -rf __pycache__
	rm vars/*.json

$(VBIN)/python:
	python -m venv venv
	chmod +x venv/bin/activate
	./venv/bin/activate
	pip install -e .

vars/config.json:
	cp vars/config.json.example vars/config.json

start: $(VBIN)/python vars/config.json
	python drawbot

.PHONY: all clean start
