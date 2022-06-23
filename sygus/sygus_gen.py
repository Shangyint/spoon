from cfg import *
import random

def gen_from_ty(ty, depth):
    if issubclass(ty, BExpr):
        return gen_BExpr(depth)
    elif issubclass(ty, Expr):
        return gen_Expr(depth)
    else:
        raise RuntimeError(f"Missing type {ty}")

def gen_members(cls, depth):
    ops = []
    for ty in cls.__annotations__.values():
        opv = gen_from_ty(ty, depth)
        ops.append(opv)

    if not all(ops):
        return None

    return ops

Expr_cls = [AddExpr, V]
def gen_Expr(depth):
    candidate_cls = random.choice(Expr_cls)
    if depth == 0 or candidate_cls is V:
        return V(random.choice(fds))
    else:
        members = gen_members(candidate_cls, depth - 1)
        return candidate_cls(*members) if members else None


BExpr_cls = [EqExpr, GtExpr, GeExpr, OrExpr, BoolExpr]
def gen_BExpr(depth):
    candidate_cls = random.choice(BExpr_cls)
    if depth == 0 or candidate_cls == BoolExpr:
        return BoolExpr(bool(random.getrandbits(1)))

    members = gen_members(candidate_cls, depth-1)
    return candidate_cls(*members) if members else None

def gen_all(depth):
    s = set()
    while True:
        bexpr = gen_BExpr(depth)
        # print(hash(bexpr))
        # print({str(e): hash(e) for e in s})
        # print(bexpr in s)
        if bexpr not in s:
            print(bexpr)
            s.add(bexpr)

# gen_all(2)