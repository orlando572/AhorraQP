from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import products, cart, stores

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

origins = [
    "http://localhost:5173",    # Vite local
    "http://127.0.0.1:5173",    # Vite local IP
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(cart.router, prefix="/api/cart", tags=["cart"])
app.include_router(stores.router, prefix="/api/stores", tags=["stores"])

# Importar y registrar categorías
from app.api.categories import router as categories_router
app.include_router(categories_router, prefix="/api/categories", tags=["categories"])

@app.get("/")
def root():
    return {"message": "AhorraQP API funcionando"}

@app.get("/health")
def health():
    return {"status": "ok"}