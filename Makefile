# Some simple testing tasks (sorry, UNIX only).

to-hash-one = $(dir $1).hash/$(addsuffix .hash,$(notdir $1))
to-hash = $(foreach fname,$1,$(call to-hash-one,$(fname)))

CYS := $(wildcard kapi/parser/*.pyx) $(wildcard kapi/parser/*.pyi)  $(wildcard kapi/parser/*.pxd)
PYXS := $(wildcard kapi/parser/*.pyx)
CS := $(wildcard kapi/parser/*.c)
PYS := $(wildcard kapi/parser/*.py)
IN := doc-spelling lint cython dev
ALLS := $(sort $(CYS) $(CS) $(PYS) $(REQS))


.PHONY: all
all: test

tst:
	@echo $(call to-hash,requirements/cython.txt)
	@echo $(call to-hash,kapi/parser/%.pyx)


# Recipe from https://www.cmcrossroads.com/article/rebuilding-when-files-checksum-changes
FORCE:

# check_sum.py works perfectly fine but slow when called for every file from $(ALLS)
# (perhaps even several times for each file).
# That is why much less readable but faster solution exists
ifneq (, $(shell command -v sha256sum))
%.hash: FORCE
	$(eval $@_ABS := $(abspath $@))
	$(eval $@_NAME := $($@_ABS))
	$(eval $@_HASHDIR := $(dir $($@_ABS)))
	$(eval $@_TMP := $($@_HASHDIR)../$(notdir $($@_ABS)))
	$(eval $@_ORIG := $(subst /.hash/../,/,$(basename $($@_TMP))))
	@#echo ==== $($@_ABS) $($@_HASHDIR) $($@_NAME) $($@_TMP) $($@_ORIG)
	@if ! (sha256sum --check $($@_ABS) 1>/dev/null 2>/dev/null); then \
	  mkdir -p $($@_HASHDIR); \
	  echo re-hash $($@_ORIG); \
	  sha256sum $($@_ORIG) > $($@_ABS); \
	fi
else
%.hash: FORCE
	@./tools/check_sum.py $@ # --debug
endif

# Enumerate intermediate files to don't remove them automatically.
.SECONDARY: $(call to-hash,$(ALLS))


.install-cython: .update-pip $(call to-hash,requirements_cython.txt)
	@python -m pip install -r requirements_cython.in -c requirements_cython.txt
	@touch .install-cython

kapi/parser/_find_header.c: $(call to-hash,kapi/parser/hdrs.py ./tools/gen.py)
	./tools/gen.py

# _find_headers generator creates _headers.pyi as well
kapi/parser/%.c: kapi/parser/%.pyx $(call to-hash,$(CYS)) kapi/parser/_find_header.c
	cython -3 -o $@ $< -I kapi -Werror

vendor/llhttp/node_modules: vendor/llhttp/package.json
	cd vendor/llhttp; npm install

.llhttp-gen: vendor/llhttp/node_modules
	$(MAKE) -C vendor/llhttp generate
	@touch .llhttp-gen

.PHONY: generate-llhttp
generate-llhttp: .llhttp-gen

.PHONY: cythonize
cythonize: .install-cython $(PYXS:.pyx=.c)

.develop: .install-deps generate-llhttp $(call to-hash,$(PYS) $(CYS) $(CS))
	python -m pip install -e . -c requirements/runtime-deps.txt
	@touch .develop

.PHONY: test
test: .develop
	@pytest -q

.PHONY: vtest
vtest: .develop
	@pytest -s -v
	@python -X dev -m pytest --cov-append -s -v -m dev_mode

.PHONY: vvtest
vvtest: .develop
	@pytest -vv
	@python -X dev -m pytest --cov-append -s -vv -m dev_mode

.PHONY: cov-dev
cov-dev: .develop
	@pytest --cov-report=html
	@echo "xdg-open file://`pwd`/htmlcov/index.html"



.PHONY: clean
clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf `find . -name .hash`
	@rm -rf `find . -name .md5`  # old styling
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -f `find . -type f -name '@*' `
	@rm -f `find . -type f -name '#*#' `
	@rm -f `find . -type f -name '*.orig' `
	@rm -f `find . -type f -name '*.rej' `
	@rm -f `find . -type f -name '*.md5' `  # old styling
	@rm -f .coverage
	@rm -rf htmlcov
	@rm -rf build
	@rm -rf cover
	@make -C docs clean
	@python setup.py clean
	@rm -f kapi/parser/*.so
	@rm -f kapi/parser/*.pyd
	@rm -f kapi/parser/*.html
	@rm -f kapi/parser/_frozenlist.c
	@rm -f kapi/parser/_find_header.c
	@rm -f kapi/parser/_http_parser.c
	@rm -f kapi/parser/_http_writer.c
	@rm -f kapi/parser/_websocket.c
	@rm -rf .tox
	@rm -f .develop
	@rm -f .flake
	@rm -rf kapi/parser.egg-info
	@rm -f .install-deps
	@rm -f .install-cython
	@rm -rf vendor/llhttp/node_modules
	@rm -f .llhttp-gen
	@$(MAKE) -C vendor/llhttp clean

.PHONY: doc
doc:
	@make -C docs html SPHINXOPTS="-W --keep-going -n -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"

.PHONY: doc-spelling
doc-spelling:
	@make -C docs spelling SPHINXOPTS="-W --keep-going -n -E"

.PHONY: install
install: .update-pip
	@python -m pip install -r requirements/dev.in -c requirements/dev.txt

.PHONY: install-dev
install-dev: .develop

.PHONY: sync-direct-runtime-deps
sync-direct-runtime-deps:
	@echo Updating 'requirements/runtime-deps.in' from 'setup.cfg'... >&2
	@echo '# Extracted from `setup.cfg` via `make sync-direct-runtime-deps`' > requirements/runtime-deps.in
	@echo >> requirements/runtime-deps.in
	@python -c 'from configparser import ConfigParser; from itertools import chain; from pathlib import Path; cfg = ConfigParser(); cfg.read_string(Path("setup.cfg").read_text()); print("\n".join(line.strip() for line in chain(cfg["options"].get("install_requires").splitlines(), "\n".join(cfg["options.extras_require"].values()).splitlines()) if line.strip()))' \
		>> requirements/runtime-deps.in