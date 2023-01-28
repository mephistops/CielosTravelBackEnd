from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from crud import get_product, get_product_by_name, get_products, create_product, auth_user, create_access_token, get_types, get_type_by_id
from models import Products, Types

from schemas import Products, ProductsCreate, Login, Token, Types
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

description = """
Cielos Travel API helps you do awesome stuff. 🚀
"""

app = FastAPI(
    title="Cielos Travel",
    description=description,
    version="0.0.1",
    terms_of_service="https://gfytzo.deta.dev/",
    contact={
        "name": "Luis Caraballo",
        "url": "https://gfytzo.deta.dev/",
        "email": "lcm7039@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ATE = 30

origins = [
    "http://localhost:5173",
    "https://courageous-tapioca-159e51.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_product", response_model=Products, tags=["Products"])
def create_products(product: ProductsCreate, db: Session = Depends(get_db)):
    db_product = get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="name already registered")
    return create_product(db=db, product=product)


@app.post("/product", response_model=Products, tags=["Products"])
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, id=product_id)
    return product


@app.get("/products", response_model=list[Products], tags=["Products"])
def read_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products


@app.get("/types", response_model=list[Types], tags=["Types"])
def read_all_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    types = get_types(db, skip=skip, limit=limit)
    return types


@app.get("/type/{type_id}", response_model=Types, tags=["Types"])
def read_type_by_id(type_id: int, db: Session = Depends(get_db)):
    types = get_type_by_id(db, id=type_id)
    return types


@app.post("/login", response_model=Token, tags=["Users"])
async def login_for_access_token(form_data: Login, db: Session = Depends(get_db)):
    user = auth_user(db, form_data.user, form_data.pwd)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ATE)
    access_token = create_access_token(
        data={"sub": user.user}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
