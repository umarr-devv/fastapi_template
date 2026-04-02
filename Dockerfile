FROM python:3.12

WORKDIR /
RUN pip install poetry
COPY pyproject.toml poetry.lock* /
RUN poetry config virtualenvs.create false && poetry install --no-root --only main
COPY . /

CMD ["hypercorn", "src/main:app", "--config", "hypercorn.toml"]
