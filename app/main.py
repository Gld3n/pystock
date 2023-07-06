from .routers.products import router as products_router
from .routers.settings import router as settings_router

from fastapi import FastAPI

app = FastAPI(
    title="Inventory Management System",
    description="### Manage your inventory securely and efficiently.",
    version="0.1.0",
)
app.include_router(products_router)
app.include_router(settings_router)


@app.get("/")
def root():
    return {"message": "Main menu"}
