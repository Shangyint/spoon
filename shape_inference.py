import json
from collections import namedtuple
from typing import Any, List, Union
import typing
from functools import reduce

############################################################################
# Implementation of Types from data's shape inference algorithm for json
# https://arxiv.org/pdf/1605.02941.pdf
# TODO:
# 1. Support row variable unification 
# 2. Support nullable types
############################################################################


# Use with caution, might have false positives
def isnamedtuple(obj) -> bool:
    return (
            isinstance(obj, tuple) and
            hasattr(obj, '_asdict') and
            hasattr(obj, '_fields')
    )


def toJsonObj(json_file):
    with open(json_file) as f:
        return json.load(f)


def unify(ft, st):
    # csh(σ, σ) = σ
    if ft == st:
        return ft
    # csh([σ_1], [σ_2]) = [csh(σ_1, σ_2)]
    elif typing.get_origin(ft) == typing.get_origin(st) == list:
        eft, est = typing.get_args(ft)[0], typing.get_args(st)[0]
        return List[unify(eft, est)]
    # csh(⊥, σ) = csh(σ, ⊥) = σ
    # elif ft is None:
    #     return st
    # elif st is None:
    #     return ft        
    # csh(v {v1: σ1, ..., vn: σn}, v {v1: σ1', ..., vn: σn'})
    #     = v {v1: csh(σ1, σ1'), ..., vn: csh(σn, σn')}
    elif isnamedtuple(ft) and isnamedtuple(st):
        ks, ts = [], []
        ft_dict, st_dict = ft._asdict(), st._asdict()
        for (k, v) in ft_dict.items():
            ks.append(k)
            ts.append(unify(v, st_dict.get(k, None)))
        for (k, v) in st_dict.items():
            if k not in ks:
                ks.append(k)
                ts.append(unify(v, None))


# TODO: row variable unification 
def infer_shape(obj, name=""):
    if type(obj) is dict:
        ks, ts = [], []
        for (k, v) in obj.items():
            ks.append(k)
            ts.append(infer_shape(v, k))
        print(ks)
        print(ts)
        return namedtuple(name, ks)(*ts)
    elif type(obj) is list or type(obj) is tuple:
        if len(obj) == 0:
            return List[None]
        s = set()
        for e in obj:
            et = infer_shape(e, name)
            s.add(et)
        return List[reduce(unify, s, None)]
    else:
        return type(obj)
