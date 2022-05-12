import typing
from typing import NamedTuple


class Norm_cfg(NamedTuple):
    type: str
    requires_grad: bool


class Init_cfg(NamedTuple):
    type: str
    checkpoint: str


class Backbone(NamedTuple):
    type: str
    depth: int
    num_stages: int
    strides: typing.Union[typing.List[int], NoneType]
    dilations: typing.Union[typing.List[int], NoneType]
    out_indices: typing.List[int]
    frozen_stages: int
    norm_cfg: Norm_cfg
    norm_eval: bool
    style: str
    init_cfg: Init_cfg


class Anchor_generator(NamedTuple):
    type: str
    scales: typing.List[int]
    ratios: typing.List[float]
    strides: typing.List[int]


class Bbox_coder(NamedTuple):
    type: str
    target_means: typing.List[float]
    target_stds: typing.List[float]


class Loss_cls(NamedTuple):
    type: str
    use_sigmoid: bool
    loss_weight: float


class Loss_bbox(NamedTuple):
    type: str
    loss_weight: float


class Rpn_head(NamedTuple):
    type: str
    in_channels: int
    feat_channels: int
    anchor_generator: Anchor_generator
    bbox_coder: Bbox_coder
    loss_cls: Loss_cls
    loss_bbox: Loss_bbox


class Roi_layer(NamedTuple):
    type: str
    output_size: int
    sampling_ratio: int


class Bbox_roi_extractor(NamedTuple):
    type: str
    roi_layer: Roi_layer
    out_channels: int
    featmap_strides: typing.List[int]


class Bbox_head(NamedTuple):
    type: str
    with_avg_pool: typing.Union[bool, NoneType]
    roi_feat_size: int
    in_channels: int
    num_classes: int
    bbox_coder: Bbox_coder
    reg_class_agnostic: bool
    loss_cls: Loss_cls
    loss_bbox: Loss_bbox
    fc_out_channels: typing.Union[int, NoneType]


class Roi_head(NamedTuple):
    type: str
    shared_head: typing.Union[shape_inference.shared_head, NoneType]
    bbox_roi_extractor: Bbox_roi_extractor
    bbox_head: Bbox_head


class Assigner(NamedTuple):
    type: str
    pos_iou_thr: float
    neg_iou_thr: float
    min_pos_iou: float
    match_low_quality: bool
    ignore_iof_thr: int


class Sampler(NamedTuple):
    type: str
    num: int
    pos_fraction: float
    neg_pos_ub: int
    add_gt_as_proposals: bool


class Rpn(NamedTuple):
    assigner: Assigner
    sampler: Sampler
    allowed_border: int
    pos_weight: int
    debug: bool


class Nms(NamedTuple):
    type: str
    iou_threshold: float


class Rpn_proposal(NamedTuple):
    nms_pre: int
    max_per_img: int
    nms: Nms
    min_bbox_size: int


class Rcnn(NamedTuple):
    assigner: Assigner
    sampler: Sampler
    pos_weight: int
    debug: bool


class Train_cfg(NamedTuple):
    rpn: Rpn
    rpn_proposal: Rpn_proposal
    rcnn: Rcnn


class Test_cfg(NamedTuple):
    rpn: Rpn
    rcnn: Rcnn


class Model(NamedTuple):
    type: str
    backbone: Backbone
    rpn_head: Rpn_head
    roi_head: Roi_head
    train_cfg: Train_cfg
    test_cfg: Test_cfg
    neck: typing.Union[shape_inference.neck, NoneType]

