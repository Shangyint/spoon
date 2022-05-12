from shape_inference import *
from config_utils import *

config_path = "/home/shangyit/projects/DNNSyn/analysis/complete_configs"
config_file = "faster_rcnn_r50_fpn_1x_coco.py"
config_file_2 = "faster_rcnn_r50_caffe_c4_1x_coco.py"
cfg = f"{config_path}/{config_file}"
cfg2 = f"{config_path}/{config_file_2}"

with open("model.py", "w") as model:
    print("""import typing
from typing import NamedTuple

""", file=model)
    print(*shape_to_class_def(infer_shape([cfg_to_dict(cfg)["model"], cfg_to_dict(cfg2)["model"]], "model")).values(), sep="\n\n", file=model)