from typing import List

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException, status

from app.crud import item
from app.db import database
from app.exception import ItemNotFoundException
from app.schemas import Item, ItemCreate, ItemUpdate, Message

router = APIRouter()


@router.get("/", response_model=List[Item])
async def read_items() -> List[Item]:
    """
    Retrieve all items
    """
    return await item.list(database)


@router.get("/{id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(*, id: int) -> Item:
    """
    Get item by ID
    """

    try:
        found_item = await item.get(database, id)
    except ItemNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        ) from error

    return found_item


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
        created_item = await item.create(database, item_in)
    except UniqueViolationError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Item already exist"
        ) from error

    return created_item


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
        found_item = await item.get(database, id)
    except ItemNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        ) from error

    return await item.update(database, found_item, item_in)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(*, id: int) -> None:
    """
    Delete an item
    """

    try:
        await item.delete(database, id)
    except ItemNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        ) from error
