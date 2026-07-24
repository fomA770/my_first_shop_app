#dependencied.py
from fastapi import Depends, HTTPException, status
from app.core.security import get_email_from_token
from app.crud.crud_users import user_crud
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User

async def require_admin(email: str = Depends(get_email_from_token), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(email=email, db=db)
    if not user:
        raise ValueError("Invalid token")
    for role in user.roles:
        if role.name == "admin":
            return user
    raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin required")

async def require_admin_or_manager(email: str = Depends(get_email_from_token), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(email=email, db=db)
    if not user:
        raise ValueError("Invalid token")
    for role in user.roles:
        if role.name in ["admin", "manager"]:
            return user
    raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin required")
