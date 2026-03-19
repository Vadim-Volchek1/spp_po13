from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

engine = create_engine('sqlite:///computer_builds.db', echo=True)
Base = declarative_base()


class Manufacturer(Base):
    __tablename__ = 'manufacturers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50))
    founded_year = Column(Integer)

    components = relationship('Component', back_populates='manufacturer')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String)

    components = relationship('Component', back_populates='category')


class Component(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id', ondelete='SET NULL'))
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'))
    release_date = Column(Date)
    stock_quantity = Column(Integer, default=0)

    manufacturer = relationship('Manufacturer', back_populates='components')
    category = relationship('Category', back_populates='components')
    builds = relationship('BuildComponent', back_populates='component')


class Build(Base):
    __tablename__ = 'builds'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    build_date = Column(Date, default=date.today)
    total_price = Column(Float)
    purpose = Column(String(50))

    components = relationship('BuildComponent', back_populates='build')


class BuildComponent(Base):
    __tablename__ = 'build_components'

    id = Column(Integer, primary_key=True)
    build_id = Column(Integer, ForeignKey('builds.id', ondelete='CASCADE'), nullable=False)
    component_id = Column(Integer, ForeignKey('components.id', ondelete='CASCADE'), nullable=False)
    quantity = Column(Integer, default=1)

    build = relationship('Build', back_populates='components')
    component = relationship('Component', back_populates='builds')


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

print("Подключение к БД через SQLAlchemy успешно установлено!")
