def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_books_with_records(client, three_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
        "id": 1,
        "title": "hello world",
        "description": "coding book"
    },
    {
        "id": 2,
        "title": "harry potter",
        "description": "magic book"
    },
    {
        "id": 3,
        "title": "solar system",
        "description": "space book"
    }
    ]

def test_get_one_valid_book(client, three_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "hello world",
        "description": "coding book"
    }

def test_get_one_invalid_book(client, three_saved_books):
    # Act
    response = client.get("/books/4")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": f"Book id_4 was not found.",
        "success": False
    }

def test_post_one_book(client):
    # Arrange
    data = {"title": "hello world", "description": "coding book"}
    # Act
    response = client.post("/books",\
        json=data)
    response_body = response.get_json()
    # Assert
    assert response.status_code == 201
    assert response_body == {
        "success": True,
        "message": "Book hello world has been created"
        }