from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="my first api",
    description="This is my first api",
    version="0.0.1",
    openapi_tags=[{
        "name": "users",
        "description": "Operations related to users"
    }]
)
app.include_router(user)
