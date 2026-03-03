"""
Views for ingress and egress with fastAPI
Meant for direct interaction with the view layer (NOT the database).
"""

from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    title: str | None = Field(
        default=None,
        examples=["Example Note (title optional)"],
        max_length=256,
    )
    content: str = Field(
        examples=["Note that this API gives us examples!"],
        max_length=2048,
    )


class NoteOut(NoteIn):
    id: int = Field(examples=[1, 13, 42])
