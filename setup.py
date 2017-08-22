from setuptools import setup, find_packages

setup(
    name='dft_parser',
    version='0.1.0',
    description='Library for parsing Density Functional Theory calculations',
    url='https://github.com/CitrineInformatics/dft-parsers',
    install_requires=[],
    extras_require={},
    packages=find_packages(exclude=('docs'))
)
