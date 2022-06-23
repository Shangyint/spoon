from sampling.sample_sketch import sample_expr
from sketch import SketchExpr, Param, Constant, Field
from cfg import AVAILABLE_OP, BoolExpr
from spoon.sygus.config_syn import SAMPLE_SIZE
import z3

def sketchsyn(s: SketchExpr, config):
    opset = AVAILABLE_OP
    while opset:
        s.op = opset.pop()
        bexpr = s.to_bexpr()
        print(f"Sampleing {bexpr} from sketch {s}")
        if sample_expr(config, bexpr, SAMPLE_SIZE):
            return bexpr
    return BoolExpr(False)

def testsketch():
    s = SketchExpr([Field(["backbone", "frozen_stages"]), Field(["backbone", "num_stages"])], None)
    cfg = "/home/shangyin/projects/DNNSyn/sampling/faster_rcnn_r50_fpn_1x_coco.py"
    print(sketchsyn(s, cfg))

if __name__ == "__main__":
    testsketch()
