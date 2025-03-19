from flask import Flask, render_template, request, redirect, url_for, session, flash

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

@app.route('/template/login', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True, port=5500)