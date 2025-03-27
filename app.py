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

# Fonction utilitaire pour se connecter à la base
def get_db_connection():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print("Erreur de connexion à la base de données :", e)
        return None

@app.route('/')
def home():
    conn = get_db_connection()
    if conn is None:
        return "Erreur de connexion à la base de données."
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM tasks")
        tasks = cursor.fetchall()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        return f"Erreur lors de la récupération des tâches : {e}"
    finally:
        conn.close()

@app.route('/add', methods=['POST'])
def add_task():
    conn = get_db_connection()
    if conn is None:
        return "Erreur de connexion à la base de données."
    
    try:
        title = request.form.get('title')
        if title:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            conn.commit()
        return redirect('/')
    except Exception as e:
        return f"Erreur lors de l'ajout de la tâche : {e}"
    finally:
        conn.close()

# Ne pas inclure app.run ici pour Azure, car Gunicorn est utilisé
# Mais tu peux l'activer en local pour tester :
# if __name__ == '__main__':
#     app.run(debug=True)
