from __future__ import annotations
from typing import List, Tuple
from dataclasses import dataclass
import z3
from abc import ABC, abstractmethod
from collections import defaultdict

class Fresh:
    symbol = defaultdict(lambda: 0)
    @staticmethod
    def fresh(pre: str) -> str:
        Fresh.symbol[pre] += 1
        return f"{pre}{Fresh.symbol[pre]}"

@dataclass(eq=False)
class Expr(ABC):
    ty: type

    @abstractmethod
    def toZ3(self, ctx):
        pass

    @abstractmethod
    def isConcrete(self):
        pass

    @abstractmethod
    def toSMTLib(self):
        pass

    def __add__(self, e):
        assert self.ty == e.ty
        return SymExpr(self.ty, "add", (self, e))

    def __sub__(self, e):
        assert self.ty == e.ty
        return SymExpr(self.ty, "sub", (self, e))

    def __mul__(self, e):
        assert self.ty == e.ty
        return SymExpr(self.ty, "mul", (self, e))

    def __mod__(self, e):
        assert self.ty == e.ty
        return SymExpr(self.ty, "mod", (self, e))

    def __truediv__(self, e):
        assert self.ty == e.ty
        return SymExpr(self.ty, "truediv", (self, e))

    def __eq__(self, e):
        assert self.ty == e.ty
        return SymExpr(self.ty, "eq", (self, e))

    def __neg__(self):
        return SymExpr(self.ty, "neg", (self))

    def __le__(self, e):
        assert self.ty == e.ty
        return SymExpr(bool, "le", (self, e))

    def __lt__(self, e):
        assert self.ty == e.ty    
        return SymExpr(bool, "lt", (self, e))

    def __ge__(self, e):
        assert self.ty == e.ty
        return SymExpr(bool, "ge", (self, e))

    def __gt__(self, e):
        assert self.ty == e.ty
        return SymExpr(bool, "gt", (self, e))

    def __ne__(self, e):
        assert self.ty == e.ty
        return SymExpr(bool, "ne", (self, e))


@dataclass(eq=False)
class _IntV(Expr):
    i: int

    def toZ3(self, ctx):
        return z3.IntVal(self.i, ctx)

    def toSMTLib(self):
        pass

    def isConcrete(self):
        return True

    def __add__(self, e):
        if type(e) is _IntV:
            return IntV(self.i + e.i)
        else:
            return super().__add__(e)

    def __sub__(self, e):
        if type(e) is _IntV:
            return IntV(self.i - e.i)
        else:
            return super().__sub__(e)

    def __mul__(self, e):
        if type(e) is _IntV:
            return IntV(self.i * e.i)
        else:
            return super().__mul__(e)

    def __mod__(self, e):
        if type(e) is _IntV:
            return IntV(self.i % e.i)
        else:
            return super().__mod__(e)

    def __truediv__(self, e):
        if type(e) is _IntV:
            return IntV(self.i / e.i)
        else:
            return super().__truediv__(e)

    def __eq__(self, e):
        if type(e) is _IntV:
            return BoolV(self.i == e.i)
        else:
            return super().__eq__(e)

    def __le__(self, e):
        if type(e) is _IntV:
            return BoolV(self.i <= e.i)
        else:
            return super().__le__(e)

    def __lt__(self, e):
        if type(e) is _IntV:
            return BoolV(self.i < e.i)
        else:
            return super().__lt__(e)

    def __ge__(self, e):
        if type(e) is _IntV:
            return BoolV(self.i <= e.i)
        else:
            return super().__ge__(e)

    def __gt__(self, e):
        if type(e) is _IntV:
            return BoolV(self.i > e.i)
        else:
            return super().__gt__(e)

    def __ne__(self, e):
        if type(e) is _IntV:
            return BoolV(self.i != e.i)
        else:
            return super().__ne__(e)

    # def __neg__(self, e):
    #     if type(e) is _IntV:
    #         return IntV(self.i - e.i)
    #     else:
    #         return super.__neg__(self, e)

def IntV(i: int) -> _IntV:
    return _IntV(int, i)


@dataclass(eq=False)
class SymExpr(Expr):
    op: str
    rands: Tuple[Expr]
    z3Expr: z3.ArithRef = None

    builtin_bop =  {"add": "+", "sub": "-", "mul": "*", "mod": "%", "truediv": "/",
        "eq": "==", "neg": "-", "le": "<=", "lt": "<", "ge": "<=", "gt": ">", "ne": "!="}
    builtin_sop = {"neg": "-"}
    supported_op = {"and", "or", "neg"}

    def toZ3(self, ctx):
        if self.z3Expr is not None and self.z3Expr.ctx == z3.get_ctx(ctx):
            return self.z3Expr
        if self.op in SymExpr.builtin_bop:
            fexpr = self.rands[0].toZ3(ctx)
            sexpr = self.rands[1].toZ3(ctx)
            self.z3Expr = getattr(fexpr, f"__{self.op}__")(sexpr)
            return self.z3Expr
        elif self.op in SymExpr.builtin_sop:
            fexpr = self.rands[0].toZ3(ctx)
            self.z3Expr = getattr(fexpr, f"__{self.op}__")()
            return self.z3Expr
        elif self.op in SymExpr.supported_op:
            if self.op == "and":
                fexpr = self.rands[0].toZ3(ctx)
                sexpr = self.rands[1].toZ3(ctx)
                self.z3Expr = z3.And(fexpr, sexpr)
                return self.z3Expr
            elif self.op == "or":
                fexpr = self.rands[0].toZ3(ctx)
                sexpr = self.rands[1].toZ3(ctx)
                self.z3Expr = z3.Or(fexpr, sexpr)
                return self.z3Expr
            elif self.op == "not":
                fexpr = self.rands[0].toZ3(ctx)
                self.z3Expr = z3.Not(fexpr)
                return self.z3Expr
            raise NotImplementedError(f"z3 operation {self.op} not implemented")
        raise NotImplementedError(f"z3 operation {self.op} not implemented")

    def toSMTLib(self):
        pass

    def isConcrete(self):
        return all(map(lambda e: e.isConcrete(), self.rands))
    
    # Extend And to be variable argument list
    @staticmethod
    def And(t1: Expr, t2: Expr) -> SymExpr:
        return SymExpr(bool, "and", (t1, t2))
    
    @staticmethod
    def Or(t1: Expr, t2: Expr) -> SymExpr:
        return SymExpr(bool, "or", (t1, t2))
    
    @staticmethod
    def Not(t1: Expr) -> SymExpr:
        return SymExpr(bool, "not", (t1))
    
    @staticmethod
    def Allpos(*args):
        res = []
        for arg in args:
            res.append(arg > IntV(0))
        return res

@dataclass(eq=False)
class _BoolV(Expr):
    b: bool

    def toZ3(self, ctx):
        return z3.BoolVal(self.b, ctx)

    def toSMTLib(self):
        pass

    def isConcrete(self):
        return True

def BoolV(b: bool):
    return _BoolV(bool, b)

@dataclass(eq=False)
class SymV(Expr):
    name: str
    z3Expr: z3.ArithRef = None

    def toZ3(self, ctx):
        if self.z3Expr is not None and self.z3Expr.ctx == z3.get_ctx(ctx):
            return self.z3Expr
        if self.ty is int:
            self.z3Expr = z3.Int(self.name, ctx)
            return self.z3Expr
        else:
            raise NotImplementedError(f"z3 type {self.ty} not implemented")

    def toSMTLib(self):
        pass

    def isConcrete(self):
        return False
    
    @staticmethod
    def symvlist(pre: str, length: int, ty: type):
        return [SymV(ty, Fresh.fresh(pre)) for _ in range(length)]
