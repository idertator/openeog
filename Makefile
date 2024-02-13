NAME=bsp-eog
VERSION=1.0.0

all: art format

clean:
	find . | grep -E '(__pycache__|\.pyc|\.pyo$))' | xargs rm -rf

format:
	black ./bsp
	isort ./bsp

tags::
	ctags -R .

art:
	pyside6-rcc res/resources.qrc -o bsp/gui/resources.py

installer:
	python3 setup.py sdist
	mv dist/*.tar.gz install/
	rmdir dist
	makeself ./install bsp-1.0.0.run "BioSignalsPlux EOG" ./install.sh
	rm install/*.tar.gz
