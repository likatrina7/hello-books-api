from app import db
from app.models.book import Book
from flask import Blueprint,request,jsonify

# bp_01
books_bp = Blueprint("books", __name__, url_prefix="/books")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_single_book(book_id):
    if not is_int(book_id):
        return {
        "message": f"Book id is must be integer.",
        "success": False
    }, 404

    book = Book.query.get(book_id)
    if not book:
        return {
        "message": f"Book id_{book_id} was not found.",
        "success": False
    }, 404
    elif request.method == "GET":
        return book.to_json(), 200
    elif request.method == "PUT":
        data_to_update = request.get_json()
        book.title = data_to_update["title"]
        book.description = data_to_update["description"]
        db.session.commit()
        return {
            "success": True,
            "message": f"Book id_{book_id} successfully updated"
        }, 200
    else:
        db.session.delete(book)
        db.session.commit()
        return {
            "success": True,
            "message": f"Book id_{book_id} successfully deleted"
        }, 200

@books_bp.route('', methods=["GET"], strict_slashes=False)
def get_all_books():
    # new code for check Query Param
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
    # new code end
    books_response = []
    for book in books:
        books_response.append(book.to_json())
    return jsonify(books_response), 200

@books_bp.route('', methods=["POST"], strict_slashes=False)
def create_book():
    request_body = request.get_json()
    new_book = Book(title = request_body["title"],\
        description = request_body["description"])

    db.session.add(new_book)
    db.session.commit()
    return {
        "success": True,\
        "message": f"Book {new_book.title} has been created"
        }, 201

# bp_02
# hello_world_bp = Blueprint("hello_world", __name__)

# @hello_world_bp.route('/hello-world', methods=["GET"])
# def get_hello_world():
#     my_reponse = "Hello, World!"
#     return my_reponse

# @hello_world_bp.route('/hello-world/JSON', methods=["GET"])
# def hello_world_json():
#     return{
#         'name': 'Kat',
#         'message': 'Morning!'
#     }, 200

# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body 