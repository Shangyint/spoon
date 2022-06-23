from typing import List
from dataclasses import dataclass
import z3

# current AST
# e   ∈ Expr  ::= e + e | v
# c   ∈ bool  ::= e = e | e >= e | e > e | c ∧ c | c ∨ c
AVAILABLE_OP = {"eq", "gt", "ge"}

class Expr:
    def __hash__(self) -> int:
        return hash(self.__str__())

class BExpr:
    def __hash__(self) -> int:
        return hash(self.__str__())

@dataclass
class AddExpr(Expr):
    a: Expr
    b: Expr

    def __str__(self) -> str:
        return f"(+ {self.a} {self.b})"
    
    def __hash__(self) -> int:
        return super().__hash__()

# available terms
fds = ["dummy1", "dummy2"]

@dataclass
class V(Expr):
    fd: List[str]

    def __str__(self) -> str:
        return "_".join(self.fd)
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def toZ3(self):
        return z3.Int(self.__str__())

@dataclass
class IntV(Expr):
    i: int

    def __str__(self) -> str:
        return str(self.i)

    def __hash__(self) -> int:
        return super().__hash__()

    def toZ3(self):
        return z3.IntVal(self.i)

@dataclass
class EqExpr(BExpr):
    a: Expr
    b: Expr

    def __str__(self) -> str:
        return f"(= {self.a} {self.b})"

    def __hash__(self) -> int:
        return super().__hash__()
    
    def toZ3(self):
        return self.a.toZ3() == self.b.toZ3()

@dataclass
class GeExpr(BExpr):
    a: Expr
    b: Expr

    def __str__(self) -> str:
        return f"(>= {self.a} {self.b})"

    def __hash__(self) -> int:
        return super().__hash__()
    
    def toZ3(self):
        return self.a.toZ3() >= self.b.toZ3()

@dataclass
class GtExpr(BExpr):
    a: Expr
    b: Expr

    def __str__(self) -> str:
        return f"(> {self.a} {self.b})"

    def __hash__(self) -> int:
        return super().__hash__()
    
    def toZ3(self):
        return self.a.toZ3() > self.b.toZ3()

@dataclass
class AndExpr(BExpr):
    a: BExpr
    b: BExpr

@dataclass
class OrExpr(BExpr):
    a: BExpr
    b: BExpr

    def __str__(self) -> str:
        return f"(or {self.a} {self.b})"
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def toZ3(self):
        return z3.Or(self.a.toZ3(), self.b.toZ3())

@dataclass
class BoolExpr(BExpr):
    b: bool

    def __str__(self) -> str:
        return str(self.b)
    
    def __hash__(self) -> int:
        return super().__hash__()

# @dataclass
# class NotExpr(BExpr):
#     a: Expr
#     b: Expr

# @dataclass
# class LeExpr(Expr):
#     a: Expr
#     b: Expr

# @dataclass
# class LtExpr(Expr):
#     a: Expr
#     b: Expr