all: art format

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

format:
	black ./bsp
	isort ./bsp

tags::
	ctags -R .

art:
	pyside6-rcc res/icons.qrc -o bsp/gui/icons.py
