VENV = venv
V_BIN = $(VENV)/bin

all: start


$(V_BIN)/python:
	python3 -m venv venv
	chmod +x $(V_BIN)/activate
	./$(V_BIN)/activate

	$(V_BIN)/pip install -e .


vars/config.json:
	cp vars/config.json.example vars/config.json


start: $(V_BIN)/python vars/config.json
	python3 drawbot


clean:
	rm -rf venv
	rm -rf *.egg-info
	rm -rf */__pycache__


fclean: clean
	rm -rf venv
	rm vars/*.json


.PHONY: all clean fclean start
