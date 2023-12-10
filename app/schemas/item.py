"""Application implementation - item schema."""
from typing import Sequence

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str
    category: str
    quantity: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ItemResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={"description": "Item response model."})

    status: str
    item: Item


class ItemsListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"description": "Items response model."}
    )

    status: str
    items: Sequence[Item]
