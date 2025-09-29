
# Tienda_Abarrotes_Rous
github page 

# 🛒 Tienda de Abarrotes

Proyecto base de una aplicación web para la venta de abarrotes, desarrollada con **Python (Flask)** y **SQL Server**.

---

## 🚀 Características

- Backend con **Flask** (Python).
- Conexión a **SQL Server** usando `pyodbc`.
- Frontend con **HTML + CSS** (plantillas Jinja2).
- Arquitectura lista para desplegar en la nube.
- Variables de entorno para credenciales seguras.

---

## 📂 Estructura del proyecto

```
tienda-abarrotes/
│── app.py                # Aplicación principal Flask
│── requirements.txt      # Dependencias
│── .env.example          # Ejemplo de configuración (variables de entorno)
│── README.md             # Documentación
│
├── static/               # Archivos estáticos (CSS, imágenes, JS)
│   └── style.css
│
├── templates/            # Vistas HTML (Jinja2)
│   ├── base.html
│   ├── index.html
│   └── productos.html
│
├── database/             # Scripts SQL
│   └── init.sql
└── .gitignore            # Archivos a excluir de GitHub
```

---

## ⚙️ Instalación y uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU-USUARIO/tienda-abarrotes.git
cd tienda-abarrotes
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Copia `.env.example` y renómbralo como `.env`:

```
DB_SERVER=localhost
DB_NAME=tienda
DB_USER=sa
DB_PASS=tu_password
```

### 5. Inicializar base de datos
Ejecuta el script en tu SQL Server:

```sql
database/init.sql
```

### 6. Ejecutar la aplicación
```bash
python app.py
```

La aplicación correrá en:  
👉 http://127.0.0.1:5000

---

## 📸 Vistas disponibles

- **Inicio** → `/`
- **Productos** → `/productos`

---

## 🔒 Seguridad

- Nunca subas tu archivo `.env` real a GitHub.
- Usa `.gitignore` para excluir credenciales y entornos locales.
- Recomendado: usar **SQL Server con usuario de solo lectura** para la aplicación en producción.

---

## ☁️ Despliegue en la nube

Este proyecto puede desplegarse en:
- **Render**, **Railway** o **Fly.io** (apps Flask).
- **AWS / Azure** (si quieres usar SQL Server en la nube).
- **Docker** (si deseas contenerizar el proyecto).

---

## 👨‍💻 Autor

- **Yorgen Fernandez Malca**  
- Ingeniero de Sistemas / Redes y Telecomunicaciones  
- Proyecto de ejemplo: Tienda de Abarrotes con Flask + SQL Server
>>>>>>> 6316c79 (version inicial del proyecto tienda-abarrotes-Rosa)
