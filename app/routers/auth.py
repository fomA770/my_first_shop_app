#auth.py
from fastapi import APIRouter, HTTPException, status, Depends, Response
from app.schemas.schemas import UserCreate, UserRead
from app.crud.crud_users import user_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, create_user_token, verify_password
from app.core.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.models.models import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter(
    tags=["Authentification"]
)

@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserRead:
    try:
        logger.info(f"Registration attempt for email: {user.email}")
        hashed_password = hash_password(user.password)
        res = await user_crud.create_user(db=db, user_data=user, hashed_password=hashed_password)
        logger.info(f"User registered: {user.email}")
        return UserRead.model_validate(res, from_attributes=True)
    except ValueError as e:
        logger.warning(f"Registration failed for {user.email}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}", exc_info=True)
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
    logger.info(f"Login attempt for email {email}")
    try:
        user = await user_crud.get_by_email(db=db, email=email)
        if not user:
            logger.warning(f"Login failed for email {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong email"
            )
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Wrong password for email {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong email or password"
            )
        token = create_user_token({"sub": email, "id": user.id}) # TODO security.py: get id from token?
        logger.info(f"Token created for email {email}")
        response.set_cookie(
            key="access_token",
            value=token,
            secure=False, #FIXME only for production
            httponly=True,
            samesite="lax",
            max_age=1800
            
        )
        return UserRead.model_validate(user)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
    except Exception as e:
        logger.error(f"{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

