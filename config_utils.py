import json
from mmcv import Config

def json_to_dict(json_file):
    with open(json_file) as f:
        return json.load(f)

def cfg_to_dict(cfg_file):
    return Config._file2dict(cfg_file)[0]