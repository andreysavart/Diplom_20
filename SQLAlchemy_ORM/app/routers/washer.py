from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

from app.backend.db_depends import get_db
from app.models.washer import Washer
from app.schemas import CreateWasher, UpdateWasher


router = APIRouter(prefix="/washer", tags=["washer"])


@router.get("/all_washers")
async def all_washers(db: Annotated[Session, Depends(get_db)]):
    washers = db.scalars(select(Washer)).all()
    return washers


@router.get("/{washer_id}")
async def washer_by_id(db: Annotated[Session, Depends(get_db)], washer_id: int):
    washer = db.scalar(select(Washer).where(Washer.id == washer_id))
    if washer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Washer was not found"
        )
    return washer


@router.post("/create")
async def create_washer(db: Annotated[Session, Depends(get_db)], crt_washer: CreateWasher):
    db.execute(
        insert(Washer).values(
            name=crt_washer.name,
            diameter=crt_washer.diameter,
            weight=crt_washer.weight,
            accuracy_class=crt_washer.accuracy_class,
            strength_class=crt_washer.strength_class,
            cost=crt_washer.cost,
        )
    )
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/{washer_id}/update")
async def update_washer(db: Annotated[Session, Depends(get_db)], washer_id: int, upd_washer: UpdateWasher):
    db.execute(
        update(Washer).where(Washer.id == washer_id).values(
            name=upd_washer.name,
            diameter=upd_washer.diameter,
            weight=upd_washer.weight,
            accuracy_class=upd_washer.accuracy_class,
            strength_class=upd_washer.strength_class,
            cost=upd_washer.cost,
        )
    )
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Washer has been updated successfully!'}


@router.delete("/delete")
async def delete_washer(db: Annotated[Session, Depends(get_db)], washer_id: int):
    db.execute(delete(Washer).where(Washer.id == washer_id))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Washer has been deleted successfully!'
    }
