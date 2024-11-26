from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Table, Boolean, String, Column, Integer, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.orm import mapped_column, Mapped

from src.database import Base

metadata = MetaData()

role = Table(
    'role',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

# Императивный подход - класс не создаем (переменная).
user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("hashed_password", String(length=1024), nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


# Декларативный подход (описывается User)
# Этот подход использует библиотека fastapi_users, поэтому тут применили.
class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column("id", Integer, primary_key=True)
    email = Column("email", String, nullable=False)
    username = Column("username", String, nullable=False)
    password = Column("password", String, nullable=False)
    registered_at = Column("registered_at", TIMESTAMP, default=datetime.utcnow)
    role_id = Column("role_id", Integer, ForeignKey(role.c.id))
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
