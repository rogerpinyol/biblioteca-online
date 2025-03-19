from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Canvia això per una clau segura

# Usuaris predefinits
usuaris = {
    'client': 'client',
    'admin': 'admin'
}

@app.route('/')
def index():
    if 'usuari' in session:
        return render_template('index.html', usuari=session['usuari'])
    return redirect(url_for('login'))

@app.route('/llibre')
def llibre():
    if 'usuari' in session:
        return render_template('llibre.html', usuari=session['usuari'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuari = request.form['usuari']
        contrasenya = request.form['contrasenya']
        
        if usuari in usuaris and usuaris[usuari] == contrasenya:
            session['usuari'] = usuari
            flash('Login correcte!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuari o contrasenya incorrectes', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuari', None)
    flash('Has sortit de la sessió', 'success')
    return redirect(url_for('login'))

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

if __name__ == '__main__':
    app.run(debug=True, port=5500)