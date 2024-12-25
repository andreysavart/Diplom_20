from pydantic import BaseModel
from typing import List


class CreateBolt(BaseModel):
    name: str
    diameter: float
    length: float
    size: float
    weight: float
    accuracy_class: str
    strength_class: float
    cost: float


class UpdateBolt(BaseModel):
    name: str
    diameter: float
    length: float
    size: float
    weight: float
    accuracy_class: str
    strength_class: float
    cost: float


class CreateNut(BaseModel):
    name: str
    diameter: float
    size: float
    weight: float
    accuracy_class: str
    strength_class: float
    cost: float


class UpdateNut(BaseModel):
    name: str
    diameter: float
    size: float
    weight: float
    accuracy_class: str
    strength_class: float
    cost: float


class CreateWasher(BaseModel):
    name: str
    diameter: float
    weight: float
    accuracy_class: str
    strength_class: float
    cost: float


class UpdateWasher(BaseModel):
    name: str
    diameter: float
    weight: float
    accuracy_class: str
    strength_class: float
    cost: float


class CreateBoltJoint(BaseModel):
    material: str
    bolt_id: int
    bolt_washer_id: int
    nut_washer_id: int
    nut_id: int
    locknut_id: int


class UpdateBoltJoint(BaseModel):
    material: str
    bolt_id: int
    bolt_washer_id: int
    nut_washer_id: int
    nut_id: int
    locknut_id: int


class BoltJoint(BaseModel):
    id: int
    material: str
    bolt_id: int
    bolt_washer_id: int
    nut_washer_id: int
    nut_id: int
    locknut_id: int


    class Config:
        from_attributes = True


class CreateOrder(BaseModel):
    customer: str
    bolt_joints: List[BoltJoint]


class UpdateOrder(BaseModel):
    customer: str
    bolt_joints: List[BoltJoint]
