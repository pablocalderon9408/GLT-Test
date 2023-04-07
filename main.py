import os
import uvicorn


from fastapi import FastAPI
from config.database import engine, Base


# Routers
from products.routers import product_router
from orders.routers import order_router
from users.routers import users_router


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 8000)))

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

app.include_router(users_router)
app.include_router(product_router)
app.include_router(order_router)
Base.metadata.create_all(bind=engine)
