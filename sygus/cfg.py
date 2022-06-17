from typing import List
from dataclasses import dataclass

# current AST
# e   ∈ Expr  ::= e + e | v
# c   ∈ bool  ::= e = e | e >= e | e > e | c ∧ c | c ∨ c

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
    fd: str

    def __str__(self) -> str:
        return self.fd
    
    def __hash__(self) -> int:
        return super().__hash__()

@dataclass
class Int(Expr):
    i: int

    def __str__(self) -> str:
        return str(self.i)

    def __hash__(self) -> int:
        return super().__hash__()

@dataclass
class EqExpr(BExpr):
    a: Expr
    b: Expr

    def __str__(self) -> str:
        return f"(= {self.a} {self.b})"

    def __hash__(self) -> int:
        return super().__hash__()

@dataclass
class GeExpr(BExpr):
    a: Expr
    b: Expr

    def __str__(self) -> str:
        return f"(>= {self.a} {self.b})"

    def __hash__(self) -> int:
        return super().__hash__()

@dataclass
class GtExpr(BExpr):
    a: Expr
    b: Expr

    def __str__(self) -> str:
        return f"(> {self.a} {self.b})"

    def __hash__(self) -> int:
        return super().__hash__()

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