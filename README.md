### Alembic (create)

```bash
alembic revision --autogenerate
```

### Alembic(execute)

```bash
alembic upgrade head
```

### Uvicorn

```bash
python app.py
```

### Hypercorn

```bash
hypercorn app:app --config hypercorn.toml
```

### Docker

```bash
docker-compose up
```

### Redis

```bash
docker run -d --name redis \
  -p 6379:6379 \
  redis:8.0.2
```

### RabbitMQ

```bash
docker run -d --hostname my-rabbit --name rabbitmq-dev -p 5672:5672 -p 15672:15672 rabbitmq:4.1.0-management
```

Celery

```
celery --app celery_app.app.celery_app worker --pool threads --loglevel INFO
```