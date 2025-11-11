from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from models.db_init import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, primary_key=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="ROLE_USER")

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }
