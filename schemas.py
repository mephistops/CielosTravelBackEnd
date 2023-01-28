from pydantic import BaseModel


class LoginBase(BaseModel):
    user: str


class LoginCreate(LoginBase):
    pass


class Login(LoginBase):
    pwd: str
    pass

    class Config:
        orm_mode = True


class ProductsBase(BaseModel):
    name: str
    dir_1: str
    dir_2: str
    discount: int
    rank: int
    price_in: int
    price_out: int
    options: str
    photo_url: str
    type: int


class ProductsCreate(ProductsBase):
    pass


class Products(ProductsBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class TypesBase(BaseModel):  
    id: int  
    name: str
    show: bool
    link: str
    icon: str
    active: bool
    new: bool


class TypesCreate(TypesBase):
    pass


class Types(TypesBase):
    id: int

    class Config:
        orm_mode = True
