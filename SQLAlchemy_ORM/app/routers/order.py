from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

from app.backend.db_depends import get_db
from app.models.bolt_joint import BoltJoint
from app.models.order import Order, OrderBoltJoint
from app.schemas import CreateOrder, UpdateOrder


router = APIRouter(prefix="/order", tags=["order"])


@router.get("/all_orders")
async def all_orders(db: Annotated[Session, Depends(get_db)]):
    orders = db.scalars(select(Order)).all()
    return orders


@router.get("/{order_id}")
async def order_by_id(db: Annotated[Session, Depends(get_db)], order_id: int):
    order = db.scalar(select(Order).where(Order.id == order_id))
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order was not found"
        )
    return order


@router.post("/create")
async def create_order(db: Annotated[Session, Depends(get_db)], crt_order: CreateOrder):
    order = Order()
    db.add(order) # чтобы получить order.id
    order.customer = crt_order.customer
    weight = 0
    cost = 0
    for bolt_joint in crt_order.bolt_joints:
        bolt_joint = db.scalar(select(BoltJoint).where(BoltJoint.id == bolt_joint.id))
        order.bolt_joints.append(bolt_joint)
        # заполняем промежуточную таблицу
        order_boltjoint = OrderBoltJoint()
        order_boltjoint.order_id = order.id
        order_boltjoint.bolt_joint_id = bolt_joint.id
        db.add(order_boltjoint)
        weight += bolt_joint.weight
        cost += bolt_joint.cost
    order.weight = weight
    order.cost = cost
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/{order_id}/update")
async def update_order(db: Annotated[Session, Depends(get_db)], order_id: int, upd_order: UpdateOrder):
    weight = 0
    cost = 0
    bolt_joints = list()
    order = db.scalar(select(Order).where(Order.id == order_id))
    for bolt_joint in upd_order.bolt_joints:
        bolt_joint = db.scalar(select(BoltJoint).where(BoltJoint.id == bolt_joint.id))
        weight += bolt_joint.weight
        cost += bolt_joint.cost
        order.bolt_joints.append(bolt_joint)
    order.weight = weight
    order.cost = cost
    order.customer = upd_order.customer
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Order has been updated successfully!'}


@router.delete("/delete")
async def delete_order(db: Annotated[Session, Depends(get_db)], order_id: int):
    db.execute(delete(Order).where(Order.id == order_id))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Order has been deleted successfully!'
    }
