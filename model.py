import typing
from typing import NamedTuple
import constraint_expr
NoneType = type(None)

class Norm_cfg(NamedTuple):
    type: str
    requires_grad: bool
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Init_cfg(NamedTuple):
    type: str
    checkpoint: str
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Backbone(NamedTuple):
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
    constraints: typing.Set[constraint_expr.SymExpr] = set()

    def construct_cons(self):
        constraints = set(
            constraint_expr.SymExpr.Or(
                constraint_expr.SymExpr(bool, "==", (self.depth, 18)),
                constraint_expr.SymExpr(bool, "==", (self.depth, 34))),
            constraint_expr.SymExpr(bool, "<=", (self.num_stages, 4)),
            constraint_expr.SymExpr(bool, "<=", (1, self.num_stages)),   
        )
        return constraints

class Neck(NamedTuple):
    type: str
    in_channels: typing.List[int]
    out_channels: int
    num_outs: int
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Anchor_generator(NamedTuple):
    type: str
    scales: typing.List[int]
    ratios: typing.List[float]
    strides: typing.List[int]
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Bbox_coder(NamedTuple):
    type: str
    target_means: typing.List[float]
    target_stds: typing.List[float]
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Loss_cls(NamedTuple):
    type: str
    use_sigmoid: bool
    loss_weight: float
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Loss_bbox(NamedTuple):
    type: str
    loss_weight: float
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Rpn_head(NamedTuple):
    type: str
    in_channels: int
    feat_channels: int
    anchor_generator: Anchor_generator
    bbox_coder: Bbox_coder
    loss_cls: Loss_cls
    loss_bbox: Loss_bbox
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Roi_layer(NamedTuple):
    type: str
    output_size: int
    sampling_ratio: int
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Bbox_roi_extractor(NamedTuple):
    type: str
    roi_layer: Roi_layer
    out_channels: int
    featmap_strides: typing.List[int]
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Bbox_head(NamedTuple):
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
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Shared_head(NamedTuple):
    type: str
    depth: int
    stage: int
    stride: int
    dilation: int
    style: str
    norm_cfg: Norm_cfg
    norm_eval: bool
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Roi_head(NamedTuple):
    type: str
    bbox_roi_extractor: Bbox_roi_extractor
    bbox_head: Bbox_head
    shared_head: typing.Union[Shared_head, NoneType]
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Assigner(NamedTuple):
    type: str
    pos_iou_thr: float
    neg_iou_thr: float
    min_pos_iou: float
    match_low_quality: bool
    ignore_iof_thr: int
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Sampler(NamedTuple):
    type: str
    num: int
    pos_fraction: float
    neg_pos_ub: int
    add_gt_as_proposals: bool
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Rpn(NamedTuple):
    assigner: Assigner
    sampler: Sampler
    allowed_border: int
    pos_weight: int
    debug: bool
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Nms(NamedTuple):
    type: str
    iou_threshold: float
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Rpn_proposal(NamedTuple):
    nms_pre: int
    max_per_img: int
    nms: Nms
    min_bbox_size: int
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Rcnn(NamedTuple):
    assigner: Assigner
    sampler: Sampler
    pos_weight: int
    debug: bool
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Train_cfg(NamedTuple):
    rpn: Rpn
    rpn_proposal: Rpn_proposal
    rcnn: Rcnn
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Test_cfg(NamedTuple):
    rpn: Rpn
    rcnn: Rcnn
    constraints: typing.Set[constraint_expr.SymExpr] = set()


class Model(NamedTuple):
    type: str
    backbone: Backbone
    neck: typing.Union[Neck, NoneType]
    rpn_head: Rpn_head
    roi_head: Roi_head
    train_cfg: Train_cfg
    test_cfg: Test_cfg
    constraints: typing.Set[constraint_expr.SymExpr] = set()

    def construct_cons(self):
        constraints = set(
            constraint_expr.SymExpr(bool, "==", (self.roi_head.bbox_roi_extractor.out_channels, self.neck.out_channels))
        )
        return constraints

