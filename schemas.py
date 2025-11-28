from typing import Optional, Any

from pydantic import BaseModel, EmailStr
from datetime import datetime

from sqlalchemy_to_pydantic import sqlalchemy_to_pydantic

from models import PostModel as _postmodel


class User(BaseModel):
    email: EmailStr


class UserCreate(User):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int | None = None
    email: EmailStr
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class Post(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: bool = True

    class Config:
        from_attributes = True


class PostCreate(Post):
    pass


class PostResponseSchema(BaseModel):
    id: int | None = None
    title: str
    content: str | None = None
    published: bool | None = None
    created_at: datetime | None = None
    owner_id: int
    owner: UserResponseSchema

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    # title: Optional[str] = None
    # content: Optional[str] = None
    # published: bool = True
    # title: Optional[str] = None
    # content: Optional[str] = None
    # published: Any | None
    #الحاجه اللي بنفضي فيها ,الdatatype : الاسم زي المبعوت
    PostModel: PostResponseSchema
    votes: int

    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    vote_dir: int
