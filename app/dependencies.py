"""
Dependencies for FastAPI

Used for doing dependency injection, decoupling the routers and the controllers.
Favor these over using singletons or direct dependency references.
"""

from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlmodel import Session

from . import main
from .database import Database


def _is_valid_secret(token: str):
    # TODO: Actually validate a secret token rather than just checking it has the word 'secret'
    return "secret" not in token


async def get_token_header(x_token: Annotated[str, Header()]):
    """Require that a FastAPI route provide a security token

    Args:
        x_token (Annotated[str, Header): the secret token contents

    Raises:
        HTTPException: If the token not providedm or if invalid
    """
    if not x_token:
        raise HTTPException(status_code=400, detail="X-Token header not provided")
    elif _is_valid_secret(x_token):
        raise HTTPException(status_code=403, detail="X-Token header invalid")


def get_db() -> Database:
    return main.database


DatabaseDep = Annotated[Database, Depends(get_db)]


def get_session(db: DatabaseDep):
    with Session(db.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
