from fastapi.routing import APIRouter
from src.apps.api.docs.views import router as docs_router
from src.apps.api.auth.views import router as auth_router
from src.apps.api.category.views import router as category_router
from src.apps.api.product.views import router as product_router

api_router = APIRouter(prefix='/api')

api_router.include_router(docs_router)

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(category_router, prefix="/category", tags=["Category"])
api_router.include_router(product_router, prefix="/product", tags=["Product"])

