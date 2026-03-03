from fastapi import APIRouter, HTTPException
from sqlalchemy import exc
from sqlmodel import literal_column, select

from ..dependencies import SessionDep

router = APIRouter()


@router.get(
    "/liveness",
    description="INTERNAL USE ONLY - Check if the service is alive.  If this fails, the service should be restarted.",
)
async def liveness():
    return {"status": "alive"}


@router.get(
    "/readiness",
    description="INTERNAL USE ONLY - Check if the service is ready for use. If this fails, traffic should not be routed here.",
)
async def readiness(session: SessionDep):
    # Check that the database is ready to respond
    try:
        session.exec(select(literal_column("1"))).one()  # type: ignore
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database error")

    # Otherwise...
    return {"status": "ready"}
