from flask import Flask, render_template
import pyodbc
import os
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
load_dotenv()

app = Flask(__name__)

# Conexión a SQL Server
def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASS')}"
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
