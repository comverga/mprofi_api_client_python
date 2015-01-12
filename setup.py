#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='mprofi_api_client',
    version='0.1.0',
    description='krotki opis',
    long_description=readme + '\n\n' + history,
    author='Materna Communications',
    author_email='biuro@materna.com.pl',
    url='https://github.com/materna/mprofi_api_client',
    packages=[
        'mprofi_api_client',
    ],
    package_dir={'mprofi_api_client':
                 'mprofi_api_client'},
    include_package_data=True,
    install_requires=[],
    license="BSD",
    zip_safe=False,
    keywords='mprofi_api_client',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
)
