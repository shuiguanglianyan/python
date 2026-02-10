from typing import Optional

from pydantic import BaseModel, Field


class AssetCreate(BaseModel):
    hostname: str = Field(min_length=1)
    ip: str = Field(min_length=1)
    environment: str = "prod"
    os: str = "linux"
    owner: str = ""
    status: str = "active"
    note: str = ""


class AssetUpdate(BaseModel):
    hostname: Optional[str] = None
    ip: Optional[str] = None
    environment: Optional[str] = None
    os: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    note: Optional[str] = None


class ServiceCreate(BaseModel):
    name: str = Field(min_length=1)
    asset_id: int
    repo_url: str = ""
    deploy_method: str = "ansible"
    owner: str = ""
    status: str = "running"
    note: str = ""


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    asset_id: Optional[int] = None
    repo_url: Optional[str] = None
    deploy_method: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    note: Optional[str] = None


class ChangeCreate(BaseModel):
    title: str = Field(min_length=1)
    service_id: int
    risk_level: str = "medium"
    change_window: str = ""
    executor: str = ""
    approver: str = ""
    status: str = "pending"
    rollback_plan: str = ""


class ChangeUpdate(BaseModel):
    title: Optional[str] = None
    service_id: Optional[int] = None
    risk_level: Optional[str] = None
    change_window: Optional[str] = None
    executor: Optional[str] = None
    approver: Optional[str] = None
    status: Optional[str] = None
    rollback_plan: Optional[str] = None
