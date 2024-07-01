from setuptools import setup


def readme():
    with open("README.md", "rt") as f:
        return f.read()


def requirements():
    with open("requirements.txt", "rt") as f:
        return f.read().strip().split("\n")


setup(
    name="bsp-eog",
    version="1.2.0",
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
        "bsp.core.biomarkers",
        "bsp.core.models",
        "bsp.core.models.annotations",
        "bsp.core.models.protocols",
        "bsp.gui",
        "bsp.gui.newrecord",
    ],
    data_files=[
        ("", ["requirements.txt", "README.md"]),
        ("share/icons", ["data/BSPEog.png"]),
        ("share/applications", ["data/BSPEog.desktop"]),
    ],
    install_requires=requirements(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Visualization",
        "Typing :: Typed",
    ],
    python_requires=">=3.10",
    include_package_data=True,
    zip_safe=False,
)
