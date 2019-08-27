from setuptools import setup, find_packages

setup(
    name="timingdiagram",
    version="0.3.0",
    author="Alexander Reynolds",
    install_requires=["sortedcollections"],
    packages=find_packages(),
    description="Temporal boolean algebra",
)
