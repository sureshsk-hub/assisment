"""
ENTRYPOINT FOR FASTAPI
> fastapi run -h

Please run this program through use of fastapi or ASGI server directly - see outer README packaged with it for details.
"""

import textwrap
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse

from .database import Database
from .dependencies import get_session, get_token_header
from .routes import health, notes
from .settings import get_settings

# Pull ENV vars and .env file in
settings = get_settings()
# Configure Database, set up db initialization
database = Database(settings)


# Init and teardown
@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
    yield


# Start the app
app = FastAPI(lifespan=lifespan, title=settings.app_name)

# Set up routes and injected depedencies:
app.include_router(
    health.router,
    tags=["internal"],
)
app.include_router(
    notes.router,
    dependencies=[
        Depends(get_token_header),  # Require token header auth
        Depends(get_session),  # Provide database sessions
    ],
    tags=["external"],
)


# Root endpoint for when folks hit the API blindly
@app.get("/", response_class=PlainTextResponse)
async def root():
    return textwrap.dedent(
        f"""\
        Welcome to the Notes API!
        
        Use the following routes:
        {app.docs_url} - Interactable API documentation (execute samples) 
        {app.redoc_url} - API documentation (redoc) 
        {app.openapi_url} - OpenAPI spec
        """
    )
