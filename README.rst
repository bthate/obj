README
######

NAME
====

     **OBJ** - python3 object library

INSTALL
=======

     sudo pip3 install obj

DESCRIPTION
===========

The obj package provides a namespace you can use to program objects 
under python3, an Object class, that mimics a dict while using 
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction.
Methods are factored out into functions to have a clean namespace to read
JSON data into.

basic usage is this::

>>> from kmd.obj import Object
>>> o = Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> from kmd.obj import Object, load, save
>>> o = Object()
>>> o.key = "value"
>>> p = save(o)
>>> oo = Object()
>>> load(oo, p)
>>> oo.key
>>> 'value'

great for giving objects peristence by having their state stored in files.

FILES
=====

| obj.py


COPYRIGHT
=========

**OBJ** is placed in the Public Domain, no Copyright, no LICENSE.


AUTHOR
======

Bart Thate 

