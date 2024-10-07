from flask import Flask, render_template, request, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Substitua por uma chave secreta segura

auth = HTTPBasicAuth()

# Usuários para autenticação básica (apenas admin)
users = {
    "admin": generate_password_hash("davinhe")  # Substitua "sua_senha_aqui" por uma senha segura
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

# Inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            mensagem TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        mensagem = request.form['mensagem']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contatos (nome, email, telefone, mensagem)
            VALUES (?, ?, ?, ?)
        ''', (nome, email, telefone, mensagem))
        conn.commit()
        conn.close()

        flash('Sua mensagem foi enviada com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/admin')
@auth.login_required
def admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contatos ORDER BY id DESC')
    contatos = cursor.fetchall()
    conn.close()
    return render_template('admin.html', contatos=contatos)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
