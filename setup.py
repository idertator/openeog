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
    package_data={
        "bsp.adc": [
            "external/Linux64/plux.so",
            "external/LinuxARM32/plux.so",
            "external/LinuxARM64_38/plux.so",
            "external/LinuxARM64_39/plux.so",
            "external/M1_310/bth_macprocess",
            "external/M1_310/plux.so",
            "external/M1_311/bth_macprocess",
            "external/M1_311/plux.so",
            "external/M1_312/bth_macprocess",
            "external/M1_312/plux.so",
            "external/M1_37/bth_macprocess",
            "external/M1_37/plux.so",
            "external/M1_39/bth_macprocess",
            "external/M1_39/plux.so",
            "external/MacOS/Intel310/bth_macprocess",
            "external/MacOS/Intel310/plux.so",
            "external/MacOS/Intel37/plux.so",
            "external/MacOS/Intel38/plux.so",
            "external/MacOS/Intel39/plux.so",
            "external/Win32_37/LibFT4222.dll",
            "external/Win32_37/LibFT4222AB.dll",
            "external/Win32_37/msvcp100.dll",
            "external/Win32_37/msvcr100.dll",
            "external/Win64_37/LibFT4222-64.dll",
            "external/Win64_37/LibFT4222AB-64.dll",
            "external/Win64_37/msvcp100.dll",
            "external/Win64_37/msvcr100.dll",
            "external/Win64_38/LibFT4222-64.dll",
            "external/Win64_38/LibFT4222AB-64.dll",
            "external/Win64_38/msvcp100.dll",
            "external/Win64_38/msvcr100.dll",
        ],
    },
    data_files=[
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
    python_requires=">=3.11",
    include_package_data=True,
    zip_safe=False,
)
