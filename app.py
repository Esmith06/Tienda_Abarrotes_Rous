from flask import Flask, render_template, session, redirect, url_for, request
import pyodbc, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Conexión a SQL Server
conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('DB_SERVER')};DATABASE={os.getenv('DB_NAME')};UID={os.getenv('DB_USER')};PWD={os.getenv('DB_PASS')}"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# ---------- Rutas principales ----------

@app.route('/')
def index():
    cursor.execute("SELECT * FROM Categorias")
    categorias = cursor.fetchall()
    return render_template('index.html', categorias=categorias)

@app.route('/productos')
def productos():
    cursor.execute("""
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.ruta_imagen, c.nombre as categoria
        FROM Productos p
        JOIN Categorias c ON p.id_categoria = c.id
    """)
    productos = cursor.fetchall()
    return render_template('productos.html', productos=productos)

@app.route('/agregar_carrito/<int:id_producto>')
def agregar_carrito(id_producto):
    if 'carrito' not in session:
        session['carrito'] = {}
    carrito = session['carrito']
    carrito[id_producto] = carrito.get(id_producto, 0) + 1
    session['carrito'] = carrito
    return redirect(url_for('productos'))

@app.route('/carrito')
def carrito():
    carrito = session.get('carrito', {})
    productos_detalle = []
    for pid, cantidad in carrito.items():
        cursor.execute("SELECT nombre, precio FROM Productos WHERE id=?", pid)
        prod = cursor.fetchone()
        if prod:
            productos_detalle.append({
                'id': pid,
                'nombre': prod.nombre,
                'precio': prod.precio,
                'cantidad': cantidad,
                'subtotal': prod.precio * cantidad
            })
    total = sum(item['subtotal'] for item in productos_detalle)
    return render_template('carrito.html', productos=productos_detalle, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    usuario_id = 1  # Usuario de prueba, en real sería el login
    carrito = session.get('carrito', {})
    if not carrito:
        return redirect(url_for('productos'))
    total = 0
    for pid, cantidad in carrito.items():
        cursor.execute("SELECT precio FROM Productos WHERE id=?", pid)
        precio = cursor.fetchone()[0]
        total += precio * cantidad
    cursor.execute("INSERT INTO Ventas (id_usuario, total) VALUES (?, ?)", usuario_id, total)
    venta_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchval()
    for pid, cantidad in carrito.items():
        cursor.execute("SELECT precio FROM Productos WHERE id=?", pid)
        precio = cursor.fetchone()[0]
        subtotal = precio * cantidad
        cursor.execute("INSERT INTO DetallesVenta (id_venta, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                       venta_id, pid, cantidad, subtotal)
        cursor.execute("UPDATE Productos SET stock = stock - ? WHERE id=?", cantidad, pid)
    conn.commit()
    session['carrito'] = {}
    return redirect(url_for('productos'))

if __name__ == '__main__':
    app.run(debug=True)
