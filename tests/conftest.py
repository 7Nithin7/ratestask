import pytest
from app import create_app
from app.extensions import db

# @pytest.fixture(scope="function")
# def flask_app():
#     app = create_app("test")
#     with app.test_client() as client:
#         ctx = app.app_context()
#         ctx.push()
#         yield client
#         ctx.pop()


@pytest.fixture(scope="function")
def flask_client():
    app = create_app("test")
    with app.test_client() as client:
        ctx = app.app_context()
        ctx.push()
        yield client
        ctx.pop()


@pytest.fixture
def setup_database(flask_client):
    """Fixture to set up the in-memory database with test data"""
    db.session.execute(
        """
        CREATE TABLE regions
        (slug text CONSTRAINT constraint_name PRIMARY KEY, name text, parent_slug text)
        """
    )
    db.session.execute(
        """
        CREATE TABLE ports
        (code text CONSTRAINT constraint_name PRIMARY KEY, name text, parent_slug text)
        """
    )
    db.session.execute(
        """
        CREATE TABLE prices
        (orig_code text, dest_code text, day date, price integer)
        """
    )


@pytest.fixture
def setup_test_data(setup_database):
    regions = [
        ("northern_europe", "Northern Europe", None),
        ("north_europe_main", "North Europe Main", "northern_europe"),
        ("uk_main", "North Europe Main", "north_europe_main"),
        ("china_main", "China Main", None),
        ("china_east_main", "China East Main", "china_main"),
    ]
    for slug, name, parent_slug in regions:
        db.session.execute(
            f"""
            INSERT INTO regions VALUES('{slug}', '{name}',{'null' if parent_slug is None else f"'{parent_slug}'"})
            """
        )

    ports = [
        ("DEBRV", "Bremerhaven", "north_europe_main"),
        ("GBSOU", "Southampton", "uk_main"),
        ("CNLYG", "Lianyungang", "china_east_main"),
        ("CNNBO", "Ningbo", "china_east_main"),
    ]
    for code, name, parent_slug in ports:
        db.session.execute(f"""INSERT INTO ports VALUES('{code}', '{name}','{parent_slug}')""")

    prices = [
        ("DEBRV", "CNLYG", "2016-01-01", 1000),
        ("DEBRV", "CNLYG", "2016-01-01", 1050),
        ("DEBRV", "CNLYG", "2016-01-01", 1100),
        ("DEBRV", "CNNBO", "2016-01-01", 980),
        ("DEBRV", "CNNBO", "2016-01-01", 1030),
        ("DEBRV", "CNNBO", "2016-01-01", 1080),
        ("GBSOU", "CNLYG", "2016-01-01", 930),
        ("GBSOU", "CNLYG", "2016-01-01", 975),
        ("GBSOU", "CNLYG", "2016-01-01", 1000),
        ("DEBRV", "CNLYG", "2016-01-02", 1010),
        ("DEBRV", "CNLYG", "2016-01-02", 1060),
        ("DEBRV", "CNLYG", "2016-01-02", 1110),
        ("GBSOU", "CNLYG", "2016-01-02", 960),
        ("GBSOU", "CNLYG", "2016-01-02", 985),
    ]
    for orig_code, dest_code, day, price in prices:
        db.session.execute(f"""INSERT INTO prices VALUES('{orig_code}', '{dest_code}', '{day}', {price})""")
