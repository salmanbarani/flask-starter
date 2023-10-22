import logging
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey,
    DateTime,
    event
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
    Column("created_at", Date, nullable=False), # TODO: change it to DateTime
    Column("updated_at", Date, nullable=False)  # TODO: change it to DateTime
)

user_logs = Table(
    "userlogs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", ForeignKey("users.id"), unique=True, nullable=False),
    Column("log_type", String(50), nullable=False),
    Column("description", String(255), nullable=True),
    Column("log_time", DateTime)
)

account = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user", ForeignKey("users.id"), unique=True, nullable=False),
    Column("version_number", Integer, nullable=False, server_default="0"),
    Column("logs", ForeignKey("userlogs.id"))
)

def start_mappers():
    logger.info("Starting mappers")
    mapper(user_models.User, user)
    mapper(user_models.Account, account)
    mapper(user_models.UserLog, user_logs)

@event.listens_for(user_models.Account, "load")
def receive_load(account, _):
    account.events = []