from fastapi import APIRouter, status, HTTPException
from tortoise import Tortoise

from app.backend.db import init_db
from app.models import Washer
from app.schemas import CreateWasher, UpdateWasher


router = APIRouter(prefix="/washer", tags=["washer"])


@router.get("/all_washers")
async def all_washers():
    await init_db() # подключаемся к базе
    washers = await Washer.all()
    await Tortoise.close_connections() # закрываем соединения
    return washers


@router.get("/{washer_id}")
async def washer_by_id(washer_id: int):
    await init_db()
    washer = await Washer.get(washer_id=washer_id)
    await Tortoise.close_connections()
    if washer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Washer was not found"
        )
    return washer


@router.post("/create")
async def create_washer(crt_washer: CreateWasher):
    await init_db()
    await Washer.create(
        name=crt_washer.name,
        diameter=crt_washer.diameter,
        weight=crt_washer.weight,
        accuracy_class=crt_washer.accuracy_class,
        strength_class=crt_washer.strength_class,
        cost=crt_washer.cost,
    )
    await Tortoise.close_connections()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/{washer_id}/update")
async def update_washer(washer_id: int, upd_washer: UpdateWasher):
    await init_db()
    washer = await Washer.get(washer_id=washer_id)
    upd_washer = {
        'name': upd_washer.name,
        'diameter': upd_washer.diameter,
        'weight': upd_washer.weight,
        'accuracy_class': upd_washer.accuracy_class,
        'strength_class': upd_washer.strength_class,
        'cost': upd_washer.cost,
    }
    await washer.update_from_dict(upd_washer)
    await washer.save() # обязательно сохранить после изменения
    await Tortoise.close_connections()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Washer has been updated successfully!'}


@router.delete("/{washer_id}/delete")
async def delete_washer(washer_id: int):
    await init_db()
    washer = await Washer.get(washer_id=washer_id)
    await washer.delete()
    await Tortoise.close_connections()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Washer has been deleted successfully!'
    }
