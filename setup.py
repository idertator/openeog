from setuptools import setup


def readme():
    with open("README.md", "rt") as f:
        return f.read()


def requirements():
    with open("requirements.txt", "rt") as f:
        return f.read().strip().split("\n")


setup(
    name="bsp-eog",
    version="1.0.0",
    description="Electrooculographic Recording and Records Processing Platform",
    long_description=readme(),
    author="Roberto Antonio Becerra García",
    author_email="idertator@gmail.com",
    entry_points={
        "gui_scripts": ["bsp = bsp:main"],
    },
    packages=[
        "bsp",
        "bsp.adc",
        "bsp.core",
        "bsp.gui",
    ],
    install_requires=requirements(),
)
