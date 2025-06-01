import pytest
from httpx import AsyncClient, ASGITransport

from app import app


@pytest.fixture
async def async_client() -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app),
        base_url='http://tests/api'
    )
