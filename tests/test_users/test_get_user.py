import pytest
from httpx import AsyncClient

from repositories import RepositoryManager


@pytest.mark.asyncio
async def test_get_users(
        async_client: AsyncClient,
):
    response = await async_client.get('/users')
    assert response.status_code in (200, 201)
