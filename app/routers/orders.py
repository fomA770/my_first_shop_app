from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.security import get_email_from_token
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_orders import orders_crud
from app.crud.crud_users import user_crud
from app.schemas.schemas import OrderReturn, OrderProductsList, OrdersReturn, ReturnOrderAndOrderItems, OrderItemReturn, UpdateOrderStatusRequest

router = APIRouter(
    tags=["Orders"]
)

@router.post("/create_order")
async def handle_create_order(email: str = Depends(get_email_from_token), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    result = await orders_crud.create_order(user_id=user.id, db=db)
    if not result:
        return JSONResponse(status_code=200, content={"message": "There is no items in the cart"})
    new_order, order_items = result
    return ReturnOrderAndOrderItems.model_validate({
        "order": new_order,
        "items": [OrderItemReturn.model_validate(i) for i in order_items]
    })
    

@router.get("/user_orders")
async def handle_get_user_orders(email: str = Depends(get_email_from_token), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_order_items = await orders_crud.get_user_orders_items(user_id=user.id, db=db)
    if not user_order_items:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "No orders yet"})
    return_dict = {}
    for item in user_order_items:
        order_id, product_id, quantity, order_status = item.order_id, item.product_id, item.quantity, item.order_status
        return_dict[order_id] = (return_dict.get(order_id, []) + 
                                 [OrderProductsList.model_validate(
                                     {"product_id": product_id, "quantity": quantity}
                                     )]
        )
        print(return_dict)
    return [OrdersReturn.model_validate({"id": key, "status": order_status, "products": values}) for key, values in return_dict.items() ]

@router.put("/update_status")
async def handle_update_order_status(update_order_data: UpdateOrderStatusRequest, 
                                     email: str = Depends(get_email_from_token), 
                                     db: AsyncSession = Depends(get_db)):
    order_status = update_order_data.status
    order_id = update_order_data.order_id
    result = await orders_crud.update_order_status(order_id=order_id, status=order_status, db=db)
    return OrderReturn.model_validate(result)