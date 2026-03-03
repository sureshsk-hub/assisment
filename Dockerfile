# # # -----------------------------
# # # 1️⃣ Base Image
# # # -----------------------------
# # FROM python:3.11-slim AS base

# # # Prevent Python from writing pyc files
# # ENV PYTHONDONTWRITEBYTECODE=1
# # # Ensure stdout/stderr are unbuffered
# # ENV PYTHONUNBUFFERED=1

# # WORKDIR /app

# # # Install system dependencies (minimal)
# # RUN apt-get update \
# #     && apt-get install -y --no-install-recommends build-essential curl \
# #     && rm -rf /var/lib/apt/lists/*

# # # -----------------------------
# # # 2️⃣ Install Python Dependencies
# # # -----------------------------
# # FROM base AS builder

# # COPY requirements.txt .

# # RUN pip install --upgrade pip \
# #     && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# # # -----------------------------
# # # 3️⃣ Final Production Image
# # # -----------------------------
# # FROM base

# # # Create non-root user
# # RUN useradd --create-home appuser

# # # Copy only wheels from builder
# # COPY --from=builder /app/wheels /wheels
# # COPY requirements.txt .

# # RUN pip install --no-cache /wheels/*

# # # Copy application code
# # COPY ./app ./app

# # # Change ownership
# # RUN chown -R appuser:appuser /app

# # USER appuser

# # EXPOSE 8000

# # # Health check
# # HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
# #   CMD curl -f http://localhost:8000/health || exit 1


# # CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

# # Use an official Python base image
# FROM python:3.11-slim

# # Set environment variables
# ENV PYTHONUNBUFFERED=1 \
#     APP_HOME=/app

# # Create app directory
# WORKDIR $APP_HOME

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     curl build-essential \
#     && rm -rf /var/lib/apt/lists/*

# # Install uv (Python environment manager)
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# # Copy project files
# COPY . .

# # Install Python dependencies using uv
# RUN uv sync --frozen

# # Expose port
# EXPOSE 8000

# # Default command to run the app with uvicorn
# CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config=log_conf.yaml"]

# ----------- Builder Stage -------------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock* ./

# Install UV (if you're using uv)
RUN pip install --no-cache-dir uv

RUN uv pip install --system .

# ----------- Runtime Stage -------------
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run with production settings
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
RUN uv sync --system
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



