FROM python:3.12

WORKDIR /code
RUN pip install poetry
COPY pyproject.toml poetry.lock* /code/
RUN poetry config virtualenvs.create false \
&& poetry install --no-root --only main
COPY . /code/

CMD ["hypercorn", "app:app", "--config", "hypercorn.toml"]
