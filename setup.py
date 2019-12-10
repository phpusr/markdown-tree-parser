#!/usr/bin/env python3

import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='markdown-tree-parser',
    version='0.0.1-5',
    author='phpusr',
    author_email='phpusr@gmail.com',
    description='Markdown tree parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/phpusr/markdown-tree-parser',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    test_suite='tests.art_tests'
)
