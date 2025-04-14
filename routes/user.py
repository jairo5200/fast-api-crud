from fastapi import APIRouter, Response
from config.db import conn
from models.user import users
from schemas.user import User
from starlette.status import HTTP_204_NO_CONTENT
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()


@user.get('/users', response_model=list[User], tags=["users"])
async def get_users():
    res = conn.execute(users.select())
    users_list = res.mappings().fetchall()
    return [dict(user) for user in users_list]


@user.get('/users/{id}', response_model=User, tags=["users"])
async def get_user(id: str):
    res = conn.execute(users.select().where(users.c.id == id))
    created_user = res.mappings().fetchone()
    return dict(created_user)


@user.post('/users', response_model=User, tags=["users"])
async def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    print(new_user)
    result = conn.execute(users.insert().values(new_user))
    conn.commit()
    res = conn.execute(users.select().where(users.c.id == result.lastrowid))
    created_user = res.mappings().fetchone()
    return dict(created_user)


@user.delete('/users/{id}', status_code=HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(id: str):
    result = conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put('/users/{id}', response_model=User, tags=["users"])
async def update_user(id: int, user: User):
    conn.execute(users.update().values(
        name=user.name,
        email=user.email,
        password=f.encrypt(user.password.encode("utf-8"))
    ).where(users.c.id == id))
    conn.commit()

    res = conn.execute(users.select().where(users.c.id == id))
    updated_user = res.mappings().fetchone()

    return dict(updated_user)
