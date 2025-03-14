from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/llibre')
def llibre():
    return render_template('llibre.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)  # Executa l'aplicació al port 5500