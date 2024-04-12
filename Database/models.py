from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, Enum, String

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text(500))
    phone: Mapped[str] = mapped_column(Text(500), nullable=True)
    login: Mapped[str] = mapped_column(Text(500))
    password : Mapped[str] = mapped_column(Text(500))
    
