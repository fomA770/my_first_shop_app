#crud_users.py
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.models import User, Role
from app.schemas.schemas import UserCreate, UserRead

class CRUDUsers(CRUDBase[User]):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create_user(self,
                           db: AsyncSession,
                           user_data: UserCreate,
                           hashed_password: str,
                           role_name: str = "customer") -> UserRead:
        """
        CRUD operations for USERS table
        """
        existing = await self.get_by_email(db=db, email=user_data.email)
        if existing:
            raise ValueError("User already exists")
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=True,
        )
        result = await db.execute(
            select(Role).where(Role.name == role_name) 
        )
        role = result.scalar_one_or_none()
        if not role:
            role = Role(name=role_name, description=f"Automatically created {role_name} role")
            db.add(role)
            await db.flush()
        user.roles.append(role)
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return UserRead(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            roles=[r.name for r in user.roles]
        )
        

user_crud = CRUDUsers()