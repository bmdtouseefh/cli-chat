from sqlalchemy import create_engine, ForeignKey 
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker, DeclarativeBase, Session


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__="ai_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]

class Chats(Base):
    __tablename__="chats"

    chat_id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("ai_users.id"))
    prompt: Mapped[str]
    response_text: Mapped[str]


DB_URL = "postgresql://postgres:sec1122@localhost:5432/ai"

engine = create_engine(DB_URL, echo=True)

session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

