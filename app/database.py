"""
Database wrapper to hold reference to engine and any utility methods
"""

from sqlmodel import SQLModel, create_engine

from .settings import Settings


class Database:
    def __init__(self, settings: Settings) -> None:
        self.engine = create_engine(
            url=settings.sqlachemy_url,
            connect_args=settings.sqlachemy_connection_args,
        )

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)
