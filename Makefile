etc/_rsstail:
	compgen.py zsh > $@

etc/rsstail.sh:
	compgen.py bash > $@

compgen: etc/_rsstail etc/rsstail.sh

rsstail.pyz:
	./pyzgen.sh $@

PHONY: standalone compgen
