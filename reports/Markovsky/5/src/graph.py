import os
from graphviz import Digraph


def create_db_schema():
    dot = Digraph(comment='Схема базы данных Сборка компьютера',
                  format='png',
                  graph_attr={'rankdir': 'LR', 'splines': 'polyline'})

    dot.attr('node', shape='plaintext', fontname='Arial')

    manufacturers = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD COLSPAN="2" BGCOLOR="lightblue"><B>manufacturers</B></TD></TR>
        <TR><TD PORT="id">id (PK)</TD><TD>INTEGER</TD></TR>
        <TR><TD>name</TD><TD>VARCHAR(100) NOT NULL</TD></TR>
        <TR><TD>country</TD><TD>VARCHAR(50)</TD></TR>
        <TR><TD>founded_year</TD><TD>INTEGER</TD></TR>
    </TABLE>>"""
    dot.node('manufacturers', manufacturers)

    categories = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD COLSPAN="2" BGCOLOR="lightblue"><B>categories</B></TD></TR>
        <TR><TD PORT="id">id (PK)</TD><TD>INTEGER</TD></TR>
        <TR><TD>name</TD><TD>VARCHAR(50) NOT NULL</TD></TR>
        <TR><TD>description</TD><TD>TEXT</TD></TR>
    </TABLE>>"""
    dot.node('categories', categories)

    components = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD COLSPAN="2" BGCOLOR="lightgreen"><B>components</B></TD></TR>
        <TR><TD PORT="id">id (PK)</TD><TD>INTEGER</TD></TR>
        <TR><TD>name</TD><TD>VARCHAR(200) NOT NULL</TD></TR>
        <TR><TD>price</TD><TD>DECIMAL(10,2) NOT NULL</TD></TR>
        <TR><TD PORT="manufacturer_id">manufacturer_id (FK)</TD><TD>INTEGER</TD></TR>
        <TR><TD PORT="category_id">category_id (FK)</TD><TD>INTEGER</TD></TR>
        <TR><TD>release_date</TD><TD>DATE</TD></TR>
        <TR><TD>stock_quantity</TD><TD>INTEGER DEFAULT 0</TD></TR>
    </TABLE>>"""
    dot.node('components', components)

    builds = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD COLSPAN="2" BGCOLOR="lightyellow"><B>builds</B></TD></TR>
        <TR><TD PORT="id">id (PK)</TD><TD>INTEGER</TD></TR>
        <TR><TD>name</TD><TD>VARCHAR(100) NOT NULL</TD></TR>
        <TR><TD>build_date</TD><TD>DATE DEFAULT CURRENT_DATE</TD></TR>
        <TR><TD>total_price</TD><TD>DECIMAL(10,2)</TD></TR>
        <TR><TD>purpose</TD><TD>VARCHAR(50)</TD></TR>
    </TABLE>>"""
    dot.node('builds', builds)

    build_components = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD COLSPAN="2" BGCOLOR="lightcoral"><B>build_components</B></TD></TR>
        <TR><TD PORT="id">id (PK)</TD><TD>INTEGER</TD></TR>
        <TR><TD PORT="build_id">build_id (FK)</TD><TD>INTEGER NOT NULL</TD></TR>
        <TR><TD PORT="component_id">component_id (FK)</TD><TD>INTEGER NOT NULL</TD></TR>
        <TR><TD>quantity</TD><TD>INTEGER DEFAULT 1</TD></TR>
    </TABLE>>"""
    dot.node('build_components', build_components)

    dot.edge('manufacturers:id', 'components:manufacturer_id')
    dot.edge('categories:id', 'components:category_id')
    dot.edge('builds:id', 'build_components:build_id')
    dot.edge('components:id', 'build_components:component_id')

    legend = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD COLSPAN="2" BGCOLOR="gray"><B>Легенда</B></TD></TR>
        <TR><TD>PK</TD><TD>Primary Key</TD></TR>
        <TR><TD>FK</TD><TD>Foreign Key</TD></TR>
        <TR><TD>1 --- *</TD><TD>Один ко многим</TD></TR>
    </TABLE>>"""
    dot.node('legend', legend, shape='plaintext')
    dot.render('db_schema', view=True, cleanup=True)


if __name__ == '__main__':
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
    create_db_schema()
