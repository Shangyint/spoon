import typing
from typing import NamedTuple
import constraint_expr
NoneType = type(None)

class Norm_cfg(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    requires_grad: bool


class Init_cfg(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    checkpoint: str


class Backbone(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    depth: int
    num_stages: int
    out_indices: typing.List[int]
    frozen_stages: int
    norm_cfg: Norm_cfg
    norm_eval: bool
    style: str
    init_cfg: Init_cfg
    strides: typing.Union[typing.List[int], NoneType]
    dilations: typing.Union[typing.List[int], NoneType]


class Neck(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    in_channels: typing.List[int]
    out_channels: int
    num_outs: int


class Anchor_generator(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    scales: typing.List[int]
    ratios: typing.List[float]
    strides: typing.List[int]


class Bbox_coder(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    target_means: typing.List[float]
    target_stds: typing.List[float]


class Loss_cls(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    use_sigmoid: bool
    loss_weight: float


class Loss_bbox(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    loss_weight: float


class Rpn_head(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    in_channels: int
    feat_channels: int
    anchor_generator: Anchor_generator
    bbox_coder: Bbox_coder
    loss_cls: Loss_cls
    loss_bbox: Loss_bbox


class Roi_layer(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    output_size: int
    sampling_ratio: int


class Bbox_roi_extractor(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    roi_layer: Roi_layer
    out_channels: int
    featmap_strides: typing.List[int]


class Bbox_head(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    in_channels: int
    fc_out_channels: typing.Union[int, NoneType]
    roi_feat_size: int
    num_classes: int
    bbox_coder: Bbox_coder
    reg_class_agnostic: bool
    loss_cls: Loss_cls
    loss_bbox: Loss_bbox
    with_avg_pool: typing.Union[bool, NoneType]


class Shared_head(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    depth: int
    stage: int
    stride: int
    dilation: int
    style: str
    norm_cfg: Norm_cfg
    norm_eval: bool


class Roi_head(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    bbox_roi_extractor: Bbox_roi_extractor
    bbox_head: Bbox_head
    shared_head: typing.Union[Shared_head, NoneType]


class Assigner(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    pos_iou_thr: float
    neg_iou_thr: float
    min_pos_iou: float
    match_low_quality: bool
    ignore_iof_thr: int


class Sampler(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    num: int
    pos_fraction: float
    neg_pos_ub: int
    add_gt_as_proposals: bool


class Rpn(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    assigner: Assigner
    sampler: Sampler
    allowed_border: int
    pos_weight: int
    debug: bool


class Nms(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    iou_threshold: float


class Rpn_proposal(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    nms_pre: int
    max_per_img: int
    nms: Nms
    min_bbox_size: int


class Rcnn(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    assigner: Assigner
    sampler: Sampler
    pos_weight: int
    debug: bool


class Train_cfg(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    rpn: Rpn
    rpn_proposal: Rpn_proposal
    rcnn: Rcnn


class Test_cfg(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    rpn: Rpn
    rcnn: Rcnn


class Model(NamedTuple):
    constraints: typing.Set[constraint_expr.SymExpr]
    type: str
    backbone: Backbone
    neck: typing.Union[Neck, NoneType]
    rpn_head: Rpn_head
    roi_head: Roi_head
    train_cfg: Train_cfg
    test_cfg: Test_cfg

