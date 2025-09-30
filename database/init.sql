-- ========================================
-- Script de Base de Datos - Tienda Abarrotes
-- Autor: Yorgen Fernandez Malca
-- ========================================

-- Crear base de datos (si no existe)
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'TiendaAbarrotes')
BEGIN
    CREATE DATABASE TiendaAbarrotes;
END;
GO

USE TiendaAbarrotes;
GO

-- ================================
-- Tabla de Productos
-- ================================
IF OBJECT_ID('Productos', 'U') IS NOT NULL DROP TABLE Productos;
GO

CREATE TABLE Productos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(255),
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    categoria NVARCHAR(50),
    creado_en DATETIME DEFAULT GETDATE()
);
GO

-- ================================
-- Tabla de Ventas
-- ================================
IF OBJECT_ID('Ventas', 'U') IS NOT NULL DROP TABLE Ventas;
GO

CREATE TABLE Ventas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    fecha DATETIME DEFAULT GETDATE(),
    cliente_nombre NVARCHAR(100),
    cliente_direccion NVARCHAR(200),
    cliente_telefono NVARCHAR(20),
    total DECIMAL(10,2) NOT NULL
);
GO

-- ================================
-- Tabla de DetalleVentas
-- ================================
IF OBJECT_ID('DetalleVentas', 'U') IS NOT NULL DROP TABLE DetalleVentas;
GO

CREATE TABLE DetalleVentas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal AS (cantidad * precio_unitario) PERSISTED,

    CONSTRAINT FK_DetalleVentas_Ventas FOREIGN KEY (id_venta) REFERENCES Ventas(id),
    CONSTRAINT FK_DetalleVentas_Productos FOREIGN KEY (id_producto) REFERENCES Productos(id)
);
GO

-- ================================
-- Datos iniciales
-- ================================
INSERT INTO Productos (nombre, descripcion, precio, stock, categoria)
VALUES
('Arroz Costeño 5kg', 'Arroz de primera calidad', 22.50, 50, 'Granos'),
('Aceite Primor 1L', 'Aceite vegetal', 9.80, 30, 'Aceites'),
('Leche Gloria 400g', 'Leche evaporada entera', 4.20, 100, 'Lácteos'),
('Azúcar Rubia 1kg', 'Azúcar de caña rubia', 3.50, 80, 'Endulzantes'),
('Fideos Don Vittorio 500g', 'Fideos de trigo', 4.00, 60, 'Pastas');
GO
