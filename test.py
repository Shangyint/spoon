from shape_inference import *

config_path = "/home/shangyit/projects/DNNSyn/analysis/complete_configs"
config_file = "faster_rcnn_r50_fpn_1x_coco.py"

test = toJsonObj("test.json")
print(infer_shape(test, "test").__annotations__)