from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# Connexion à la base Azure SQL
server = 'serveur-sene.database.windows.net'
database = 'taskdb-sene'
username = 'adminsene'
password = 'Netta-1999'
driver = '{ODBC Driver 18 for SQL Server}'

connection_string = f"""
    Driver={driver};
    Server=tcp:{server},1433;
    Database={database};
    Uid={username};
    Pwd={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
"""

try:
    conn = pyodbc.connect(connection_string)
except Exception as e:
    print("Erreur de connexion à la base de données :", e)

@app.route('/')
def home():
    if conn is None:
        return "Erreur de connexion à la base de données."
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM tasks")
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    if conn is None:
        return "Erreur de connexion à la base de données."
    title = request.form.get('title')
    if title:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
