from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Admin schemas
class AdminBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    specialization: Optional[str] = None


class AdminCreate(AdminBase):
    pass


class AdminUpdate(AdminBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class AdminResponse(AdminBase):
    admin_id: int
    hire_date: datetime

    class Config:
        from_attributes = True


# Server schemas
class ServerBase(BaseModel):
    hostname: str
    ip_address: str
    os_type: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = "active"
    cpu_cores: Optional[int] = None
    ram_gb: Optional[int] = None
    disk_gb: Optional[int] = None


class ServerCreate(ServerBase):
    pass


class ServerUpdate(ServerBase):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None


class ServerResponse(ServerBase):
    server_id: int
    purchase_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# Service schemas
class ServiceBase(BaseModel):
    server_id: int
    service_name: str
    service_type: Optional[str] = None
    port: Optional[int] = None
    status: Optional[str] = "active"
    version: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    server_id: Optional[int] = None
    service_name: Optional[str] = None


class ServiceResponse(ServiceBase):
    service_id: int

    class Config:
        from_attributes = True


# MaintenanceLog schemas
class MaintenanceLogBase(BaseModel):
    server_id: int
    admin_id: int
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[Decimal] = None


class MaintenanceLogCreate(MaintenanceLogBase):
    pass


class MaintenanceLogUpdate(BaseModel):
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    end_time: Optional[datetime] = None
    cost: Optional[Decimal] = None


class MaintenanceLogResponse(MaintenanceLogBase):
    log_id: int
    start_time: datetime
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True


# Incident schemas
class IncidentBase(BaseModel):
    server_id: int
    admin_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "open"


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    admin_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None


class IncidentResponse(IncidentBase):
    incident_id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
