import json
from collections import namedtuple
from typing import Any, List, Union
from functools import reduce

# Use with caution, might have false positives
def isinstance_namedtuple(obj) -> bool:
    return (
            isinstance(obj, tuple) and
            hasattr(obj, '_asdict') and
            hasattr(obj, '_fields')
    )


def toJsonObj(json_file):
    with open(json_file) as f:
        return json.load(f)

def unify(ft, st):
    return st

def infer_shape(obj, name=""):
    if type(obj) is dict:
        ks = []
        ts = []
        for (k, v) in obj.items():
            ks.append(k)
            ts.append(infer_shape(v, k))
        print(ks)
        print(ts)
        return namedtuple(name, ks)(*ts)
    elif type(obj) is list or type(obj) is tuple:
        if len(obj) == 0:
            return List[Any]
        s = set()
        nt = Any
        for e in obj:
            et = infer_shape(e, name)
            if isinstance_namedtuple(et):
                nt = unify(nt, et)
            else:
                s.add(et)
        return List[reduce(unify, s, Any)]
    else:
        return type(obj)
    


def test():
    print(infer_shape(toJsonObj("test.json"), "test"))

test()