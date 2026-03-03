# Notes API

This is a RESTful CRUD app for creating, reading, listing, and deleting notes.

## Quickstart
```sh
# In dev...
uv run fastapi dev --host "0.0.0.0" --port 80
# In prod...
uv run uvicorn app.main:app --host "0.0.0.0" --port 8000 --log-config=log_conf.yaml
```
See the rest of the readme for details on usage and configuration.

## API Endpoints:

Use the following routes:
- `/` (GET) - Introduction to the API
- `/docs`, `/redoc`, `/openapi.json` (GET) - Documentation for what this API can do 
- `/liveness` (GET) - Whether the API is alive (200) or not
- `/readiness` (GET) - Whether the API is ready to respond (200) or not
- `/notes`, `/notes/{id}` (GET, POST, DELETE) - List, create, read, and delete notes 

## What's included
- **uv** to manage the python version, build environment, and dependencies._(encapsulates nearly [all python tooling](https://docs.astral.sh/uv/getting-started/features/))_
- **[fastapi](https://fastapi.tiangolo.com/)** REST API framework
- **[sqlalchemy](https://docs.sqlalchemy.org/en/20/dialects/index.html)** to read & write to an RDBMS
- **uvicorn** [ASGI server](https://fastapi.tiangolo.com/deployment/manually/#asgi-servers) as a pre-packaged  dependency
- **opentelemetry** reporter dependencies pre-packaged (awaiting a [collector](https://opentelemetry.io/docs/platforms/kubernetes/operator/automatic/#python))
    

# Usage
## Local development usage

Start by [installing UV](https://docs.astral.sh/uv/getting-started/installation/).

Then, navigate to this project and...
```sh
# Set up the dev env:
uv python install # fetch and install the python required by this project (will be managed by UV)
uv venv # create a virtual env to keep the dependencies isolated
source .venv/bin/activate # if on OSX/Linux, otherwise...
./.venv/Scripts/activate # if on windows
uv sync # install dependencies

# Run in dev
uv run fastapi --help # display options
uv run fastapi dev --host "0.0.0.0" --port 8000 # run with auto-refresh on source change - host and port are optional
```

Your app should now be running at http://localhost:8000.

## Deployment usage

When running as a non-development server, you have a variety of ways to run the app.

### Option 1: Run with `fastapi` directly
```sh
uv run fastapi --help # display fastapi help
uv run fastapi run --host "0.0.0.0" --port 8000 # host and port are optional
```

### Option 2: Run with `uvicorn`
```sh
uv run uvicorn --help # display uvicorn help
uv run uvicorn app.main:app --host "0.0.0.0" --port 8000 --log-config=log_conf.yaml # uvicorn exposes logging configuration
```

### Option 3: Run with `uvicorn` wrapped with `opentelemetry-instrument`
```sh
uv run opentelemetry-instrument --help # display otel help
uv run opentelemetry-instrument uvicorn --help # display uvicorn help
uv run opentelemetry-instrument uvicorn app.main:app --host "0.0.0.0" --port 8000 --log-config=log_conf.yaml # watch for logs coming from otel reporter

# You can set up otel parameters with ENV vars too!
# https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/
export OTEL_EXPORTER_OTLP_ENDPOINT='http://localhost:4318'
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
export OTEL_SERVICE_NAME='<NAME_OF_YOUR_APP_OR_SERVICE>'
uv run opentelemetry-instrument uvicorn app.main:app --host "0.0.0.0" --port 8000
```
_Note: You will need to [set up an otel collector](https://opentelemetry.io/docs/platforms/kubernetes/operator/automatic/#python), otherwise there will be nowhere to report._

# Configuration

Uses ENV vars and/or [dotenv](https://www.dotenv.org/) file (loading in that order.)

See `./.env` for the defaulted local usage.

Some examples of other potential configurations:

### Option 1: SQLite
```sh
APP_NAME='Notes API running on SQLite'
SQLACHEMY_URL='sqlite:///local-database.db'
SQLACHEMY_CONNECTION_ARGS='{"check_same_thread": false}'
```

### Option 2: PostgreSQL
```sh
APP_NAME='Notes API running on PGSQL'
SQLACHEMY_URL='postgresql+psycopg2://user:password@hostname/database_name'
# SQLACHEMY_CONNECTION_ARGS='{}' # no need to supply, will default to empty
```

### Option 3: MySQL/MariaDB
```sh
APP_NAME='Notes API running on PGSQL'
SQLACHEMY_URL='mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4'
# SQLACHEMY_CONNECTION_ARGS='{}' # no need to supply, will default to empty
```

### Other Options
The above options use dependencies that are alread pre-packaged _(so they can be used immediately),_ but our underlying SQL ORM supports [many other options](https://docs.sqlalchemy.org/en/20/dialects/index.html).

If you want to use these, make sure you `uv add` the dependency.