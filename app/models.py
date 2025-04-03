from sqlalchemy import Integer, String, Boolean, Column
from app.database import Base


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True)
    username = Column (String, nullable=False)
    password = Column (String, nullable=False)
    role= Column (String(10), nullable=False)

