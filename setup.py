# This file is placed in the Public Domain.

import os

from setuptools import setup

def read():
    return open("README.rst", "r").read()

def uploadlist(dir):
    upl = []
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl

setup(
    name='kmd',
    version='1',
    url='https://github.com/bthate/kmd',
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    description="write your own commands.",
    long_description=read(),
    license='KMD is placed in the Public Domain, no Copyright, no LICENSE.',
    packages_dir={"": "lib"},
    py_modules=["obj.py"],
    zip_safe=True,
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
