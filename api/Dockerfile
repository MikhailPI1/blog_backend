FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_INPUT=1 \
    PIP_PROGRESS_BAR=off

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev python3-dev build-essential

WORKDIR /app

COPY ./requirements.txt ./requirements/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -U pip setuptools wheel && \
    (python -m pip install -r ./requirements/requirements.txt -j 4 --use-feature=fast-deps \
    || python -m pip install -r ./requirements/requirements.txt)

COPY src ./src

WORKDIR /app/src

CMD ["python", "main.py"]