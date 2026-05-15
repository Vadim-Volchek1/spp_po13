from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models import init_db, get_db
from schemas import (
    AdminCreate, AdminUpdate, AdminResponse,
    ServerCreate, ServerUpdate, ServerResponse,
    ServiceCreate, ServiceUpdate, ServiceResponse,
    MaintenanceLogCreate, MaintenanceLogUpdate, MaintenanceLogResponse,
    IncidentCreate, IncidentUpdate, IncidentResponse
)
import crud

app = FastAPI(title="System Administrator API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    init_db()


# ADMIN ENDPOINTS

@app.post("/admins/", response_model=AdminResponse, tags=["Admins"])
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    # Создание нового системного администратора
    return crud.create_admin(db, admin)


@app.get("/admins/", response_model=List[AdminResponse], tags=["Admins"])
def read_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Получение списка всех администраторов
    return crud.get_admins(db, skip=skip, limit=limit)


@app.get("/admins/{admin_id}", response_model=AdminResponse, tags=["Admins"])
def read_admin(admin_id: int, db: Session = Depends(get_db)):
    # Получение информации об администраторе по ID
    db_admin = crud.get_admin(db, admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin


@app.put("/admins/{admin_id}", response_model=AdminResponse, tags=["Admins"])
def update_admin(admin_id: int, admin: AdminUpdate, db: Session = Depends(get_db)):
    # Обновление информации об администраторе
    db_admin = crud.update_admin(db, admin_id, admin)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin


@app.delete("/admins/{admin_id}", response_model=AdminResponse, tags=["Admins"])
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    # Удаление администратора
    db_admin = crud.delete_admin(db, admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin


# SERVER ENDPOINTS

@app.post("/servers/", response_model=ServerResponse, tags=["Servers"])
def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    # Создание нового сервера
    return crud.create_server(db, server)


@app.get("/servers/", response_model=List[ServerResponse], tags=["Servers"])
def read_servers(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Получение списка серверов (с фильтрацией по статусу)
    return crud.get_servers(db, skip=skip, limit=limit, status=status)


@app.get("/servers/{server_id}", response_model=ServerResponse, tags=["Servers"])
def read_server(server_id: int, db: Session = Depends(get_db)):
    # Получение информации о сервере по ID
    db_server = crud.get_server(db, server_id)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server


@app.put("/servers/{server_id}", response_model=ServerResponse, tags=["Servers"])
def update_server(server_id: int, server: ServerUpdate, db: Session = Depends(get_db)):
    # Обновление информации о сервере
    db_server = crud.update_server(db, server_id, server)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server


@app.delete("/servers/{server_id}", response_model=ServerResponse, tags=["Servers"])
def delete_server(server_id: int, db: Session = Depends(get_db)):
    # Удаление сервера
    db_server = crud.delete_server(db, server_id)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server


# SERVICE ENDPOINTS

@app.post("/services/", response_model=ServiceResponse, tags=["Services"])
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    # Создание новой службы на сервере
    return crud.create_service(db, service)


@app.get("/services/", response_model=List[ServiceResponse], tags=["Services"])
def read_services(
    skip: int = 0,
    limit: int = 100,
    server_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    # Получение списка служб (с фильтрацией по серверу)
    return crud.get_services(db, skip=skip, limit=limit, server_id=server_id)


@app.get("/services/{service_id}", response_model=ServiceResponse, tags=["Services"])
def read_service(service_id: int, db: Session = Depends(get_db)):
    # Получение информации о службе по ID
    db_service = crud.get_service(db, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service


@app.put("/services/{service_id}", response_model=ServiceResponse, tags=["Services"])
def update_service(service_id: int, service: ServiceUpdate, db: Session = Depends(get_db)):
    # Обновление информации о службе
    db_service = crud.update_service(db, service_id, service)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service


@app.delete("/services/{service_id}", response_model=ServiceResponse, tags=["Services"])
def delete_service(service_id: int, db: Session = Depends(get_db)):
    # Удаление службы
    db_service = crud.delete_service(db, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service


# MAINTENANCE LOG ENDPOINTS

@app.post("/maintenance/", response_model=MaintenanceLogResponse, tags=["Maintenance"])
def create_maintenance_log(log: MaintenanceLogCreate, db: Session = Depends(get_db)):
    # Создание записи о техническом обслуживании
    return crud.create_maintenance_log(db, log)


@app.get("/maintenance/", response_model=List[MaintenanceLogResponse], tags=["Maintenance"])
def read_maintenance_logs(
    skip: int = 0,
    limit: int = 100,
    server_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    # Получение журнала обслуживания (с фильтрацией по серверу)
    return crud.get_maintenance_logs(db, skip=skip, limit=limit, server_id=server_id)


@app.get("/maintenance/{log_id}", response_model=MaintenanceLogResponse, tags=["Maintenance"])
def read_maintenance_log(log_id: int, db: Session = Depends(get_db)):
    # Получение записи об обслуживании по ID
    db_log = crud.get_maintenance_log(db, log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    return db_log


@app.put("/maintenance/{log_id}", response_model=MaintenanceLogResponse, tags=["Maintenance"])
def update_maintenance_log(log_id: int, log: MaintenanceLogUpdate, db: Session = Depends(get_db)):
    # Обновление записи об обслуживании (завершение работ)
    db_log = crud.update_maintenance_log(db, log_id, log)
    if not db_log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    return db_log


@app.delete("/maintenance/{log_id}", response_model=MaintenanceLogResponse, tags=["Maintenance"])
def delete_maintenance_log(log_id: int, db: Session = Depends(get_db)):
    # Удаление записи об обслуживании
    db_log = crud.delete_maintenance_log(db, log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    return db_log


# INCIDENT ENDPOINTS

@app.post("/incidents/", response_model=IncidentResponse, tags=["Incidents"])
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    # Создание нового инцидента
    return crud.create_incident(db, incident)


@app.get("/incidents/", response_model=List[IncidentResponse], tags=["Incidents"])
def read_incidents(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Получение списка инцидентов (с фильтрацией по статусу и приоритету)
    return crud.get_incidents(db, skip=skip, limit=limit, status=status, priority=priority)


@app.get("/incidents/{incident_id}", response_model=IncidentResponse, tags=["Incidents"])
def read_incident(incident_id: int, db: Session = Depends(get_db)):
    # Получение информации об инциденте по ID
    db_incident = crud.get_incident(db, incident_id)
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident


@app.put("/incidents/{incident_id}", response_model=IncidentResponse, tags=["Incidents"])
def update_incident(incident_id: int, incident: IncidentUpdate, db: Session = Depends(get_db)):
    # Обновление инцидента (назначение админа, изменение статуса)
    db_incident = crud.update_incident(db, incident_id, incident)
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident


@app.delete("/incidents/{incident_id}", response_model=IncidentResponse, tags=["Incidents"])
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    # Удаление инцидента
    db_incident = crud.delete_incident(db, incident_id)
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
