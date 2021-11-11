from typing import List, Optional

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException, Response, status

from app.crud import item
from app.db import database
from app.exceptions import ModelNotFoundException
from app.schemas import Item, ItemCreate, ItemUpdate, Message
from app.utils import format_response_headers

router = APIRouter()


@router.get("/", response_model=List[Item])
async def read_items(
    response: Response, offset: Optional[int] = 0, limit: Optional[int] = 100
) -> List[Item]:
    """
    Retrieve all items
    """

    items_count = await item.count(database)
    format_response_headers(response, items_count)

    return await item.list(database, offset=offset, limit=limit)


@router.get("/{id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(*, id: int) -> Item:
    """
    Get item by ID
    """

    try:
        return await item.get(database, id)
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
async def create_item(*, item_in: ItemCreate) -> Item:
    """
    Create a item
    """

    try:
        return await item.create(database, item_in)
    except UniqueViolationError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Item already exist"
        ) from error


@router.put(
    "/{id}",
    response_model=Item,
    responses={404: {"model": Message}, 400: {"model": Message}},
)
async def update_item(*, id: int, item_in: ItemUpdate) -> Item:
    """
    Update an item
    """

    try:
        return await item.update(database, item_in, id)
    except ModelNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        ) from error


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(*, id: int) -> None:
    """
    Delete an item
    """

    try:
        await item.delete(database, id)
    except ModelNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        ) from error
