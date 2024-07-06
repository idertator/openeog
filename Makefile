VERSION=1.0.2

all: art format

clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	find . | grep -E '(__pycache__|\.pyc|\.pyo$))' | xargs rm -rf

format:
	black ./openeog
	isort ./openeog

tags::
	ctags -R .

art:
	pyside6-rcc res/recorder.qrc -o openeog/recorder/gui/resources.py

installer:
	python3 setup.py sdist
	mv dist/*.tar.gz install/
	rmdir dist
	makeself ./install openeog-${VERSION}.run "Open EOG" ./install.sh
	rm install/*.tar.gz

install-requirements:
	( \
 	  source .venv/bin/activate; \
  	  uv pip install -r requirements/devel.txt; \
	)

update-requirements:
	( \
 	  source .venv/bin/activate; \
  	  uv pip install --upgrade -r requirements/devel.txt; \
	)

notebook:
	( \
 	  source .venv/bin/activate; \
	  jupyter notebook; \
	)

develop:
	uv pip install -e .

build:
	( \
 	  source .venv/bin/activate; \
	  python -m build; \
	)
