
import fastapi_users.router
from fastapi import FastAPI

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate


app = FastAPI(
    title="Trading App"
)

# fastapi_users = FastAPIUsers[User, int](
#     get_user_manager,
#     [auth_backend],
# )

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

# current_user = fastapi_users.current_user()


# @app.get("/protected-route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.username}"
#
#
# @app.get("/unprotected-route")
# def unprotected_route():
#     return f"Hello, anonym"
#
# async def common_parameters(
#         q: Union[str, None] = None, skip: int = 0, limit: int = 100
# ):
#     return {"q": q, "skip": skip, "limit": limit}
#
#
# @app.get("/items/")
# async def read_items(commons: dict = Depends(common_parameters)):
#     return commons
#
# @app.get("/users/")
# async def read_users(commons: dict = Depends(common_parameters)):
#     return commons
