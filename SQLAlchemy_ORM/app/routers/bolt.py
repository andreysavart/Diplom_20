from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

from app.backend.db_depends import get_db
from app.models.bolt import Bolt
from app.schemas import CreateBolt, UpdateBolt


router = APIRouter(prefix="/bolt", tags=["bolt"])


@router.get("/all_bolts")
async def all_bolts(db: Annotated[Session, Depends(get_db)]):
    bolts = db.scalars(select(Bolt)).all()
    return bolts


@router.get("/{bolt_id}")
async def bolt_by_id(db: Annotated[Session, Depends(get_db)], bolt_id: int):
    bolt = db.scalar(select(Bolt).where(Bolt.id == bolt_id))
    if bolt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bolt was not found"
        )
    return bolt


@router.post("/create")
async def create_bolt(db: Annotated[Session, Depends(get_db)], crt_bolt: CreateBolt):
    db.execute(
        insert(Bolt).values(
            name=crt_bolt.name,
            diameter=crt_bolt.diameter,
            length=crt_bolt.length,
            weight=crt_bolt.weight,
            size=crt_bolt.size,
            accuracy_class=crt_bolt.accuracy_class,
            strength_class=crt_bolt.strength_class,
            cost=crt_bolt.cost,
        )
    )
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/{bolt_id}/update")
async def update_bolt(db: Annotated[Session, Depends(get_db)], bolt_id: int, upd_bolt: UpdateBolt):
    db.execute(
        update(Bolt).where(Bolt.id == bolt_id).values(
            name=upd_bolt.name,
            diameter=upd_bolt.diameter,
            length=upd_bolt.length,
            weight=upd_bolt.weight,
            size=upd_bolt.size,
            accuracy_class=upd_bolt.accuracy_class,
            strength_class=upd_bolt.strength_class,
            cost=upd_bolt.cost,
        )
    )
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Bolt has been updated successfully!'}


@router.delete("/delete")
async def delete_bolt(db: Annotated[Session, Depends(get_db)], bolt_id: int):
    db.execute(delete(Bolt).where(Bolt.id == bolt_id))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Bolt has been deleted successfully!'
    }
