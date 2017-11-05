#!/usr/bin/env python
# coding: utf-8**

"""setuptools based setup module for occutils

References
----------
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
http://peterdowns.com/posts/first-time-with-pypi.html

How to upload to PyPi
---------------------
Add download_url to setup parameters
git tag <same version as in __init__.py> -m "Adds a tag so that we can put this on PyPI."
git push --tags origin master
check metadata section of setup.cfg

check the .pypirc is C:/Users/<username> directory on Windows, in $HOME directory on Linux

python setup.py register -r pypitest
python setup.py sdist upload -r pypitest

python setup.py register -r pypi
python setup.py sdist upload -r pypi

Notes
-----
.pypirc should contain the password during the upload, otherwise an error 401 occurs

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import aocxchange

here = path.abspath(path.dirname(__file__))

# Get the long description from the README_SHORT file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=aocxchange.__name__,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=aocxchange.__version__,

    description=aocxchange.__description__,
    long_description=long_description,

    # The project's main homepage.
    url=aocxchange.__url__,
    download_url=aocxchange.__download_url__,

    # Author details
    author=aocxchange.__author__,
    author_email=aocxchange.__author_email__,

    # Choose your license
    license=aocxchange.__license__,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],

    # What does your project relate to?
    keywords='OpenCASCADE pythonocc CAD',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['aocxchange'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['OCC', 'scipy', 'wx'],
    install_requires=['aocutils'],  # OCC, scipy and wx cannot be installed via pip

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': ['pytest', 'coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={'console_scripts': ['sample=sample:main',],},
    entry_points={},

    scripts=['bin/step_to_stl', 'bin/step_to_obj']

    )

