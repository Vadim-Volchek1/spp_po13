import enum
from datetime import datetime
from urllib.parse import quote_plus

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, Enum, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class ServerStatus(str, enum.Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class IncidentStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Admin(Base):
    __tablename__ = 'admins'

    admin_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    specialization = Column(String(100))
    hire_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    maintenance_logs = relationship("MaintenanceLog", back_populates="admin")
    incidents = relationship("Incident", back_populates="assigned_admin")


class Server(Base):
    __tablename__ = 'servers'

    server_id = Column(Integer, primary_key=True)
    hostname = Column(String(100), unique=True, nullable=False)
    ip_address = Column(String(15), nullable=False)
    os_type = Column(String(50))
    location = Column(String(100))
    status = Column(Enum(ServerStatus), default=ServerStatus.ACTIVE)
    cpu_cores = Column(Integer)
    ram_gb = Column(Integer)
    disk_gb = Column(Integer)
    purchase_date = Column(DateTime)

    # Relationships
    services = relationship("Service", back_populates="server")
    maintenance_logs = relationship("MaintenanceLog", back_populates="server")
    incidents = relationship("Incident", back_populates="server")


class Service(Base):
    __tablename__ = 'services'

    service_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.server_id'), nullable=False)
    service_name = Column(String(100), nullable=False)
    service_type = Column(String(50))
    port = Column(Integer)
    status = Column(Enum(ServerStatus), default=ServerStatus.ACTIVE)
    version = Column(String(50))

    # Relationships
    server = relationship("Server", back_populates="services")


class MaintenanceLog(Base):
    __tablename__ = 'maintenance_logs'

    log_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.server_id'), nullable=False)
    admin_id = Column(Integer, ForeignKey('admins.admin_id'), nullable=False)
    maintenance_type = Column(String(50))
    description = Column(Text)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    cost = Column(DECIMAL(10, 2))

    # Relationships
    server = relationship("Server", back_populates="maintenance_logs")
    admin = relationship("Admin", back_populates="maintenance_logs")


class Incident(Base):
    __tablename__ = 'incidents'

    incident_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.server_id'), nullable=False)
    admin_id = Column(Integer, ForeignKey('admins.admin_id'))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.OPEN)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)

    # Relationships
    server = relationship("Server", back_populates="incidents")
    assigned_admin = relationship("Admin", back_populates="incidents")


# Database connection
DB_USER = "postgres"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "sysadmin_db"

DATABASE_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
