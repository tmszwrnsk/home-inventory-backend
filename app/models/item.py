from sqlalchemy import Column, Integer, String

from app.database import Base


class Item(Base):
    __tablename__: str = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
