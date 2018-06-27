# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='indiepaper',
    version='0.1.0',
    description='A "read later" service for micropub endpoints.',
    author='Jonathan LaCour',
    author_email='jonathan@cleverdevil.org',
    install_requires=[
        "pecan",
        "requests",
        "zappa"
    ],
    test_suite='indiepaper',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup'])
)
