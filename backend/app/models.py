# backend/app/models.py

import enum
from datetime import datetime
from sqlalchemy.types import JSON
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Numeric,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship

from . import db  # import the single db instance from __init__.py


class User(db.Model):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # "provider" or "customer"
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    provider_profile = relationship("ProviderProfile", uselist=False, back_populates="user")
    customer_profile = relationship("CustomerProfile", uselist=False, back_populates="user")
    works = relationship("Work", back_populates="provider", cascade="all, delete-orphan")


class ProviderProfile(db.Model):
    __tablename__ = "provider_profile"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False, unique=True)
    bio = Column(Text, nullable=True)
    equipment_specs = Column(String(255), nullable=True)
    pricing_info = Column(JSON, nullable=True)
    location = Column(String(255), nullable=True)

    user = relationship("User", back_populates="provider_profile")


class CustomerProfile(db.Model):
    __tablename__ = "customer_profile"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False, unique=True)
    phone = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)

    user = relationship("User", back_populates="customer_profile")


class JobRequest(db.Model):
    __tablename__ = "job_request"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    provider_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    model_file_url = Column(String(512), nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    price_offered = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("User", foreign_keys=[customer_id])
    provider = relationship("User", foreign_keys=[provider_id])
    messages = relationship("Message", back_populates="job_request", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="job_request", cascade="all, delete-orphan")


class Message(db.Model):
    __tablename__ = "message"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    job_request_id = Column(BigInteger, ForeignKey("job_request.id"), nullable=False)
    sender_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    job_request = relationship("JobRequest", back_populates="messages")
    sender = relationship("User")


class Review(db.Model):
    __tablename__ = "review"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    job_request_id = Column(BigInteger, ForeignKey("job_request.id"), nullable=False)
    reviewer_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    job_request = relationship("JobRequest", back_populates="reviews")
    reviewer = relationship("User")


class Work(db.Model):
    __tablename__ = "works"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    provider_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    image_url = Column(String(512), nullable=False)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    provider = relationship("User", back_populates="works")
