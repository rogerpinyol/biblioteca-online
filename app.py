from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

def get_book_by_isbn(isbn):
    with open('data/books.txt', 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if fields[0] == isbn:
                categories = fields[3].split(',') if fields[3] else []
                return {
                    'isbn': fields[0],
                    'name': fields[1],
                    'author': fields[2],
                    'categories': categories,
                    'language': fields[4],
                    'release_year': fields[5],
                    'cover': fields[6]
                }
    return None

@app.route('/book/<isbn>')
def book_details(isbn):
    book = get_book_by_isbn(isbn)
    if book:
        return render_template('book.html', book=book)
    else:
        return "Book not found", 404

@app.route('/covers/<filename>')
def serve_cover(filename):
    return send_from_directory('data/covers', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/llibre')
def llibre():
    return render_template('llibre.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/llibre')
def llibre():
    return render_template('llibre.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)  # Executa l'aplicació al port 5500