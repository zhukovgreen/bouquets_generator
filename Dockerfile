FROM python:3.8-alpine as base

FROM base as poetry
RUN apk add --no-cache curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN ln -s $HOME/.poetry/bin/poetry /usr/local/bin

FROM poetry as install_deps
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry install
ENTRYPOINT ["poetry", "run"]
