from setuptools import setup


def readme():
    with open("README.md", "rt") as f:
        return f.read()


def requirements():
    with open("requirements.txt", "rt") as f:
        return f.read().strip().split("\n")


setup(
    name="openeog",
    version="1.2.0",
    description="Electrooculographic Recording and Records Processing Platform",
    long_description=readme(),
    author="Roberto Antonio Becerra García",
    author_email="idertator@gmail.com",
    entry_points={
        "gui_scripts": [
            "openeog-recorder = openeog.recorder:main",
            "openeog-editor = openeog.editor:main",
        ],
    },
    packages=[
        "openeog",
        "openeog.core",
        "openeog.core.biomarkers",
        "openeog.core.models",
        "openeog.core.models.annotations",
        "openeog.core.models.protocols",
        "openeog.recorder.adc",
        "openeog.recorder.gui",
        "openeog.recorder.gui.newrecord",
    ],
    data_files=[
        ("", ["requirements.txt", "README.md"]),
        ("share/icons", ["data/OpenEOG-Recorder.png"]),
        ("share/icons", ["data/OpenEOG-Editor.png"]),
        ("share/applications", ["data/OpenEOG-Recorder.desktop"]),
        ("share/applications", ["data/OpenEOG-Editor.desktop"]),
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
