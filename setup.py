#!/usr/bin/env python
# coding: utf-8

"""setuptools based setup module for aocxchange"""

from setuptools import setup
# To use a consistent encoding
import codecs
from os import path

import aocxchange

here = path.abspath(path.dirname(__file__))

# Get the long description from the README_SHORT file
with codecs.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=aocxchange.__name__,
    version=aocxchange.__version__,
    description=aocxchange.__description__,
    long_description=long_description,
    url=aocxchange.__url__,
    download_url=aocxchange.__download_url__,
    author=aocxchange.__author__,
    author_email=aocxchange.__author_email__,
    license=aocxchange.__license__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'],
    keywords='OpenCASCADE pythonocc CAD',
    packages=['aocxchange',
              'aocxchange.convert',
              'aocxchange.pymesh',
              'aocxchange.ui'],
    install_requires=['OCC', 'numpy', 'scipy', 'corelib', 'wx', 'aocutils'],
    extras_require={
        'dev': [],
        'test': ['pytest', 'coverage'],
    },
    package_data={},
    data_files=[],
    entry_points={},
    scripts=['bin/step_to_stl', 'bin/step_to_obj']
    )
