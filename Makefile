VENV = venv
VBIN = $(VENV)/bin

all: start

clean:
	rm -rf venv
	rm -rf *.egg-info
	rm -rf */__pycache__
	rm vars/*.json

$(VBIN)/python:
	python3 -m venv venv
	chmod +x $(VBIN)/activate
	./$(VBIN)/activate
	${VBIN}/pip install -e .

vars/config.json:
	cp vars/config.json.example vars/config.json

start: $(VBIN)/python vars/config.json
	python3 drawbot

.PHONY: all clean start
