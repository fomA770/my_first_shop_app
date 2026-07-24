from fastapi import Depends, HTTPException, status
from app.core.security import get_email_from_token
from app.crud.crud_users import user_crud
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User

async def require_admin(email: str = Depends(get_email_from_token), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(email=email, db=db)
    print(user.roles) #type: ignore
    for role in user.roles: # type: ignore
        if role.name == "admin":
            return True
    raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin required")

async def require_admin_or_manager(email: str = Depends(get_email_from_token), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(email=email, db=db)
    for role in user.roles: #type: ignore sqlalchemy model User(name=..., email=..., full_name=..., roles=[..])
        if role.name in ["admin", "manager"]:
            return True
    raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin required")
