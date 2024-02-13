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

requirements:
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt update -y
	sudo apt install -y build-essential python3.11-full python3.11-dev ruby libdouble-conversion-dev
	sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 110
	sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 100
	sudo gem install fpm

environment:
	rm -rf .venv
	python3.11 -m venv .venv
	( \
       source .venv/bin/activate; \
       pip install -r requirements.txt; \
	   pip install --upgrade pip; \
    )

deb:
	# easy_install --editable --build-directory . "$(NAME)==$(VERSION)"
	python setup.py bdist
	tar -zxf dist/bsp-eog-$(VERSION).linux-$(shell uname -m).tar.gz
	fpm -s dir -t deb -n $(NAME) -v $(VERSION) -p python-$(NAME)-VERSION_ARCH.deb -d "python" usr

