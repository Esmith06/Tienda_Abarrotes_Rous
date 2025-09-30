import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pyodbc
from dotenv import load_dotenv

# ==============================
# 📌 Punto 1 — Configuración del proyecto y conexión a SQL Server
# ==============================

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Conexión a SQL Server
def get_db_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER', 'localhost')};"
        f"DATABASE={os.getenv('DB_NAME', 'tienda_abarrotes')};"
        f"UID={os.getenv('DB_USER', 'sa')};"
        f"PWD={os.getenv('DB_PASSWORD', 'your_password')}"
    )
    return conn


# ==============================
# 📌 Punto 2 — Página principal e indexación de productos
# ==============================
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, stock FROM Productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template("index.html", productos=productos)


# ==============================
# 📌 Punto 3 — Página de productos por categoría
# ==============================
@app.route('/productos/<int:categoria_id>')
def productos_categoria(categoria_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, c.nombre AS categoria
        FROM Productos p
        INNER JOIN Categorias c ON p.categoria_id = c.id
        WHERE c.id = ?
    """, (categoria_id,))
    productos = cursor.fetchall()
    conn.close()
    return render_template("productos.html", productos=productos)


# ==============================
# 📌 Punto 4 — Carrito de compras en sesión
# ==============================
@app.route('/carrito')
def ver_carrito():
    carrito = session.get("carrito", [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    return render_template("carrito.html", carrito=carrito, total=total)

@app.route('/agregar_carrito/<int:producto_id>')
def agregar_carrito(producto_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio FROM Productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()
    conn.close()

    if not producto:
        flash("Producto no encontrado", "error")
        return redirect(url_for('index'))

    carrito = session.get("carrito", [])
    for item in carrito:
        if item["id"] == producto.id:
            item["cantidad"] += 1
            break
    else:
        carrito.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": 1
        })

    session["carrito"] = carrito
    flash("Producto agregado al carrito", "success")
    return redirect(url_for("ver_carrito"))


# ==============================
# 📌 Punto 5 — Registro de usuarios y autenticación
# ==============================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (nombre, email, password) VALUES (?, ?, ?)",
                       (nombre, email, password))
        conn.commit()
        conn.close()

        flash("Usuario registrado con éxito", "success")
        return redirect(url_for("login"))

    return render_template("registro.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM Usuarios WHERE email = ? AND password = ?", (email, password))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            flash(f"Bienvenido {usuario.nombre}", "success")
            return redirect(url_for("index"))
        else:
            flash("Credenciales incorrectas", "error")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("index"))


# ==============================
# 🚀 Arranque de la app
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
