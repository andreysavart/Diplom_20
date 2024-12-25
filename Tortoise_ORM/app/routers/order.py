from fastapi import APIRouter, status, HTTPException
from tortoise import Tortoise

from app.backend.db import init_db
from app.models import Order, BoltJoint
from app.schemas import CreateOrder, UpdateOrder


router = APIRouter(prefix="/order", tags=["order"])


@router.get("/all_orders")
async def all_orders():
    await init_db() # подключаемся к базе
    orders = await Order.all()
    await Tortoise.close_connections() # закрываем соединения
    return orders


@router.get("/{order_id}")
async def order_by_id(order_id: int):
    await init_db()
    order = await Order.get(order_id=order_id)
    await Tortoise.close_connections()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order was not found"
        )
    return order


@router.post("/create")
async def create_order(crt_order: CreateOrder):
    await init_db()
    order = Order()
    weight = 0
    cost = 0
    for bolt_joint in crt_order.bolt_joints:
        bolt_joint = await BoltJoint.get(bolt_joint_id=bolt_joint.bolt_joint_id)
        weight += bolt_joint.weight
        cost += bolt_joint.cost
        order.order_items.add(bolt_joint)
    order.weight = weight
    order.cost = cost
    await order.create(
        customer=crt_order.customer,
        weight=weight,
        cost=cost,
    )
    await Tortoise.close_connections()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/{order_id}/update")
async def update_order(order_id: int, upd_order: UpdateOrder):
    await init_db()
    items = upd_order.bolt_joints
    order = await Order.get(order_id=order_id)
    weight = 0
    cost = 0
    for bolt_joint in upd_order.bolt_joints:
        bolt_joint = await BoltJoint.get(bolt_joint_id=bolt_joint.bolt_joint_id)
        weight += bolt_joint.weight
        cost += bolt_joint.cost
        order.order_items.add(bolt_joint) # обновляем поле order_items
    upd_order = {
        'customer': upd_order.customer,
        'weight': weight,
        'cost': cost,
    }
    await order.update_from_dict(upd_order) # обновляем остальные поля через словарь
    await order.save() # обязательно сохранить после изменения
    await Tortoise.close_connections()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Order has been updated successfully!'}


@router.delete("/{order_id}/delete")
async def delete_order(order_id: int):
    await init_db()
    order = await Order.get(order_id=order_id)
    await order.delete()
    await Tortoise.close_connections()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Order has been deleted successfully!'
    }
