from typing import Any
from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Category(Base):
    __tablename__ = "categories"

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    name : Mapped[str] = mapped_column(
        unique=True
    )

    description : Mapped[str : None] = mapped_column(
        String(50)
    )

    def __init__(self, **kw: Any):
        super().__init__(**kw)

    def __repr__(self) -> str:
        string = f"ID: {self.id} "
        string += f"NAME : {self.name}\n"
        string += f"DESCRIPtION : \n{self.description}"
        return string