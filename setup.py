from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="timingdiagram-alkasm",
    version="0.3.1",
    author="Alexander Reynolds",
    url="https://github.com/alkasm/timingdiagram",    
    install_requires=["sortedcollections"],
    packages=find_packages(),
    description="Temporal boolean algebra",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
