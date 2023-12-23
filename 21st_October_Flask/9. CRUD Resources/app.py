from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Sample data (in-memory database for simplicity)
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"}
]

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    print(books)
    # return jsonify(books)
    return render_template('index.html', books= books)

# Get a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    print(book)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    new_book = {
        "id": len(books) + 1,
        "title": request.json.get("title"),
        "author": request.json.get("author")
    }
    print(new_book)
    ids = list(map(lambda d: d['id'], books))
    if new_book['id'] not in ids:
        books.append(new_book)
        return jsonify(new_book), 201
    else:
        return jsonify({"error": "Book already exists"}), 404
    # new_book = {
    #     "id": len(books) + 1,
    #     "title": request.form["title"],
    #     "author": request.form["author"]
    # }
    return render_template('index.html')

# Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        title = [item["title"] for item in books if item["id"] == book_id][0]
        author = [item["author"] for item in books if item["id"] == book_id][0]
        book['title'] = request.json.get('title', book['title'])
        book['author'] = request.json.get('author', book['author'])
        print(f"Updated: {title} - {book['title']}, {author} - {book['author']}")
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    ids = [d['id'] for d in books]
    print(ids)
    if book_id in ids:
        book = [item["title"] for item in books if item["id"] == book_id][0]
        books = [book for book in books if book['id'] != book_id]
        print(f"{book_id} deleted")
        return jsonify({"id": f"Book - {book} deleted"})
    else:
        return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
