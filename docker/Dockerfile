FROM ubuntu AS base

RUN apt-get -y update
RUN apt-get install -y curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /opt/app-root/
COPY src src/
COPY .python-version .
COPY pyproject.toml .

ENV PATH="/root/.local/bin/:$PATH"
ENV PYTHONPATH=.

RUN uv sync

ENV TZ="Europe/Moscow"

FROM base AS master

CMD uv run src/main.py