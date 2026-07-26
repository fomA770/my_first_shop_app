from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_email_from_token
from app.crud.crud_cart import cart_crud
from app.crud.crud_users import user_crud
from app.crud.crud_products import products_crud
from app.crud.crud_cart_item import cart_item_crud
from app.schemas.schemas import AddToCart, CartItemReturn, CartReturn

router = APIRouter(
    tags=["Cart"]
)

@router.get("/")
async def handle_get_cart(email: str = Depends(get_email_from_token), db: AsyncSession = Depends(get_db)) -> CartReturn:
    try:
        user = await user_crud.get_by_email(email=email, db=db)
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        result = await cart_crud.get_cart(user_id = user.id, db=db)
        return CartReturn.model_validate(result)
    except Exception as e:
        raise HTTPException(500, detail=f"Внутренняя ошибка сервера, {str(e)}") #TODO errors

@router.post("/add")
async def handle_add_to_cart(data: AddToCart, 
                             email: str = Depends(get_email_from_token), 
                             db: AsyncSession = Depends(get_db)) -> CartItemReturn:
    user = await user_crud.get_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    result = await cart_crud.add_to_cart(user_id=user.id, 
                                         product_id=data.product_id, 
                                         cart_id=data.cart_id, 
                                         quantity=data.quantity, 
                                         db=db)
    return CartItemReturn.model_validate(result)

@router.get("/get_all")
async def handle_get_all_cart_items(email: str = Depends(get_email_from_token), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    cart = await cart_crud.get_cart(user_id=user.id, db=db)
    result = await cart_item_crud.get_all_cart_items(cart_id=cart.id, db=db)
    if not result:
        return JSONResponse(status_code=200, content={"message": "No items in the cart"})
    return [CartItemReturn.model_validate(item) for item in result]

@router.delete("/del/{product_id}")
async def handle_del_by_id(product_id: int, email: str = Depends(get_email_from_token), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    cart_item = await cart_crud.del_by_id(user_id=user.id, product_id=product_id, db=db)
    return CartItemReturn.model_validate(cart_item)

@router.delete("/clear_cart")
async def handle_clear_cart(email: str = Depends(get_email_from_token), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    cart = await cart_crud.get_cart(user_id=user.id, db=db)
    cart_items = await cart_crud.clear_cart(cart_id=cart.id, db=db)
    if not cart_items:
        raise ValueError("Cart is empty")
    return [CartItemReturn.model_validate(item) for item in cart_items]

    
