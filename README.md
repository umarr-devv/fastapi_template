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
  redis:latest
```