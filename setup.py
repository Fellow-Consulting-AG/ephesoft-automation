# import setuptools


from __future__ import print_function, unicode_literals

from setuptools import find_packages, setup


import sys


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]


if sys.version_info < (3, 7):
    print("Python 3.7 or newer is required", file=sys.stderr)
    sys.exit(1)

# pylint: disable=w0613

command = next((arg for arg in sys.argv[1:] if not arg.startswith("-")), "")
if command.startswith("install") or command in [
    "check",
    "test",
    "nosetests",
    "easy_install",
]:
    forced = "--force" in sys.argv
    if forced:
        print("The argument --force is deprecated. Please discontinue use.")


if "upload" in sys.argv[1:]:
    print("Use twine to upload the package - setup.py upload is insecure")
    sys.exit(1)


#tests_require = open("requirements/test.txt", encoding="utf-8").read().splitlines()


def readme():
    pass
    with open("README.md", encoding="utf-8") as f:
        return f.read()


with open("README.md", "r") as fh:
    long_description = fh.read()

#install_reqs = parse_requirements("requirements.txt")
#reqs = install_reqs


setup(
    name="ephesoftautomation",  # Replace with your own username
    version="1.4",
    author="Fellow Consulting AG",
    author_email="amier.haider@fellow-consulting.de",
    description="Ephesoft Automation package to test extraction results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fellow-Consulting-AG/ion-workflow/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=find_packages("src", exclude=["tests", "tests.*"]),
    package_dir={"": "src"},
    package_data={
        "ephesoftAutomation": [
            "helper/*",
        ]
    },
    entry_points={"console_scripts": ["ephesoftAutomation = ephesoftAutomation.__main__:main"]},
    keywords=["Ephesoft", "EphesoftAutomation"],
    
)