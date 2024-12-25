from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

from app.backend.db_depends import get_db
from app.models.nut import Nut
from app.schemas import CreateNut, UpdateNut


router = APIRouter(prefix="/nut", tags=["nut"])


@router.get("/all_nuts")
async def all_nuts(db: Annotated[Session, Depends(get_db)]):
    nuts = db.scalars(select(Nut)).all()
    return nuts


@router.get("/{nut_id}")
async def nut_by_id(db: Annotated[Session, Depends(get_db)], nut_id: int):
    nut = db.scalar(select(Nut).where(Nut.id == nut_id))
    if nut is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nut was not found"
        )
    return nut


@router.post("/create")
async def create_nut(db: Annotated[Session, Depends(get_db)], crt_nut: CreateNut):
    db.execute(
        insert(Nut).values(
            name=crt_nut.name,
            diameter=crt_nut.diameter,
            weight=crt_nut.weight,
            size=crt_nut.size,
            accuracy_class=crt_nut.accuracy_class,
            strength_class=crt_nut.strength_class,
            cost=crt_nut.cost,
        )
    )
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/{nut_id}/update")
async def update_nut(db: Annotated[Session, Depends(get_db)], nut_id: int, upd_nut: UpdateNut):
    db.execute(
        update(Nut).where(Nut.id == nut_id).values(
            name=upd_nut.name,
            diameter=upd_nut.diameter,
            weight=upd_nut.weight,
            size=upd_nut.size,
            accuracy_class=upd_nut.accuracy_class,
            strength_class=upd_nut.strength_class,
            cost=upd_nut.cost,
        )
    )
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Nut has been updated successfully!'}


@router.delete("/delete")
async def delete_nut(db: Annotated[Session, Depends(get_db)], nut_id: int):
    db.execute(delete(Nut).where(Nut.id == nut_id))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Nut has been deleted successfully!'
    }
