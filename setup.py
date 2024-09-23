# -----------------------------------------------------------------------------
# Copyright (c) 2020-2024 C. Aubert, T. Rubiano, N. Rusch and T. Seiller.
#
# This file is part of pymwp.
#
# pymwp is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pymwp is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pymwp. If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import setuptools
import os

__title__ = "pymwp"
__author__ = "Clément Aubert, Thomas Rubiano, Neea Rusch, Thomas Seiller"
__desc__ = "Implementation of MWP analysis on C code in Python."

with open('README.md', 'r', encoding='utf-8') as fh:
    readme = fh.read()
    start_key, end_key = '<!--include-start-->', '<!--include-end-->'
    start = readme.index(start_key) + len(start_key)
    end = readme.index(end_key)
    long_description = readme[start:end]

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       "pymwp", "version.py")) as fp:
    exec(fp.read())

setuptools.setup(
    name=__title__,
    version=__version__,  # noqa: F821
    author=__author__,
    author_email='nrusch@augusta.edu',
    packages=['pymwp'],
    entry_points={'console_scripts': ['pymwp = pymwp.__main__:main'], },
    license='GPLv3+',
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
    license_files=('LICENSE',),
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
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Typing :: Typed',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        ('License :: OSI Approved :: ' +
         'GNU General Public License v3 or later (GPLv3+)')
    ],
    python_requires=">=3.7",
    install_requires=[
        'pycparser',
        'pycparser-fake-libc'
    ]
)
