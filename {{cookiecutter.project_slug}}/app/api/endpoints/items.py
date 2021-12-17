from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud import item
from app.exceptions import ModelNotFoundException
from app.schemas import Item, ItemCreate, ItemUpdate, Message

router = APIRouter()


@router.get("/", response_model=List[Item])
async def read_items(
    db: AsyncSession = Depends(get_db),
    offset: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> List[Item]:
    """
    Retrieve all items
    """

    found_items = await item.list(db, offset=offset, limit=limit)
    return parse_obj_as(List[Item], found_items)


@router.get("/{id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(*, db: AsyncSession = Depends(get_db), id: int) -> Item:
    """
    Get item by ID
    """

    try:
        found_item = await item.get(db, id)
        return parse_obj_as(Item, found_item)
    except ModelNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        ) from error


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Item,
    responses={409: {"model": Message}},
)
async def create_item(
    *, db: AsyncSession = Depends(get_db), item_in: ItemCreate
) -> Item:
    """
    Create a item
    """

    try:
        created_item = await item.create(db, item_in)
        return parse_obj_as(Item, created_item)
    except IntegrityError as error:
        if "duplicate key" in str(error.__cause__):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Item already exist"
            )
        raise error


@router.put(
    "/{id}",
    response_model=Item,
    responses={404: {"model": Message}, 400: {"model": Message}},
)
async def update_item(
    *, db: AsyncSession = Depends(get_db), id: int, item_in: ItemUpdate
) -> Item:
    """
    Update an item
    """

    try:
        updated_item = await item.update(db, item_in, id)
        return parse_obj_as(Item, updated_item)
    except ModelNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        ) from error


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(*, db: AsyncSession = Depends(get_db), id: int) -> None:
    """
    Delete an item
    """

    try:
        await item.delete(db, id)
    except ModelNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        ) from error
