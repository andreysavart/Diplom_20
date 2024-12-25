from fastapi import APIRouter, status, HTTPException
from tortoise import Tortoise

from app.backend.db import init_db
from app.models import Nut
from app.schemas import CreateNut, UpdateNut


router = APIRouter(prefix="/nut", tags=["nut"])


@router.get("/all_nuts")
async def all_nuts():
    await init_db() # подключаемся к базе
    nuts = await Nut.all()
    await Tortoise.close_connections() # закрываем соединения
    return nuts


@router.get("/{nut_id}")
async def nut_by_id(nut_id: int):
    await init_db()
    nut = await Nut.get(nut_id=nut_id)
    await Tortoise.close_connections()
    if nut is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nut was not found"
        )
    return nut


@router.post("/create")
async def create_nut(crt_nut: CreateNut):
    await init_db()
    await Nut.create(
        name=crt_nut.name,
        diameter=crt_nut.diameter,
        weight=crt_nut.weight,
        size=crt_nut.size,
        accuracy_class=crt_nut.accuracy_class,
        strength_class=crt_nut.strength_class,
        cost=crt_nut.cost,
    )
    await Tortoise.close_connections()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/{nut_id}/update")
async def update_nut(nut_id: int, upd_nut: UpdateNut):
    await init_db()
    nut = await Nut.get(nut_id=nut_id)
    upd_nut = {
        'name': upd_nut.name,
        'diameter': upd_nut.diameter,
        'weight': upd_nut.weight,
        'size': upd_nut.size,
        'accuracy_class': upd_nut.accuracy_class,
        'strength_class': upd_nut.strength_class,
        'cost': upd_nut.cost,
    }
    await nut.update_from_dict(upd_nut)
    await nut.save() # обязательно сохранить после изменения
    await Tortoise.close_connections()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Nut has been updated successfully!'}


@router.delete("/{nut_id}/delete")
async def delete_nut(nut_id: int):
    await init_db()
    nut = await Nut.get(nut_id=nut_id)
    await nut.delete()
    await Tortoise.close_connections()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Nut has been deleted successfully!'
    }
