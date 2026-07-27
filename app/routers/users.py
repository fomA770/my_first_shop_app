from fastapi import APIRouter, HTTPException
from app.schemas.schemas import RoleGive, UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_products import products_crud
from fastapi import Depends
from app.core.database import get_db
from typing import Optional, List
from app.core.dependencies import require_admin, require_admin_or_manager
from app.models.models import User, Role
from app.core.security import get_email_from_token
from app.core.dependencies import require_admin
from app.crud.crud_users import user_crud

router = APIRouter(
    tags=["/users"]
)

@router.post("/give_role")
async def handle_give_role(role_data: RoleGive, 
                           db: AsyncSession = Depends(get_db), 
                           user: User = Depends(require_admin)) -> UserRead:
    user_to_add_role = await user_crud.get(db=db, obj_id=role_data.user_id)
    if not user_to_add_role:
        raise ValueError("No user with that id")
    user_to_add_role.roles.append(Role(name=role_data.name))
    await db.commit()
    await db.refresh(user_to_add_role)
    return UserRead.model_validate(user_to_add_role)