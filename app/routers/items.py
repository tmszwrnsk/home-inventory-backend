"""Application implementation - Items router."""
import logging
from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db

router = APIRouter()
log: logging.Logger = logging.getLogger(__name__)


@router.post(
    "/items",
    tags=["items"],
    response_model=schemas.ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    payload: schemas.ItemCreate, db: Session = Depends(get_db)
) -> schemas.ItemResponse:
    if payload.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0.",
        )

    db_item = models.Item(**payload.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return schemas.ItemResponse(status="created", item=db_item)


@router.get(
    "/items",
    tags=["items"],
    response_model=schemas.ItemsListResponse,
    status_code=status.HTTP_200_OK,
)
def get_items(db: Session = Depends(get_db)) -> schemas.ItemsListResponse:
    items: Sequence[schemas.Item] = db.query(models.Item).all()

    return schemas.ItemsListResponse(status="success", items=items)


@router.get(
    "/items/{item_id}",
    tags=["items"],
    response_model=schemas.ItemResponse,
    status_code=status.HTTP_200_OK,
)
def get_item(item_id: int, db: Session = Depends(get_db)) -> schemas.ItemResponse:
    item: schemas.Item | None = (
        db.query(models.Item).filter(models.Item.id == item_id).one_or_none()
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No item with id: {item_id} found.",
        )

    return schemas.ItemResponse(status="success", item=item)


@router.patch(
    "/items/{item_id}",
    tags=["items"],
    response_model=schemas.ItemResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_item(
    item_id: int, payload: schemas.ItemBase, db: Session = Depends(get_db)
) -> schemas.ItemResponse:
    item: schemas.Item | None = (
        db.query(models.Item).filter(models.Item.id == item_id).one_or_none()
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No item with id: {item_id} found.",
        )

    if payload.quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must not be less than 0.",
        )

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return schemas.ItemResponse(status="accepted", item=item)


@router.delete("/items/{item_id}", tags=["items"], status_code=status.HTTP_200_OK)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    item_query = db.query(models.Item).filter(models.Item.id == item_id)
    item: schemas.Item | None = item_query.one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No item with id: {item_id} found.",
        )

    item_query.delete(synchronize_session=False)
    db.commit()

    return {"status": "deleted", "message": "Item deleted successfully."}
