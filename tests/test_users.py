import pytest_asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import UserCreate, UserRead

@pytest.mark.asyncio
async def test_register_user_success(async_client: AsyncClient, db_session: AsyncSession):
    """Testing successful user registration"""
    user_data = {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "full_name": "Testik Testovich"
    }

    response = await async_client.post(
        "/auth/register",
        json=user_data
    )

    if response.status_code != 200:
        print(f"❌ Status: {response.status_code}")
        print(f"📝 Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "password" not in data

    from app.models.models import User
    db_user = await db_session.get(User, data["id"])
    assert db_user is not None
    assert db_user.email == user_data["email"]
    assert db_user.hashed_password != user_data["password"]