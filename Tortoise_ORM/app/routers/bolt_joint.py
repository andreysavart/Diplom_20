from fastapi import APIRouter, status, HTTPException
from tortoise import Tortoise

from app.backend.db import init_db
from app.models import BoltJoint, Bolt, Nut, Washer
from app.schemas import CreateBoltJoint, UpdateBoltJoint


router = APIRouter(prefix="/boltjoint", tags=["boltjoint"])


@router.get("/all_bolt_joints")
async def all_bolt_joints():
    await init_db() # подключаемся к базе
    bolt_joints = await BoltJoint.all()
    await Tortoise.close_connections() # закрываем соединения
    return bolt_joints


@router.get("/{bolt_joint_id}")
async def bolt_joint_by_id(bolt_joint_id: int):
    await init_db()
    bolt_joint = await BoltJoint.get(bolt_joint_id=bolt_joint_id)
    await Tortoise.close_connections()
    if bolt_joint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Boltjoint was not found"
        )
    return bolt_joint


@router.post("/create")
async def create_bolt_joint(crt_bolt_joint: CreateBoltJoint):
    await init_db()
    bolt = await Bolt.get(bolt_id=crt_bolt_joint.bolt_id)
    bolt_washer = await Washer.get(washer_id=crt_bolt_joint.bolt_washer_id)
    nut_washer = await Washer.get(washer_id=crt_bolt_joint.nut_washer_id)
    nut = await Nut.get(nut_id=crt_bolt_joint.nut_id)
    locknut = await Nut.get(nut_id=crt_bolt_joint.locknut_id)
    weight = bolt.weight + bolt_washer.weight + nut_washer.weight + nut.weight + locknut.weight
    cost = bolt.cost + bolt_washer.cost + nut_washer.cost + nut.cost + locknut.cost
    await BoltJoint.create(
        material=crt_bolt_joint.material,
        bolt=bolt, # сохраняем непосредственно объект
        bolt_washer=bolt_washer,
        nut_washer=nut_washer,
        nut=nut,
        locknut=locknut,
        weight=weight,
        cost=cost,
    )
    await Tortoise.close_connections()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/{bolt_joint_id}/update")
async def update_bolt_joint(bolt_joint_id: int, upd_bolt_joint: UpdateBoltJoint):
    await init_db()
    bolt_joint = await BoltJoint.get(bolt_joint_id=bolt_joint_id)
    bolt = await Bolt.get(bolt_id=upd_bolt_joint.bolt_id)
    bolt_washer = await Washer.get(washer_id=upd_bolt_joint.bolt_washer_id)
    nut_washer = await Washer.get(washer_id=upd_bolt_joint.nut_washer_id)
    nut = await Nut.get(nut_id=upd_bolt_joint.nut_id)
    locknut = await Nut.get(nut_id=upd_bolt_joint.locknut_id)
    weight = bolt.weight + bolt_washer.weight + nut_washer.weight + nut.weight + locknut.weight
    cost = bolt.cost + bolt_washer.cost + nut_washer.cost + nut.cost + locknut.cost
    upd_bolt_joint = {
        'material': upd_bolt_joint.material,
        'bolt': bolt,
        'bolt_washer': bolt_washer,
        'nut_washer': nut_washer,
        'nut': nut,
        'locknut': locknut,
        'weight': weight,
        'cost': cost,
    }
    await bolt_joint.update_from_dict(upd_bolt_joint)
    await bolt_joint.save() # обязательно сохранить после изменения
    await Tortoise.close_connections()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Boltjoint has been updated successfully!'}


@router.delete("/{bolt_joint_id}/delete")
async def delete_bolt_joint(bolt_joint_id: int):
    await init_db()
    bolt_joint = await BoltJoint.get(bolt_joint_id=bolt_joint_id)
    await bolt_joint.delete()
    await Tortoise.close_connections()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Boltjoint has been deleted successfully!'
    }
