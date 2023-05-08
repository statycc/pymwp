import setuptools

__title__ = "pymwp"
__author__ = "Clément Aubert, Thomas Rubiano, Neea Rusch, Thomas Seiller"
__desc__ = "Implementation of MWP analysis on C code in Python."
__version__ = "0.4.2"

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email='nrusch@augusta.edu',
    packages=['pymwp'],
    entry_points={'console_scripts': ['pymwp = pymwp.__main__:main'], },
    license='GPLv3',
    description=__desc__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/statycc/pymwp',
    project_urls={
        'Bug Tracker': 'https://github.com/statycc/pymwp/issues',
        'Documentation': 'https://statycc.github.io/pymwp/',
        'Source Code': 'https://github.com/statycc/pymwp',
        'Archive': 'https://doi.org/10.5281/zenodo.7879822'
    },
    package_data={"": ["LICENSE"], },
    include_package_data=True,
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Typing :: Typed',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    python_requires=">=3.7",
    install_requires=[
        'pycparser',
        'pycparser-fake-libc'
    ]
)
