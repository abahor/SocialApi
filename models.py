from sqlalchemy import Column, Integer, String, Boolean, text, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import Relationship, relationship

from database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


# alembic init alembic
# alembic revision --autogenerate -m "First revision"
# alembic upgrade head
# alembic downgrade -1

class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True')
    phone_number = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User"'', back_populates="owner")

    # votes = Relationship()
    # votes = relationship("Votes", back_populates="owner")

    # gg = Column(String)
    # arbitrary_types_allowed = True

    def __init__(self, title, content, published, owner_id):
        self.title = title
        self.content = content
        self.published = published
        self.owner_id = owner_id

    class Config:
        arbitrary_types_allowed = True

    class model_config:
        arbitrary_types_allowed = True


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    owner = relationship("PostModel", back_populates="owner")

    def __init__(self, email, password):
        self.email = email
        self.password = pwd_context.hash(password)

    def check_password(self, password):
        print(self.password)
        return pwd_context.verify(password, self.password)


class Votes(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE", ), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE", ), primary_key=True)

    # owner = relationship("PostModel", back_populates="votes")

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
