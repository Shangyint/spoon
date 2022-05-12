from typing import NamedTuple, Set
from constraint_expr import SymExpr
from shape_inference import infer_shape


class Constraint_Type(NamedTuple):
    ty: type
    constraint: Set[SymExpr]

# data should be of type dict
def gen_constraint_type(data):
    return Constraint_Type(infer_shape(data), set())


def check_type(data, type):
    # check type
    # check constraint
    pass