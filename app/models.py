"""
Models for use with SQL Alchemy (specifically SQLModel wrapper.)
Meant for direct interaction with the database (NOT the view layer).
"""

from sqlmodel import Field, SQLModel  # type: ignore


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str | None = Field(default=None, index=True)
    content: str = Field(index=False)
