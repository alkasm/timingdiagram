from setuptools import setup, find_packages

setup(
    name="timingdiagrams",
    version="0.2.1",
    author="Alexander Reynolds",
    install_requires=['sortedcollections'],
    packages=find_packages(),
    description="Temporal boolean algebra",
)
