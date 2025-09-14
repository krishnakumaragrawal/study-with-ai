from setuptools import setup, find_packages

with open("./requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="mypackage",
    version="0.1.0",
    author="krishna",
    packages=find_packages(),
    install_requires=requirements,
)