import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc

# ============================
# CONFIGURACIÓN DE LA APP
# ============================
app = Flask(__name__)
app.secret_key = "clave_secreta_cambiar"  # Cambia esto por una clave segura

# ============================
# CONEXIÓN SQL SERVER
# ============================
def get_db_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"  # Cambia por tu servidor SQL
        "DATABASE=TiendaAbarrotes;"
        "UID=sa;"            # Usuario SQL Server
        "PWD=tu_password;"   # Contraseña
    )
    return conn


# ============================
# RUTAS
# ============================

@app.route("/")
def index():
    """Página principal con categorías"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion FROM Categorias WHERE estado = 1;")
    categorias = cursor.fetchall()
    conn.close()
    return render_template("index.html", categorias=categorias)


@app.route("/productos/<int:id_categoria>")
def productos(id_categoria):
    """Lista de productos por categoría"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM Categorias WHERE id = ?", (id_categoria,))
    categoria = cursor.fetchone()

    cursor.execute("""
        SELECT id, nombre, descripcion, precio, stock, ruta_imagen 
        FROM Productos WHERE id_categoria = ? AND estado = 1;
    """, (id_categoria,))
    productos = cursor.fetchall()
    conn.close()
    return render_template("productos.html", productos=productos, categoria=categoria)


@app.route("/carrito")
def carrito():
    """Carrito de compras (datos en sesión)"""
    if "carrito" not in session:
        session["carrito"] = []
    return render_template("carrito.html", carrito=session["carrito"])


@app.route("/agregar_carrito/<int:id_producto>")
def agregar_carrito(id_producto):
    """Agregar producto al carrito"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio FROM Productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    conn.close()

    if not producto:
        flash("Producto no encontrado", "error")
        return redirect(url_for("index"))

    if "carrito" not in session:
        session["carrito"] = []

    session["carrito"].append({
        "id": producto[0],
        "nombre": producto[1],
        "precio": float(producto[2]),
        "cantidad": 1
    })
    session.modified = True
    flash(f"{producto[1]} agregado al carrito", "success")
    return redirect(request.referrer or url_for("index"))


@app.route("/vaciar_carrito")
def vaciar_carrito():
    """Vaciar carrito"""
    session.pop("carrito", None)
    flash("Carrito vaciado", "info")
    return redirect(url_for("carrito"))


# ============================
# INICIO
# ============================
if __name__ == "__main__":
    app.run(debug=True)

