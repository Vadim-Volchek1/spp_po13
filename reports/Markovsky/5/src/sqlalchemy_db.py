from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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


def add_manufacturer(name, country=None, founded_year=None):
    manufacturer = Manufacturer(name=name, country=country, founded_year=founded_year)
    session.add(manufacturer)
    session.commit()
    print(f"Производитель {name} добавлен с id {manufacturer.id}")
    return manufacturer


def add_category(name, description=None):
    category = Category(name=name, description=description)
    session.add(category)
    session.commit()
    print(f"Категория {name} добавлена с id {category.id}")
    return category


def add_component(name, price, manufacturer_id=None, category_id=None, stock_quantity=0):
    component = Component(
        name=name,
        price=price,
        manufacturer_id=manufacturer_id,
        category_id=category_id,
        stock_quantity=stock_quantity
    )
    session.add(component)
    session.commit()
    print(f"Компонент {name} добавлен с id {component.id}")
    return component


def add_build(name, purpose=None, total_price=None):
    build = Build(name=name, purpose=purpose, total_price=total_price)
    session.add(build)
    session.commit()
    print(f"Сборка {name} добавлена с id {build.id}")
    return build


def add_component_to_build(build_id, component_id, quantity=1):
    build_component = BuildComponent(
        build_id=build_id,
        component_id=component_id,
        quantity=quantity
    )
    session.add(build_component)
    session.commit()
    print(f"Компонент {component_id} добавлен в сборку {build_id} (кол-во: {quantity})")
    return build_component


def get_all_manufacturers():
    manufacturers = session.query(Manufacturer).all()
    print("ВСЕ ПРОИЗВОДИТЕЛИ")
    for m in manufacturers:
        print(f"ID: {m.id}, Название: {m.name}, Страна: {m.country}")
    return manufacturers


def get_all_components():
    components = session.query(Component).all()
    print("ВСЕ КОМПОНЕНТЫ")
    for c in components:
        print(f"ID: {c.id}, Название: {c.name}, Цена: {c.price}, Кол-во: {c.stock_quantity}")
    return components


def get_components_by_category(category_id):
    components = session.query(Component).filter(Component.category_id == category_id).all()
    print(f"КОМПОНЕНТЫ КАТЕГОРИИ {category_id}")
    for c in components:
        print(f"ID: {c.id}, Название: {c.name}, Цена: {c.price}")
    return components


def get_build_details(build_id):
    build = session.query(Build).filter(Build.id == build_id).first()
    if build:
        print(f"СБОРКА: {build.name}")
        print(f"ID: {build.id}, Дата: {build.build_date}, Цель: {build.purpose}")
        print("Компоненты:")
        total = 0
        for bc in build.components:
            comp = bc.component
            subtotal = comp.price * bc.quantity
            total += subtotal
            print(f"- {comp.name} x{bc.quantity} = {comp.price} * {bc.quantity} = {subtotal} руб.")
        print(f"ИТОГО: {total} руб.")
        return build
    return None


def update_component_price(component_id, new_price):
    component = session.query(Component).filter(Component.id == component_id).first()
    if component:
        old_price = component.price
        component.price = new_price
        session.commit()
        print(f"Цена компонента {component.name} изменена с {old_price} на {new_price}")
    else:
        print(f"Компонент с id {component_id} не найден")


def update_manufacturer_country(manufacturer_id, new_country):
    manufacturer = session.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if manufacturer:
        old_country = manufacturer.country
        manufacturer.country = new_country
        session.commit()
        print(f"Страна производителя {manufacturer.name} изменена с {old_country} на {new_country}")
    else:
        print(f"Производитель с id {manufacturer_id} не найден")


def update_component_quantity(component_id, new_quantity):
    component = session.query(Component).filter(Component.id == component_id).first()
    if component:
        component.stock_quantity = new_quantity
        session.commit()
        print(f"Количество компонента {component.name} на складе обновлено до {new_quantity}")
    else:
        print(f"Компонент с id {component_id} не найден")


def delete_manufacturer(manufacturer_id):
    manufacturer = session.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if manufacturer:
        name = manufacturer.name
        session.delete(manufacturer)
        session.commit()
        print(f"Производитель {name} удален")
    else:
        print(f"Производитель с id {manufacturer_id} не найден")


def delete_component(component_id):
    component = session.query(Component).filter(Component.id == component_id).first()
    if component:
        name = component.name
        session.delete(component)
        session.commit()
        print(f"Компонент {name} удален")
    else:
        print(f"Компонент с id {component_id} не найден")


def delete_build(build_id):
    build = session.query(Build).filter(Build.id == build_id).first()
    if build:
        name = build.name
        session.delete(build)
        session.commit()
        print(f"Сборка {name} удалена")
    else:
        print(f"Сборка с id {build_id} не найдена")
