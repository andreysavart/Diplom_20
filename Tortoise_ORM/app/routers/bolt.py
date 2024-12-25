from fastapi import APIRouter, status, HTTPException
from tortoise import Tortoise

from app.backend.db import init_db
from app.models import Bolt
from app.schemas import CreateBolt, UpdateBolt


router = APIRouter(prefix="/bolt", tags=["bolt"])


@router.get("/all_bolts")
async def all_bolts():
    await init_db() # подключаемся к базе
    bolts = await Bolt.all()
    await Tortoise.close_connections() # закрываем соединения
    return bolts


@router.get("/{bolt_id}")
async def bolt_by_id(bolt_id: int):
    await init_db()
    bolt = await Bolt.get(bolt_id=bolt_id)
    await Tortoise.close_connections()
    if bolt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bolt was not found"
        )
    return bolt


@router.post("/create")
async def create_bolt(crt_bolt: CreateBolt):
    await init_db()
    await Bolt.create(
        name=crt_bolt.name,
        diameter=crt_bolt.diameter,
        length=crt_bolt.length,
        weight=crt_bolt.weight,
        size=crt_bolt.size,
        accuracy_class=crt_bolt.accuracy_class,
        strength_class=crt_bolt.strength_class,
        cost=crt_bolt.cost,
    )
    await Tortoise.close_connections()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/{bolt_id}/update")
async def update_bolt(bolt_id: int, upd_bolt: UpdateBolt):
    await init_db()
    bolt = await Bolt.get(bolt_id=bolt_id)
    upd_bolt = {
        'name': upd_bolt.name,
        'diameter': upd_bolt.diameter,
        'length': upd_bolt.length,
        'weight': upd_bolt.weight,
        'size': upd_bolt.size,
        'accuracy_class': upd_bolt.accuracy_class,
        'strength_class': upd_bolt.strength_class,
        'cost': upd_bolt.cost,
    }
    await bolt.update_from_dict(upd_bolt)
    await bolt.save() # обязательно сохранить после изменения
    await Tortoise.close_connections()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Bolt has been updated successfully!'}


@router.delete("/{bolt_id}/delete")
async def delete_bolt(bolt_id: int):
    await init_db()
    bolt = await Bolt.get(bolt_id=bolt_id)
    await bolt.delete()
    await Tortoise.close_connections()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Bolt has been deleted successfully!'
    }
