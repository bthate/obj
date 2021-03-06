README
######

NAME
====

**libobj** - python3 object library

INSTALL
=======

sudo pip3 install libobj

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

>>> from obj import Object
>>> o = Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> from obj import Object, load, save
>>> o = Object()
>>> o.key = "value"
>>> p = save(o)
>>> oo = Object()
>>> load(oo, p)
>>> oo.key
>>> 'value'

great for giving objects peristence by having their state stored in files.

>>> from obj import Cfg, Object, save
>>> Cfg.wd = ".test"
>>> o = Object()
>>> save(o)
'obj.Object/e455c143-180e-4b43-bda2-9f09500cedba/2021-08-31/15:31:05.717063'


FILES
=====

obj.py


COPYRIGHT
=========

**libobj** is placed in the Public Domain, no Copyright, no LICENSE.


AUTHOR
======

Bart Thate 

