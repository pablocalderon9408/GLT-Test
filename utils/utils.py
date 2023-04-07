# Utils
from datetime import datetime

# SQLAlchemy
from sqlalchemy import Column, DateTime

# Database
from config.database import Base


class BaseModel(Base):
    """
    Base model for all models

    Include the created_at and updated_at fields
    to track all objects creation and modification.
    """

    __abstract__ = True

    created_at = Column(
        DateTime,
        default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )
