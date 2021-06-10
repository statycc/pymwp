import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymwp",
    version="0.0.1-alpha.1",
    author="Clément Aubert, Thomas Rubiano, Neea Rusch, Thomas Seiller",
    author_email="nrusch@augusta.edu",
    packages=["pymwp"],
    package_data={"": ["LICENSE"],},
    description="Implementation of MWP analysis on C code in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seiller/pymwp",
    project_urls={
        "Bug Tracker": "https://github.com/seiller/pymwp/issues",
        "Documentation": "https://seiller.github.io/pymwp/",
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)