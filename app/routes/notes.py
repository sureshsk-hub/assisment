from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from ..dependencies import SessionDep
from ..models import Note
from ..views import NoteIn, NoteOut

router = APIRouter()


def to_view(note: Note):
    return NoteOut(
        id=note.id or -1,
        title=note.title,
        content=note.content,
    )


def to_model(note: NoteIn):
    return Note(
        title=note.title,
        content=note.content,
    )


@router.post("/notes/")
def create_note(view: NoteIn, session: SessionDep) -> NoteOut:
    model = to_model(view)
    session.add(model)
    session.commit()
    session.refresh(model)
    return to_view(model)


@router.get("/notes/")
def read_notes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[NoteOut]:
    notes = session.exec(select(Note).offset(offset).limit(limit)).all()
    return [to_view(model) for model in notes]


@router.get("/notes/{note_id}")
def read_note(note_id: int, session: SessionDep) -> NoteOut:
    model = session.get(Note, note_id)
    if not model:
        raise HTTPException(status_code=404, detail="Note not found")
    return to_view(model)


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, session: SessionDep):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"ok": True}
