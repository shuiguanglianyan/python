from pydantic import BaseModel, Field


class AssetCreate(BaseModel):
    hostname: str = Field(min_length=1)
    ip: str = Field(min_length=1)
    environment: str = "prod"
    os: str = "linux"
    owner: str = ""
    status: str = "active"
    note: str = ""


class ServiceCreate(BaseModel):
    name: str = Field(min_length=1)
    asset_id: int
    repo_url: str = ""
    deploy_method: str = "ansible"
    owner: str = ""
    status: str = "running"
    note: str = ""


class ChangeCreate(BaseModel):
    title: str = Field(min_length=1)
    service_id: int
    risk_level: str = "medium"
    change_window: str = ""
    executor: str = ""
    approver: str = ""
    status: str = "pending"
    rollback_plan: str = ""
