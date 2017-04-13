.PHONY  : all clean install run test

MAIN = test.py
VENV = venv

install: $(VENV)
	$(VENV)/bin/python setup.py install

all: | install test

run: install
	$(VENV)/bin/python $(MAIN)

test: install
	$(VENV)/bin/python setup.py test

clean:
	rm -rf $(VENV)

$(VENV):
	virtualenv $(VENV)
