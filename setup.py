from setuptools import setup, find_packages
import io

import simpledash


def read_lines(file_path):
    with open(file_path) as fp:
        return [line.strip() for line in fp]


setup(
    name="simpledash",
    version=simpledash.__version__,
    author="Przemyslaw Pastuszka",
    author_email="pastuszka.przemyslaw@gmail.com",
    license="MIT",
    url="https://github.com/rtshadow/simple-dash",
    description=(
        "Library to simplify building Plotly Dash applications"
    ),
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    packages=find_packages(exclude=["tests*", "examples*"]),
    install_requires=read_lines("requirements.txt"),
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Dash",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ]
)
