import logging
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Date,
    Boolean,
)

from sqlalchemy.orm import registry

from src.domain import user_models

logger = logging.getLogger(__name__)

metadata = registry().metadata
mapper = registry().map_imperatively

user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(255), nullable=False, unique=True),
    Column("username", String(50), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("first_name", String(255), nullable=True),
    Column("last_name", String(255), nullable=True),
    Column("is_active", Boolean, default=True, nullable=True),
    Column("is_admin", Boolean, default=False, nullable=True),
    Column("created_at", Date, nullable=False),
    Column("updated_at", Date, nullable=False)
)


def start_mappers():
    logger.info("Starting mappers")
    mapper(user_models.User, user)