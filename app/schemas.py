from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from typing import Literal
from pydantic import ConfigDict



#Building the schema for post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: Post
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_Data(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]


# Amounts are USD cents to avoid floating-point rounding for money.
from pydantic import Field, field_validator

DealStage = Literal["pitch", "negotiation", "brief", "content_review", "delivered", "paid"]

class DealCreate(BaseModel):
    brand: str = Field(min_length=1, max_length=200)
    creator: str = Field(min_length=1, max_length=200)
    deliverables: str = Field(min_length=1, max_length=2000)
    amount_cents: int = Field(ge=0, le=2147483647, strict=True)
    stage: DealStage = "pitch"

    @field_validator("brand", "creator", "deliverables")
    @classmethod
    def nonblank(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Must not be blank")
        return value

class DealUpdate(BaseModel):
    brand: Optional[str] = Field(default=None, min_length=1, max_length=200)
    creator: Optional[str] = Field(default=None, min_length=1, max_length=200)
    deliverables: Optional[str] = Field(default=None, min_length=1, max_length=2000)
    amount_cents: Optional[int] = Field(default=None, ge=0, le=2147483647, strict=True)
    stage: Optional[DealStage] = None

    @field_validator("brand", "creator", "deliverables", "amount_cents", "stage")
    @classmethod
    def validate_update(cls, value):
        if value is None:
            raise ValueError("Field cannot be null")
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Must not be blank")
        return value

class DealOut(DealCreate):
    id: int
    owner_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
