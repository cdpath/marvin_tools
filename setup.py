#!/usr/bin/env python

from setuptools import setup, find_packages
import marvin_tools
import os


def read(*names):
    values = dict()
    extensions = ['.txt', '.rst']
    for name in names:
        value = ''
        for extension in extensions:
            filename = name + extension
            if os.path.isfile(filename):
                value = open(name + extension).read()
                break
        values[name] = value
    return values

long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(
    name='marvin_tools',
    version=marvin_tools.__version__,
    description='Instant coding answers via the command line',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Documentation",
    ],
    keywords='Convert Marvin CSV to My Clippings.txt',
    author='cdpath',
    author_email='cdpath@outlook.com',
    maintainer='cdpath',
    maintainer_email='cdpath@outlook.com',
    url='https://github.com/cdpath/marvin_tools',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'marvin = marvin_tools.marvin:command_line_runner',
        ]
    },
    install_requires=[]
)
