# This file is placed in the Public Domain.

"python3 object library"

# imports

import datetime
import json as js
import os
import pathlib
import sys
import types
import time
import uuid

# exceptions

class NoFile(Exception):

    pass


class NoModule(Exception):

    pass


class NoType(Exception):

    pass


def __dir__():
    return ("NoFile","NoModule","NoType", "Object", "Default", "List" , "Db", "cdir", "edit", "fmt", "fns", "gettype", "hook", "get", "keys", "items", "last", "load", "register", "save", "set", "update", "values")

# classes

class Object:

    __slots__ = ("__dict__", "__stp__", "__otype__")

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__otype__ = gettype(self)
        self.__stp__ = os.path.join(
            gettype(self),
            str(uuid.uuid4()),
            os.sep.join(str(datetime.datetime.now()).split()),
        )
        if args:
            self.__dict__.update(args[0])

    @staticmethod
    def __default__(oo):
        if isinstance(oo, Object):
            return vars(oo)
        if isinstance(oo, dict):
            return oo.items()
        if isinstance(oo, list):
            return iter(oo)
        if isinstance(oo, (type(str), type(True), type(False), type(int), type(float))):
            return oo
        return oqn(oo)

    def __oqn__(self):
        return "<%s.%s object at %s>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self)),
        )

    def __contains__(self, k):
        if k in keys(self):
            return True
        return False

    def __delitem__(self, k):
        if k in self:
            del self.__dict__[k]

    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __repr__(self):
        return json(self)

    def __str__(self):
        return str(self.__dict__)


class List(Object):

    def append(self, key, value):
        if key not in self:
            self[key] = []
        if value in self[key]:
            return
        if isinstance(value, list):
            self[key].extend(value)
        else:
            self[key].append(value)

    def update(self, d):
        for k, v in d.items():
            self.append(k, v)


class Default(Object):

    def __getattr__(self, k):
        try:
            return super().__getitem__(k)
        except KeyError:
            self[k] = ""
            return self[k]

class Cfg(Default):

     wd = ""

class Db(Object):

    def all(self, otype, selector=None, index=None, timed=None):
        nr = -1
        if selector is None:
            selector = {}
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

    def deleted(self, otype):
        for fn in fns(otype):
            o = hook(fn)
            if "_deleted" not in o or not o._deleted:
                continue
            yield fn, o

    def every(self, selector=None, index=None, timed=None):
        if selector is None:
            selector = {}
        nr = -1
        wd = getmain("wd")
        for otype in os.listdir(os.path.join(wd, "store")):
            for fn in fns(otype, timed):
                o = hook(fn)
                if selector and not search(o, selector):
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                nr += 1
                if index is not None and nr != index:
                    continue
                yield fn, o

    def find(self, otype, selector=None, index=None, timed=None):
        if selector is None:
            selector = {}
        got = False
        nr = -1
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            got = True
            yield (fn, o)
        if got:
            return (None, None)
        return None

    def lastmatch(self, otype, selector=None, index=None, timed=None):
        res = sorted(
            find(otype, selector, index, timed), key=lambda x: fntime(x[0])
        )
        if res:
            return res[-1]
        return (None, None)

    def lastobject(self, o):
        return self.lasttype(o.__otype__)

    def lasttype(self, otype):
        fnn = fns(otype)
        if fnn:
            return hook(fnn[-1])
        return None

    def lastfn(self, otype):
        fn = fns(otype)
        if fn:
            fnn = fn[-1]
            return (fnn, hook(fnn))
        return (None, None)

# utilities

def cdir(path):
    if os.path.exists(path):
        return
    if path.split(os.sep)[-1].count(":") == 2:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def fns(name, timed=None):
    if not name:
        return []
    assert Cfg.wd
    p = os.path.join(Cfg.wd, "store", name) + os.sep
    res = []
    d = ""
    for rootdir, dirs, _files in os.walk(p, topdown=False):
        if dirs:
            d = sorted(dirs)[-1]
            if d.count("-") == 2:
                dd = os.path.join(rootdir, d)
                fls = sorted(os.listdir(dd))
                if fls:
                    p = os.path.join(dd, fls[-1])
                    if (
                        timed
                        and "from" in timed
                        and timed["from"]
                        and fntime(p) < timed["from"]
                    ):
                        continue
                    if timed and timed.to and fntime(p) > timed.to:
                        continue
                    res.append(p)
    return sorted(res, key=fntime)

def fntime(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        t += float("." + rest)
    else:
        t = 0
    return t

def gettype(o):
    return str(type(o)).split()[-1][1:-2]


def hook(hfn):
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    fn = os.sep.join(oname)
    mn, cn = cname.rsplit(".", 1)
    mod = sys.modules.get(mn, None)
    if not mod:
        raise NoModule(mn)
    t = getattr(mod, cn, None)
    if t:
        o = t()
        load(o, fn)
        return o
    raise NoType(cname)

# factored out methods and some

def edit(self, setter, skip=True, skiplist=None):
    if skiplist is None:
        skiplist = []
    count = 0
    for key, v in items(setter):
        if skip and v == "":
            del self[key]
        if key in skiplist:
            continue
        count += 1
        if v in ["True", "true"]:
            self[key] = True
        elif v in ["False", "false"]:
            self[key] = False
        else:
            self[key] = v
    return count


def fmt(self, keyz=None, empty=True, skip=None):
    if keyz is None:
        keyz = keys(self)
    if not keyz:
        keyz = ["txt"]
    if skip is None:
        skip = []
    res = []
    txt = ""
    for key in sorted(keyz):
        if key in skip:
            continue
        if key in self:
            val = self[key]
            if empty and not val:
                continue
            val = str(val).strip()
            res.append((key, val))
    result = []
    for k, v in res:
        result.append("%s=%s%s" % (k, v, " "))
    txt += " ".join([x.strip() for x in result])
    return txt.strip()


def get(self, key, default=None):
    return self.__dict__.get(key, default)


def keys(self):
    return self.__dict__.keys()


def items(self):
    try:
        return self.__dict__.items()
    except AttributeError:
        return self.items()


def json(self):
    s = js.dumps(self.__dict__, default=self.__default__, sort_keys=True)
    s = s.replace("'", "\\\"")
    s = s.replace('"', "'")
    return s


def last(self):
    db = Db()
    t = str(gettype(self))
    path, l = db.lastfn(t)
    if l:
        update(self, l)
    if path:
        splitted = path.split(os.sep)
        stp = os.sep.join(splitted[-4:])
        return stp
    return None


def load(self, opath):
    if opath.count(os.sep) != 3:
        raise NoFile(opath)
    assert Cfg.wd
    splitted = opath.split(os.sep)
    stp = os.sep.join(splitted[-4:])
    lpath = os.path.join(Cfg.wd, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r") as ofile:
            d = js.load(ofile, object_hook=Object)
            update(self, d)
    self.__stp__ = stp


def oqn(self):
    return Object.__oqn__(self)


def register(self, k, v):
    self[str(k)] = v


def save(self, tab=False):
    assert Cfg.wd
    prv = os.sep.join(self.__stp__.split(os.sep)[:2])
    self.__stp__ = os.path.join(prv, os.sep.join(str(datetime.datetime.now()).split()))
    opath = os.path.join(Cfg.wd, "store", self.__stp__)
    cdir(opath)
    with open(opath, "w") as ofile:
        js.dump(self.__dict__, ofile, default=self.__default__, indent=4, sort_keys=True)
    os.chmod(opath, 0o444)
    return self.__stp__


def search(self, s):
    ok = False
    for k, v in items(s):
        vv = getattr(self, k, None)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok

def set(self, key, value):
    self.__dict__[key] = value


def update(self, data):
    try:
        return self.__dict__.update(vars(data))
    except TypeError:
        return self.__dict__.update(data)


def values(self):
    return self.__dict__.values()

