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
    
class dialogs(Base):
    __tablename__ = 'dialogs'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block1_main_quest: Mapped[str] = mapped_column(Text(1000))
    ans1: Mapped[str] = mapped_column(Text(1000))
    block1_quest2: Mapped[str] = mapped_column(Text(1000))
    ans2: Mapped[str] = mapped_column(Text(1000))
    block1_question3: Mapped[str] = mapped_column(Text(1000))
    ans3: Mapped[str] = mapped_column(Text(1000))
    block2_main_quest: Mapped[str] = mapped_column(Text(1000))
    ans4: Mapped[str] = mapped_column(Text(1000))
    block2_quest2: Mapped[str] = mapped_column(Text(1000))
    ans5: Mapped[str] = mapped_column(Text(1000))
    block2_quest3: Mapped[str] = mapped_column(Text(1000))
    ans6: Mapped[str] = mapped_column(Text(1000))
    block3_main_q: Mapped[str] = mapped_column(Text(1000))
    ans7: Mapped[str] = mapped_column(Text(1000))
    block3_quest2: Mapped[str] = mapped_column(Text(1000))
    ans8: Mapped[str] = mapped_column(Text(1000))
    block3_quest3: Mapped[str] = mapped_column(Text(1000))
    ans9: Mapped[str] = mapped_column(Text(1000))
    ans10: Mapped[str] = mapped_column(Text(1000))