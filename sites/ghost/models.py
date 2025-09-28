from dataclasses import dataclass
from typing import List

@dataclass
class GhostVariant:
    flavor: str
    in_stock: bool

@dataclass
class GhostProductStatus:
    name: str
    url: str
    variants: List[GhostVariant]