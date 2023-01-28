from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import Products, Login, Types
from schemas import ProductsCreate, LoginCreate
from passlib.context import CryptContext
from jose import JWTError, jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SK = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def get_product(db: Session, id: int):
    return db.query(Products).filter(Products.id == id).first()


def get_product_by_name(db: Session, name: str):
    return db.query(Products).filter(Products.name == name).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Products).offset(skip).limit(limit).all()


def get_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Types).offset(skip).limit(limit).all()


def get_type_by_id(db: Session, id: int):
    return db.query(Types).filter(Types.id == id).first()


def create_product(db: Session, product: ProductsCreate):
    db_product = Products(
        name=product.name,
        dir_1=product.dir_1,
        dir_2=product.dir_2,
        discount=product.discount,
        rank=product.rank,
        price_in=product.price_in,
        price_out=product.price_out,
        options=product.options,
        photo_url=product.photo_url,
        type=product.type,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_login_by_name(db: Session, name: str):
    db_user = db.query(Login).filter(Login.user == name).first()
    return db_user


def auth_user(db: Session, username: str, password: str):
    user = get_login_by_name(db, username)
    if not user:
        return False
    if not verify_password(password, user.pwd):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SK, algorithm=ALGORITHM)
    return encoded_jwt


def create_login(db: Session, login: LoginCreate):
    db_login = Products(
        name=login.name,
        pwd=login.pwd,
    )
    db.add(db_login)
    db.commit()
    db.refresh(db_login)
    return db_login
