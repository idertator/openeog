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
	pyside6-rcc res/resources.qrc -o openeog/gui/resources.py

installer:
	python3 setup.py sdist
	mv dist/*.tar.gz install/
	rmdir dist
	makeself ./install openeog-${VERSION}.run "Open EOG" ./install.sh
	rm install/*.tar.gz

install_requirements:
	( \
 	  source .venv/bin/activate; \
  	  uv pip install -r requirements.txt; \
	)

update_requirements:
	( \
 	  source .venv/bin/activate; \
  	  uv pip install --upgrade -r requirements.txt; \
	)

notebook:
	( \
 	  source .venv/bin/activate; \
	  jupyter notebook; \
	)

develop:
	( \
 	  source .venv/bin/activate; \
	  python setup.py develop; \
	)
