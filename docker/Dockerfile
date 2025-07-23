FROM ubuntu AS master

RUN apt-get -y update
RUN apt-get install -y curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN apt-get -y install ffmpeg

WORKDIR /opt/app-root/
COPY src src/
COPY .python-version .
COPY pyproject.toml .

ENV PATH="/root/.local/bin/:$PATH"
ENV PYTHONPATH=.

RUN uv sync

ENV TZ="Europe/Moscow"

FROM base AS main

CMD uv run src/main.py