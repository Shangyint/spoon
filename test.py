from shape_inference import *
from config_utils import *

config_path = "/home/shangyit/projects/DNNSyn/analysis/complete_configs"
config_file = "faster_rcnn_r50_fpn_1x_coco.py"
cfg = f"{config_path}/{config_file}"

print(*shape_to_class_def(infer_shape(cfg_to_dict(cfg)["model"], "model"), {}).values(), sep="\n\n")