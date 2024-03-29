SRC_DIR := drawbot
CONF := vars/config.json

PY_ENV := venv
PY_BIN := $(PY_ENV)/bin

PIP := $(PY_BIN)/pip

CMD_NOT_FOUND = $(error $(strip $(1)) is required for this rule)
CHECK_CMD = $(if $(shell command -v $(1)),, $(call CMD_NOT_FOUND, $(1)))

all: start

$(CONF):
	@ cp vars/config.json.example vars/config.json

$(PIP): $(PY_ENV)

$(PY_BIN)/drawbot: $(PY_ENV)
	@ $(PIP) install -e .

$(PY_ENV):
	$(call CHECK_CMD, python3)
	@ python3 -m venv venv
	@ chmod +x $(PY_BIN)/activate
	$(info Use source $(PY_BIN)/activate to enable venv overriding!)

start: $(PY_BIN)/drawbot $(CONF)
	@ $(PY_BIN)/python3 drawbot

clean:
	$(RM) -r *.egg-info
	find $(SRC_DIR) -type f -name "*.pyc" -exec rm -rf {} +

fclean: clean
	$(RM) -r $(PY_ENV)
	$(RM) $(CONF)
	$(RM) vars/*.json

.PHONY: clean fclean

re: fclean all

.PHONY: re
