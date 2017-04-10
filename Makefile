.PHONY  : all clean install run

MAIN = test.py
VENV = venv

all install: $(VENV)
	$(VENV)/bin/python setup.py install

run: install
	$(VENV)/bin/python $(MAIN)

clean:
	rm -rf $(VENV)

$(VENV):
	virtualenv $(VENV)
