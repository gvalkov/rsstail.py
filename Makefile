TARGETS := etc/_rsstail etc/rsstail.sh rsstail.pyz

all: $(TARGETS)

etc/_rsstail:
	./scripts/compgen.py zsh > $@

etc/rsstail.sh:
	./scripts/compgen.py bash > $@

compgen: etc/_rsstail etc/rsstail.sh

rsstail.pyz:
	./scripts/pyzgen.sh $@

clean:
	-rm -f $(TARGETS)

PHONY: compgen clean all
