# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import pyodbc

# ==============================
# Configuración inicial
# ==============================
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# ==============================
# Conexión a SQL Server
# ==============================
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')}"
        )
        return conn
    except Exception as e:
        print(f"❌ Error al conectar con SQL Server: {e}")
        return None

# ==============================
# Rutas principales
# ==============================
@app.route("/")
def index():
    """Página principal con categorías destacadas"""
    conn = get_db_connection()
    categorias = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 6 id, nombre, descripcion FROM Categorias")
        categorias = cursor.fetchall()
        conn.close()
    return render_template("index.html", categorias=categorias)


@app.route("/productos")
def productos():
    """Listado de productos"""
    conn = get_db_connection()
    productos = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio, c.nombre as categoria
            FROM Productos p
            INNER JOIN Categorias c ON p.categoria_id = c.id
        """)
        productos = cursor.fetchall()
        conn.close()
    return render_template("productos.html", productos=productos)


@app.route("/producto/<int:producto_id>")
def producto_detalle(producto_id):
    """Detalle de un producto"""
    conn = get_db_connection()
    producto = None
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio, c.nombre as categoria
            FROM Productos p
            INNER JOIN Categorias c ON p.categoria_id = c.id
            WHERE p.id = ?
        """, (producto_id,))
        producto = cursor.fetchone()
        conn.close()
    if not producto:
        flash("El producto no existe", "error")
        return redirect(url_for("productos"))
    return render_template("producto_detalle.html", producto=producto)


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    """Página de contacto"""
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        mensaje = request.form.get("mensaje")
        flash("Gracias por tu mensaje. Te responderemos pronto.", "success")
        return redirect(url_for("contacto"))
    return render_template("contacto.html")


# ==============================
# Punto de entrada
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
