#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'wheel==0.23.0',
    'argparse>=1.2.1',
    'numpy>=0.9.1',
    'scipy>=0.15.1',
    'more_itertools>=2.2',
    'joblib>=0.8.3-r1',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='changepoint',
    version='0.1.1',
    description='Change point detection in Time series',
    long_description=readme + '\n\n' + history,
    author='Vivek Kulkarni',
    author_email='viveksck@gmail.com',
    url='https://github.com/viveksck/changepoint',
    packages=[
        'changepoint',
        'changepoint.utils'
    ],
    package_dir={'changepoint':
                 'changepoint'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='changepoint',
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
    tests_require=test_requirements
)
