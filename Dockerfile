FROM python:3.13
ENV POETRY_VERSION=2.1.3
RUN pip install poetry==$POETRY_VERSION
WORKDIR /Bot_cli_app_work_dir
COPY pyproject.toml poetry.lock ./
COPY . .
RUN poetry config virtualenvs.create false \
    && poetry install --no-ansi --no-root
ENTRYPOINT [ "python", "main.py" ]