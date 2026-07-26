#auth.py
from fastapi import APIRouter, HTTPException, status, Depends, Response
from app.schemas.schemas import UserCreate, UserRead
from app.crud.crud_users import user_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, create_user_token, verify_password
from app.core.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.models.models import User

router = APIRouter(
    tags=["Authentification"]
)

@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserRead:
    try:
        hashed_password = hash_password(user.password)
        res = await user_crud.create_user(db=db, user_data=user, hashed_password=hashed_password)
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error {str(e)}"
        )

@router.post("/login")
async def login_user(response: Response,
                     form_data: OAuth2PasswordRequestForm = Depends(), 
                     db: AsyncSession = Depends(get_db)) -> UserRead:
    email = form_data.username
    password = form_data.password
    try:
        user = await user_crud.get_by_email(db=db, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong email"
            )
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong email or password"
            )
        token = create_user_token({"sub": email, "id": user.id}) # TODO security.py: get id from token?
        response.set_cookie(
            key="access_token",
            value=token,
            secure=False, #FIXME only for production
            httponly=True,
            samesite="lax",
            max_age=1800
            
        )
        return UserRead(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            roles=[r.name for r in user.roles]
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error {str(e)}")

