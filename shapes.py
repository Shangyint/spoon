from abc import ABC
from dataclasses import dataclass


@dataclass
class StructType(ABC):
    pass

@dataclass
class Record(StructType):
    pass