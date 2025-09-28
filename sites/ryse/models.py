from dataclasses import dataclass
from typing import Optional, List

@dataclass
class VariantStatus:
    flavor: str
    in_stock: bool

@dataclass
class ProductStatus:
    product_name: str
    variants: List[VariantStatus]