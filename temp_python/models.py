from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class User:
    id: int
    email: str
    name: str
    active: bool = True
    metadata: Dict[str, str] = field(default_factory=dict)

    def display_name(self) -> str:
        return self.name or self.email.split("@")[0]


@dataclass
class Product:
    id: int
    name: str
    price_cents: int


@dataclass
class Order:
    id: int
    user_id: int
    product_ids: List[int]
    notes: str = ""
