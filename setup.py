from setuptools import setup, find_packages

setup(
    name='dftparse',
    version='0.2.1',
    description='Library for parsing Density Functional Theory calculations',
    url='https://github.com/CitrineInformatics/dftparse',
    install_requires=[],
    extras_require={},
    packages=find_packages(exclude=('docs'))
)
