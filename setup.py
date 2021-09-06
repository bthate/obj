# This file is placed in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='libobj',
    version='202',
    url='https://github.com/bthate/libobj',
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    description="python3 object library",
    long_description=read(),
    license='libobj is placed in the Public Domain, no Copyright, no LICENSE.',
    packages=["obj"],
    zip_safe=False,
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
