# This file is placed in the Public Domain.


import os
import unittest


from obj import NoFile, NoModule, NoType, Db, Object, gettype, hook, load, last, oqn, save


class Test_Object(unittest.TestCase):

    def test_NoFile(self):
        with self.assertRaises(NoFile):
            o = Object()
            o.key = "value"
            p = save(o)
            p += os.sep
            oo = Object()
            load(oo, p)

    def test_NoType(self):
        with self.assertRaises(NoType):
            o = Object()
            o.key = "value"
            p = save(o)
            splitted = p.split(os.sep)
            splitted[0] = "obj.Bla"
            pp = os.sep.join(splitted)
            hook(pp)

    def test_NoModule(self):
        with self.assertRaises(NoModule):
            o = Object()
            o.key = "value"
            p = save(o)
            splitted = p.split(os.sep)
            splitted[0] = "bla.Object"
            pp = os.sep.join(splitted)
            hook(pp)
        
    def test_Object(self):
        o = Object()
        self.assertTrue(type(o), Object)

    def test_Object__class__(self):
        pass
        
    def test_Object__contains__(self):
        pass

    def test_Object__default__(self):
        pass

    def test_Object__delattr__(self):
        pass

    def test_Object__delitem__(self):
        pass

    def test_Object__dict__(self):
        pass

    def test_Object__dir__(self):
        pass

    def test_Object__doc__(self):
        pass

    def test_Object__eq__(self):
        pass

    def test_Object__format__(self):
        pass

    def test_Object__ge__(self):
        pass

    def test_Object__getattribute__(self):
        pass

    def test_Object__getitem__(self):
        pass

    def test_Object___gt__(self):
        pass

    def test_Object__hash__(self):
        pass
 
    def test_Object__init__(self):
        pass

    def test_Object__init_subclass__(self):
        pass

    def test_Object__iter__(self):
        pass

    def test_Object__le__(self):
        pass

    def test_Object__len__(self):
        pass

    def test_Object__lt__(self):
        pass

    def test_Object__module__(self):
        pass

    def test_Object__ne__(self):
        pass

    def test_Object__new__(self):
        pass

    def test_Object__oqn__(self):
        pass

    def test_Object__otype__(self):
        pass

    def test_Object__reduce__(self):
        pass

    def test_Object__reduce_ex__(self):
        pass

    def test_Object__repr__(self):
        pass

    def test_Object__setattr__(self):
        pass
        
    def test_Object__setitem__(self):
        pass

    def test_Object__sizeof__(self):
        pass

    def test_Object__slots__(self):
        pass

    def test_Object__stp__(self):
        pass

    def test_Object__str__(self):
        pass

    def test_Object__subclasshook__(self):
        pass

    def test_Default(self):
        pass

    def test_List(self):
        pass

    def test_Db(self):
        pass

    def test_cdir(self):
        pass

    def test_edit(self):
        pass

    def test_fmt(self):
        pass

    def test_fns(self):
        pass

    def test_get(self):
        pass

    def test_gettype(self):
        pass

    def test_hook(self):
        pass

    def test_keys(self):
        pass

    def test_items(self):
        pass

    def test_last(self):
        pass

    def test_load(self):
        pass

    def test_register(self):
        pass

    def test_save(self):
        pass

    def test_set(self):
        pass

    def test_update(self):
        pass

    def test_values(self):
        pass
   