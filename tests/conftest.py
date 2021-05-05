import pytest
from sqlalchemy.orm import with_expression
from app import create_app
from app import db
from app.models.book import Book

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def three_saved_books(app):
    # Arrange
    hello_world = Book(
        title="hello world",
        description="coding book"
    )
    harry_potter = Book(
        title="harry potter",
        description="magic book"
    )
    solar_system = Book(
        title="solar system",
        description="space book"
    )

    db.session.add_all([hello_world, harry_potter, solar_system])
    db.session.commit()

