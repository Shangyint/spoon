from ast import Pass
from dataclasses import dataclass
from typing import Any, List
from cfg import V, BExpr, EqExpr, Expr, GeExpr, GtExpr, IntV

@dataclass
class Param:
    def to_expr(self):
        pass

@dataclass
class SketchExpr(BExpr):
    plist: List[Param]
    op: str

    def __str__(self) -> str:
        return f"Sketch({self.plist}, {self.op})"

    def to_bexpr(self):
        eparam = []
        if all(p.is_concrete for p in self.plist):
            eparam = [p.to_expr() for p in self.plist]
        else:
            raise NotImplementedError(f"Not implemented unconcrete expr")
        a, b = tuple(eparam)
        if self.op == "eq":
            return EqExpr(a, b)
        elif self.op == "gt":
            return GtExpr(a, b)
        elif self.op == "ge":
            return GeExpr(a, b)


@dataclass
class Constant(Param):
    c: Any
    is_concrete = True

    def to_expr(self):
        if isinstance(self.c, int):
            return IntV(self.c)
        else:
            raise NotImplementedError(f"Constant type not implemented: {self.c}")

@dataclass
class Field(Param):
    f: List[str]
    is_concrete = True

    def to_expr(self):
        return V(self.f)
