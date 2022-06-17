# This should be able to parse a config file to a CSV
from sampling.sample_single_parameter import sample_once, sample_once_w_constraints
from sygus_gen import gen_BExpr
from cfg import V, AndExpr, GtExpr, GeExpr, check_sat, check_unsat

SAMPLE_SIZE = 10

def parse_config():
    pass

def predicate_learner():
    depth_max = 4
    for depth in range(depth_max):
        # generate predicates
        while True:
            gen_BExpr(depth)

def check_and_refine_bound(cfg, key, lbound, ubound):
    # check if the new bound is valid
    # if not, refine the bound
    for i in range(SAMPLE_SIZE):
        value, succ_ind = sample_once_w_constraints(cfg, key)
        if succ_ind:
            if value < lbound:
                lbound = value
            if value > ubound:
                ubound = value
    return lbound, ubound

#cfg is the original correct config file
def propose_bound(cfg, key):
    valid_values = []
    invalid_values = []
    for i in range(SAMPLE_SIZE):
        # mutate the original config file
        value, succ_ind = sample_once(cfg, key)
        if succ_ind:
            valid_values.append(value)
        else:
            invalid_values.append(value)
    lbound = min(valid_values)
    ubound = max(valid_values)
    lbound, ubound = check_and_refine_bound(cfg, key, lbound, ubound)
    return AndExpr(GeExpr(V(key), lbound), GeExpr(ubound, V(key)))

def sample_relation(cfg, key1, key2):
    pass

def predicate_verifier(predicate, gconfigs, bconfigs):
    if all(map(lambda x: check_sat(predicate, x), gconfigs)) and\
        any(map(lambda x: check_unsat(predicate, x), bconfigs)):
        return True
    else:
        return False

# how many configuration files are needed?
def constraint_verifier():
    pass
