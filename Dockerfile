ARG PYTHON_IMAGE=python:3.12.5
FROM ${PYTHON_IMAGE} AS installer

WORKDIR /app/
COPY poetry.lock pyproject.toml ./

RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install --without dev


FROM ${PYTHON_IMAGE}-slim AS container
ENV PATH=/app/.venv/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/
COPY --from=installer /app/.venv ./.venv
COPY src ./src
COPY alembic.ini ./
COPY alembic alembic
RUN ls -a
