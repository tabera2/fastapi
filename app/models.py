from sqlalchemy import Column
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
class Post(Base):
    __tablename__ = "posts"
    id = Column(int, primary_key=True, nullable=False)
    title = Column(str, nullable=False)
    content = Column(str, nullable=False)
    published = Column(bool, default=True, nullable=False)
    created_at = Column(TIMESTAMP (timezone=True), nullable=False, server_default=tex)