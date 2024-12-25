from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable

from app.backend.db import Base


class Bolt(Base):
    __tablename__ = "bolts"
    __table_args__ = {"keep_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    diameter = Column(Float)
    length = Column(Float)
    size = Column(Float)
    weight = Column(Float)
    accuracy_class = Column(String)
    strength_class = Column(Float)
    cost = Column(Float)

    def __str__(self):
        return f'{self.name} {self.diameter}'


print(CreateTable(Bolt.__table__))
