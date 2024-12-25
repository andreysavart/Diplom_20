from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

from app.backend.db_depends import get_db
from app.models import BoltJoint, Bolt, Nut, Washer
from app.schemas import CreateBoltJoint, UpdateBoltJoint


router = APIRouter(prefix="/boltjoint", tags=["boltjoint"])


@router.get("/all_bolt_joints")
async def all_bolt_joints(db: Annotated[Session, Depends(get_db)]):
    bolt_joints = db.scalars(select(BoltJoint)).all()
    return bolt_joints


@router.get("/{bolt_joint_id}")
async def bolt_joint_by_id(db: Annotated[Session, Depends(get_db)], bolt_joint_id: int):
    bolt_joint = db.scalar(select(BoltJoint).where(BoltJoint.id == bolt_joint_id))
    if bolt_joint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bolt joint was not found"
        )
    return bolt_joint


@router.post("/create")
async def create_bolt_joint(db: Annotated[Session, Depends(get_db)], crt_bolt_joint: CreateBoltJoint):
    bolt = db.scalar(select(Bolt).where(Bolt.id == crt_bolt_joint.bolt_id))
    bolt_washer = db.scalar(select(Washer).where(Washer.id == crt_bolt_joint.bolt_washer_id))
    nut_washer = db.scalar(select(Washer).where(Washer.id == crt_bolt_joint.nut_washer_id))
    nut = db.scalar(select(Nut).where(Nut.id == crt_bolt_joint.nut_id))
    locknut = db.scalar(select(Nut).where(Nut.id == crt_bolt_joint.locknut_id))
    weight = bolt.weight + bolt_washer.weight + nut_washer.weight + nut.weight + locknut.weight
    cost = bolt.cost + bolt_washer.cost + nut_washer.cost + nut.cost + locknut.cost
    db.execute(
        insert(BoltJoint).values(
            bolt_id=crt_bolt_joint.bolt_id,
            bolt_washer_id=crt_bolt_joint.bolt_washer_id,
            material=crt_bolt_joint.material,
            nut_washer_id=crt_bolt_joint.nut_washer_id,
            nut_id=crt_bolt_joint.nut_id,
            locknut_id=crt_bolt_joint.locknut_id,
            weight=weight,
            cost=cost,
        )
    )
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/{bolt_joint_id}/update")
async def update_bolt_joint(db: Annotated[Session, Depends(get_db)], bolt_joint_id: int, upd_bolt_joint: UpdateBoltJoint):
    bolt = db.scalar(select(Bolt).where(Bolt.id == upd_bolt_joint.bolt_id))
    bolt_washer = db.scalar(select(Washer).where(Washer.id == upd_bolt_joint.bolt_washer_id))
    nut_washer = db.scalar(select(Washer).where(Washer.id == upd_bolt_joint.nut_washer_id))
    nut = db.scalar(select(Nut).where(Nut.id == upd_bolt_joint.nut_id))
    locknut = db.scalar(select(Nut).where(Nut.id == upd_bolt_joint.locknut_id))
    weight = bolt.weight + bolt_washer.weight + nut_washer.weight + nut.weight + locknut.weight
    cost = bolt.cost + bolt_washer.cost + nut_washer.cost + nut.cost + locknut.cost
    db.execute(
        update(BoltJoint).where(BoltJoint.id == bolt_joint_id).values(
            bolt_id=upd_bolt_joint.bolt_id,
            bolt_washer_id=upd_bolt_joint.bolt_washer_id,
            material=upd_bolt_joint.material,
            nut_washer_id=upd_bolt_joint.nut_washer_id,
            nut_id=upd_bolt_joint.nut_id,
            locknut_id=upd_bolt_joint.locknut_id,
            weight=weight,
            cost=cost,
        )
    )
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Bolt joint has been updated successfully!'}


@router.delete("/delete")
async def delete_bolt_joint(db: Annotated[Session, Depends(get_db)], bolt_joint_id: int):
    db.execute(delete(BoltJoint).where(BoltJoint.id == bolt_joint_id))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Bolt joint has been deleted successfully!'
    }
