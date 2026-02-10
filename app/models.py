from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hostname: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    ip: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    environment: Mapped[str] = mapped_column(String(50), default="prod")
    os: Mapped[str] = mapped_column(String(100), default="linux")
    owner: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(String(30), default="active")
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    services: Mapped[list["Service"]] = relationship(back_populates="asset", cascade="all, delete-orphan")


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"), index=True)
    repo_url: Mapped[str] = mapped_column(String(300), default="")
    deploy_method: Mapped[str] = mapped_column(String(100), default="ansible")
    owner: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(String(30), default="running")
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    asset: Mapped[Asset] = relationship(back_populates="services")
    changes: Mapped[list["ChangeRecord"]] = relationship(back_populates="service", cascade="all, delete-orphan")


class ChangeRecord(Base):
    __tablename__ = "changes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), index=True)
    risk_level: Mapped[str] = mapped_column(String(20), default="medium")
    change_window: Mapped[str] = mapped_column(String(100), default="")
    executor: Mapped[str] = mapped_column(String(100), default="")
    approver: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(String(30), default="pending")
    rollback_plan: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    service: Mapped[Service] = relationship(back_populates="changes")
