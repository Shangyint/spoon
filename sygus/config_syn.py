# This should be able to parse a config file to a CSV
from sygus_gen import gen_BExpr
from cfg import check_sat, check_unsat

def parse_config():
    pass

def predicate_learner():
    depth_max = 4
    for depth in range(depth_max):
        # generate predicates
        while True:
            gen_BExpr(depth)


def predicate_verifier(predicate, gconfigs, bconfigs):
    if all(map(lambda x: check_sat(predicate, x), gconfigs)) and\
        any(map(lambda x: check_unsat(predicate, x), bconfigs)):
        return True
    else:
        return False

# how many configuration files are needed?
def constraint_verifier():
    pass
