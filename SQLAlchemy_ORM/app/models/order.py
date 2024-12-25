from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql import func

from app.backend.db import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"keep_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    edited_at = Column(DateTime(timezone=True), default=datetime.now())
    bolt_joints = relationship('BoltJoint', secondary='order_boltjoints', back_populates='orders')
    weight = Column(Float)
    cost = Column(Float)

    def __str__(self):
        return f'Заказ номер {self.pk} от {self.created_at}. Заказчик: {self.customer}.'


class OrderBoltJoint(Base):
    __tablename__ = 'order_boltjoints'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    bolt_joint_id = Column(Integer, ForeignKey('bolt_joints.id'), nullable=False)


print(CreateTable(Order.__table__))
print(CreateTable(OrderBoltJoint.__table__))
