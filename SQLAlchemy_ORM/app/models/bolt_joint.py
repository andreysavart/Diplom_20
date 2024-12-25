from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable

from app.backend.db import Base


class BoltJoint(Base):
    __tablename__ = "bolt_joints"
    __table_args__ = {"keep_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    bolt_id = Column(Integer, ForeignKey("bolts.id"), nullable=False, index=True)
    bolt_washer_id = Column(Integer, ForeignKey("washers.id"), nullable=False, index=True)
    material = Column(String)
    nut_washer_id = Column(Integer, ForeignKey("washers.id"), nullable=False, index=True)
    nut_id = Column(Integer, ForeignKey("nuts.id"), nullable=False, index=True)
    locknut_id = Column(Integer, ForeignKey("nuts.id"), nullable=False, index=True)
    weight = Column(Float)
    cost = Column(Float)

    bolts = relationship(
        "Bolt",
        foreign_keys=[bolt_id],
    )
    bolt_washers = relationship(
        "Washer",
        foreign_keys=[bolt_washer_id],
    )
    nut_washers = relationship(
        "Washer",
        foreign_keys=[nut_washer_id],
    )
    nuts = relationship(
        "Nut",
        foreign_keys=[nut_id],
    )
    locknuts = relationship(
        "Nut",
        foreign_keys=[locknut_id],
    )
    orders = relationship(
        "Order",
        secondary='order_boltjoints',
        back_populates="bolt_joints",
    )

    def __str__(self):
        return f'{self.bolt} {self.nut}'


print(CreateTable(BoltJoint.__table__))
