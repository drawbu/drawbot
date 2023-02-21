SRC_DIR := drawbot
CONF := vars/config.json

PY_ENV := venv
PY_BIN := $(PY_ENV)/bin

PIP := $(PY_BIN)/pip

CMD_NOT_FOUND = $(error $(strip $(1)) is required for this rule)
CHECK_CMD = $(if $(shell command -v $(1)),, $(call CMD_NOT_FOUND, $(1)))

all: $(PY_BIN)/drawbot $(CONF)

$(CONF):
	@ cp vars/config.json.example vars/config.json

$(PIP): $(PY_ENV)

$(PY_BIN)/drawbot: $(PY_ENV)
	@ $(PIP) install -e .

$(PY_ENV):
	$(call CHECK_CMD, python3)
	@ python3 -m venv venv
	@ chmod +x $(V_BIN)/activate
	$(info Use source $(PY_BIN)/activate to enable venv overriding!)

clean:
	$(RM) -r *.egg-info
	find $(SRC_DIR) -type f -name "*.pyc" -exec rm -rf {} +

fclean: clean
	$(RM) -f $(PY_ENV)
	$(RM) $(CONF)

.PHONY: clean fclean

re: fclean all

.PHONY: re
