import json
from typing import Any, List, Union, NamedTuple
import typing
from functools import reduce

############################################################################
# Implementation of Types from data's shape inference algorithm for json
# https://arxiv.org/pdf/1605.02941.pdf
# TODO:
# 1. Support row variable unification ?
# 2. Support labelled top types
############################################################################

# ⊥ in the paper
class Bottom:
    pass

# null in the paper
NoneType = type(None)

# Use with caution, might have false positives
def isnamedtuple(obj) -> bool:
    return (
            issubclass(obj, tuple) and
            hasattr(obj, '_asdict') and
            hasattr(obj, '_fields')
    )


def toJsonObj(json_file):
    with open(json_file) as f:
        return json.load(f)

def is_nullable(ty):
    if typing.get_origin(ty) is Union:
        # in python, Optional[T] == Union[T, NoneType]
        if NoneType in typing.get_args(ty):
            return True
    return False

def ceil_ty(ty):
    return ty if is_nullable(ty) else Union[ty, NoneType]

def floor_ty(ty):
    if is_nullable(ty):
        tylist = tuple(T for T in typing.get_args(ty) if T is not NoneType)
        if len(tylist) == 1:
            return tylist[0]
        elif len(tylist) > 1:
            pass
            # return Union[*ty]
    else:
        return ty

def unify(ft, st):
    print(f"unifying {ft}, {st}")
    # csh(σ, σ) = σ
    if ft == st:
        return ft
    # csh([σ_1], [σ_2]) = [csh(σ_1, σ_2)]
    elif typing.get_origin(ft) == typing.get_origin(st) == list:
        eft, est = typing.get_args(ft)[0], typing.get_args(st)[0]
        return List[unify(eft, est)]
    # csh(⊥, σ) = csh(σ, ⊥) = σ
    elif ft is Bottom:
        return st
    elif st is Bottom:
        return ft
    # csh(null, σ) = csh(σ, null) = ⌈σ⌉ 
    elif (ft is NoneType or st is NoneType) and ft != st:
        return ceil_ty(ft) if ft else ceil_ty(st)
    # csh(float, int) = csh(int, float) = float 
    elif (ft, st) == (int, float) or (ft, st) == (float, int):
        return float
    #  csh(σ2, nullable<σˆ1>) = csh(nullable<σˆ1> , σ2) = ⌈csh(σˆ1, σ2)⌉
    elif is_nullable(ft) or is_nullable(st):
        fft = floor_ty(ft) if is_nullable(ft) else ft
        fst = floor_ty(st) if is_nullable(st) else st
        return floor_ty(fft, fst)
    # csh(v {v1: σ1, ..., vn: σn}, v {v1: σ1', ..., vn: σn'})
    #     = v {v1: csh(σ1, σ1'), ..., vn: csh(σn, σn')}
    elif isnamedtuple(ft) and isnamedtuple(st) and ft.__name__ == st.__name__:
        ts = dict()
        ft_dict, st_dict = ft.__annotations__, st.__annotations__
        for (k, v) in ft_dict.items():
            ts[k] = unify(v, st_dict.get(k, NoneType))
        for (k, v) in st_dict.items():
            if k not in ts:
                ts[k] = unify(v, NoneType)
        print(NamedTuple(ft.__name__, ts.items()).__annotations__)
        return NamedTuple(ft.__name__, ts.items())
    else:
        raise RuntimeError(f"Unify: Unhandled typing relation {ft} and {st}")


# TODO: row variable unification ?
def infer_shape(obj, name=""):
    if type(obj) is dict:
        ts = []
        for (k, v) in obj.items():
            ts.append((k, infer_shape(v, k)))
        return NamedTuple(name, ts)
    elif type(obj) is list or type(obj) is tuple:
        if len(obj) == 0:
            return List[Bottom]
        s = set()
        for e in obj:
            et = infer_shape(e, name)
            s.add(et)
        return List[reduce(unify, s, Bottom)]
    else:
        return type(obj)
