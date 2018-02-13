"""
A setuptools based setup module for django_mongodb_odm
"""
import re
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def read(*parts):
    with open(path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='django_mongodb_odm',  # Required
    version=find_version("django_mongodb_odm", "__init__.py"),  # Required
    description='Simple object-document-mapper for django and MongoDB',  # Required
    long_description=long_description,  # Optional
    url='https://github.com/akhilsp/django_mongoDB_ODM',  # Optional
    author='akhilsp',  # Optional
    author_email='spillaiakhil@gmail.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='django mongodb odm',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    install_requires=[  # Optional
        'django',
        'pymongo'
    ],
)
