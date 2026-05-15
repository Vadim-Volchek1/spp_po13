from typing import Optional

from sqlalchemy.orm import Session

from models import Admin, Server, Service, MaintenanceLog, Incident
from schemas import (
    AdminCreate, AdminUpdate, ServerCreate, ServerUpdate,
    ServiceCreate, ServiceUpdate, MaintenanceLogCreate, MaintenanceLogUpdate,
    IncidentCreate, IncidentUpdate
)


# Admin CRUD
def create_admin(db: Session, admin: AdminCreate):
    db_admin = Admin(**admin.model_dump())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def get_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Admin).offset(skip).limit(limit).all()


def get_admin(db: Session, admin_id: int):
    return db.query(Admin).filter(Admin.admin_id == admin_id).first()


def update_admin(db: Session, admin_id: int, admin_update: AdminUpdate):
    db_admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()
    if not db_admin:
        return None
    for field, value in admin_update.model_dump(exclude_unset=True).items():
        setattr(db_admin, field, value)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def delete_admin(db: Session, admin_id: int):
    db_admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()
    if not db_admin:
        return None
    db.delete(db_admin)
    db.commit()
    return db_admin


# Server CRUD
def create_server(db: Session, server: ServerCreate):
    db_server = Server(**server.model_dump())
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server


def get_servers(db: Session, skip: int = 0, limit: int = 100,
                status: Optional[str] = None):
    query = db.query(Server)
    if status:
        query = query.filter(Server.status == status)
    return query.offset(skip).limit(limit).all()


def get_server(db: Session, server_id: int):
    return db.query(Server).filter(Server.server_id == server_id).first()


def update_server(db: Session, server_id: int, server_update: ServerUpdate):
    db_server = db.query(Server).filter(Server.server_id == server_id).first()
    if not db_server:
        return None
    for field, value in server_update.model_dump(exclude_unset=True).items():
        setattr(db_server, field, value)
    db.commit()
    db.refresh(db_server)
    return db_server


def delete_server(db: Session, server_id: int):
    db_server = db.query(Server).filter(Server.server_id == server_id).first()
    if not db_server:
        return None
    db.delete(db_server)
    db.commit()
    return db_server


# Service CRUD
def create_service(db: Session, service: ServiceCreate):
    db_service = Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_services(db: Session, skip: int = 0, limit: int = 100,
                 server_id: Optional[int] = None):
    query = db.query(Service)
    if server_id:
        query = query.filter(Service.server_id == server_id)
    return query.offset(skip).limit(limit).all()


def get_service(db: Session, service_id: int):
    return db.query(Service).filter(Service.service_id == service_id).first()


def update_service(db: Session, service_id: int, service_update: ServiceUpdate):
    db_service = db.query(Service).filter(Service.service_id == service_id).first()
    if not db_service:
        return None
    for field, value in service_update.model_dump(exclude_unset=True).items():
        setattr(db_service, field, value)
    db.commit()
    db.refresh(db_service)
    return db_service


def delete_service(db: Session, service_id: int):
    db_service = db.query(Service).filter(Service.service_id == service_id).first()
    if not db_service:
        return None
    db.delete(db_service)
    db.commit()
    return db_service


# MaintenanceLog CRUD
def create_maintenance_log(db: Session, log: MaintenanceLogCreate):
    db_log = MaintenanceLog(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_maintenance_logs(db: Session, skip: int = 0, limit: int = 100,
                         server_id: Optional[int] = None):
    query = db.query(MaintenanceLog)
    if server_id:
        query = query.filter(MaintenanceLog.server_id == server_id)
    return query.offset(skip).limit(limit).all()


def get_maintenance_log(db: Session, log_id: int):
    return db.query(MaintenanceLog).filter(MaintenanceLog.log_id == log_id).first()


def update_maintenance_log(db: Session, log_id: int, log_update: MaintenanceLogUpdate):
    db_log = db.query(MaintenanceLog).filter(MaintenanceLog.log_id == log_id).first()
    if not db_log:
        return None
    for field, value in log_update.model_dump(exclude_unset=True).items():
        setattr(db_log, field, value)
    db.commit()
    db.refresh(db_log)
    return db_log


def delete_maintenance_log(db: Session, log_id: int):
    db_log = db.query(MaintenanceLog).filter(MaintenanceLog.log_id == log_id).first()
    if not db_log:
        return None
    db.delete(db_log)
    db.commit()
    return db_log


# Incident CRUD
def create_incident(db: Session, incident: IncidentCreate):
    db_incident = Incident(**incident.model_dump())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


def get_incidents(db: Session, skip: int = 0, limit: int = 100,
                  status: Optional[str] = None, priority: Optional[str] = None):
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == status)
    if priority:
        query = query.filter(Incident.priority == priority)
    return query.offset(skip).limit(limit).all()


def get_incident(db: Session, incident_id: int):
    return db.query(Incident).filter(Incident.incident_id == incident_id).first()


def update_incident(db: Session, incident_id: int, incident_update: IncidentUpdate):
    db_incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not db_incident:
        return None
    for field, value in incident_update.model_dump(exclude_unset=True).items():
        setattr(db_incident, field, value)
    db.commit()
    db.refresh(db_incident)
    return db_incident


def delete_incident(db: Session, incident_id: int):
    db_incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not db_incident:
        return None
    db.delete(db_incident)
    db.commit()
    return db_incident
