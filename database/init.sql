CREATE TABLE productos (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

INSERT INTO productos (nombre, precio) VALUES 
('Arroz', 3.50),
('Azúcar', 4.20),
('Leche', 2.80);
