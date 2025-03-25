# main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes import auth, post
from app.core.database import create_db_and_tables

app = FastAPI(title="FastAPI MVC App")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="API for Auth and Posts",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(post.router, prefix="/post", tags=["Post"])

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()