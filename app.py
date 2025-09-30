import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc

# ============================
# CONFIGURACIÓN DE LA APP
# ============================
app = Flask(__name__)
app.secret_key = "clave_secreta_cambiar"  # 🔑 cambia esto por una clave segura

# ============================
# CONEXIÓN SQL SERVER
# ============================
def get_db_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"   # Cambia por tu servidor SQL
        "DATABASE=TiendaAbarrotes;"
        "UID=sa;"             # Usuario SQL Server
        "PWD=tu_password;"    # Contraseña
    )
    return conn


# ============================
# RUTAS PRINCIPALES
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
# ADMIN - CATEGORÍAS
# ============================

@app.route("/admin/categorias")
def admin_categorias():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion, estado FROM Categorias;")
    categorias = cursor.fetchall()
    conn.close()
    return render_template("admin_categorias.html", categorias=categorias)


@app.route("/admin/categorias/agregar", methods=["POST"])
def agregar_categoria():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Categorias (nombre, descripcion) VALUES (?, ?)", (nombre, descripcion))
    conn.commit()
    conn.close()

    flash("Categoría agregada con éxito", "success")
    return redirect(url_for("admin_categorias"))


@app.route("/admin/categorias/eliminar/<int:id>")
def eliminar_categoria(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Categorias WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash("Categoría eliminada", "info")
    return redirect(url_for("admin_categorias"))


# ============================
# ADMIN - PRODUCTOS
# ============================

@app.route("/admin/productos")
def admin_productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT P.id, P.nombre, P.descripcion, P.precio, P.stock, C.nombre as categoria 
        FROM Productos P
        INNER JOIN Categorias C ON P.id_categoria = C.id
    """)
    productos = cursor.fetchall()

    cursor.execute("SELECT id, nombre FROM Categorias")
    categorias = cursor.fetchall()
    conn.close()

    return render_template("admin_productos.html", productos=productos, categorias=categorias)


@app.route("/admin/productos/agregar", methods=["POST"])
def agregar_producto():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]
    id_categoria = request.form["id_categoria"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Productos (nombre, descripcion, precio, stock, id_categoria)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, precio, stock, id_categoria))
    conn.commit()
    conn.close()

    flash("Producto agregado con éxito", "success")
    return redirect(url_for("admin_productos"))


@app.route("/admin/productos/eliminar/<int:id>")
def eliminar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Productos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash("Producto eliminado", "info")
    return redirect(url_for("admin_productos"))


# ============================
# INICIO
# ============================
if __name__ == "__main__":
    app.run(debug=True)
