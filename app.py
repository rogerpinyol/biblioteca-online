from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Admin, Reader

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

def load_users():
    users = {}
    try:
        with open('data/users.txt', 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split(',')
                if len(fields) == 3:
                    username, password, role = fields
                    # Generate a simple ID (e.g., username-based for uniqueness)
                    user_id = username  # Could use a counter or UUID in a real app
                    password_hash = generate_password_hash(password)  # Hash the password
                    if role == 'admin':
                        user = Admin(user_id, username, password_hash)
                    else:  # Si no es admin, es un lector
                        user = Reader(user_id, username, password_hash)
                    users[username] = user
    except FileNotFoundError:
        print("users.txt not found; no users loaded.")
    return users

# Load users at startup
users = load_users()

def get_all_books():
    books = []
    try:
        with open('data/books.txt', 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 8:  # Ensure the line has all expected fields
                    categories = fields[3].split(',') if fields[3] else []
                    books.append({
                        'isbn': fields[0],
                        'name': fields[1],
                        'author': fields[2],
                        'categories': categories,
                        'editorial': fields[4],
                        'release_year': fields[5],
                        'cover': fields[6],
                        'description': fields[7]
                    })
    except FileNotFoundError:
        pass
    return books

@app.route('/')
def index():
    if 'usuari' in session:
        books = get_all_books()
        return render_template('index.html', usuari=session['usuari'], books=books)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuari = request.form['usuari']
        contrasenya = request.form['contrasenya']
        
        if usuari in users and users[usuari].check_password(contrasenya):
            session['usuari'] = usuari
            session['role'] = users[usuari].role  # Store role for later use
            flash('Login correcte!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuari o contrasenya incorrectes', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuari', None)
    session.pop('role', None)
    flash('Has tancat sessió correctament.', 'success')
    return redirect(url_for('index'))

def get_book_by_isbn(isbn):
    with open('data/books.txt', 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 8 and fields[0] == isbn:
                categories = fields[3].split(',') if fields[3] else []
                return {
                    'isbn': fields[0],
                    'name': fields[1],
                    'author': fields[2],
                    'categories': categories,
                    'editorial': fields[4],
                    'release_year': fields[5],
                    'cover': fields[6],
                    'description': fields[7]
                }
    return None

def get_reviews_by_isbn(isbn):
    reviews = []
    try:
        with open('data/reviews.txt', 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if fields[0] == isbn:
                    review_type = fields[1]
                    if review_type == 'numeric':
                        reviews.append({
                            'type': 'numeric',
                            'user': fields[2],
                            'timestamp': fields[3],
                            'rating': int(fields[4])
                        })
                    elif review_type == 'comment':
                        reviews.append({
                            'type': 'comment',
                            'user': fields[2],
                            'timestamp': fields[3],
                            'comment': fields[4]
                        })
                    elif review_type == 'recommendation':
                        recommendation = fields[4].lower() == 'yes'  # Convert to boolean
                        reviews.append({
                            'type': 'recommendation',
                            'user': fields[2],
                            'timestamp': fields[3],
                            'recommendation': recommendation
                        })
    except FileNotFoundError:
        pass
    return reviews

@app.route('/book/<isbn>')
def book_details(isbn):
    book = get_book_by_isbn(isbn)
    if not book:
        return "Book not found", 404
    reviews = get_reviews_by_isbn(isbn)
    numeric_reviews = [review['rating'] for review in reviews if review['type'] == 'numeric']
    average_rating = sum(numeric_reviews) / len(numeric_reviews) if numeric_reviews else 0
    recommendation_reviews = [review['recommendation'] for review in reviews if review['type'] == 'recommendation']
    recommendation_percentage = (sum(recommendation_reviews) / len(recommendation_reviews) * 100) if recommendation_reviews else 0
    return render_template('book.html', book=book, reviews=reviews, average_rating=average_rating, recommendation_percentage=recommendation_percentage)

@app.route('/covers/<filename>')
def serve_cover(filename):
    return send_from_directory('data/covers', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5500)