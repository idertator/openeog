from setuptools import setup


def readme():
    with open("README.md", "rt") as f:
        return f.read()


def requirements():
    with open("requirements.txt", "rt") as f:
        return f.read().strip().split("\n")


setup(
    name="bsp-eog",
    version="1.1.0",
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
        "bsp.core.protocols",
        "bsp.gui",
        "bsp.gui.protocols",
    ],
    package_data={
        "bsp.adc": [
            "external/Linux_x86_64/plux.so",
            "external/Darwin_x86_64/bth_macprocess",
            "external/Darwin_x86_64/plux.so",
            "external/Darwin_arm/bth_macprocess",
            "external/Darwin_arm/plux.so",
            "external/Windows_x86_64/LibFT4222-64.dll",
            "external/Windows_x86_64/LibFT4222AB-64.dll",
            "external/Windows_x86_64/msvcp100.dll",
            "external/Windows_x86_64/msvcr100.dll",
        ],
    },
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
