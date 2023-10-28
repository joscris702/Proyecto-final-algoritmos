CREATE DATABASE base_de_datos;

use base_de_datos;
CREATE TABLE articulos (
    codigo VARCHAR(255) PRIMARY KEY,
    nombre VARCHAR(255),
    existencia INT,
    proveedor VARCHAR(255),
    precio DECIMAL(10, 2)
);
CREATE TABLE clientes (
    codigo_cliente VARCHAR(255) PRIMARY KEY,
    nombre_cliente VARCHAR(255),
    direccion_cliente VARCHAR(255)
);
CREATE TABLE ventas (
    codigo_venta VARCHAR(255) PRIMARY KEY,
    codigo_producto VARCHAR(255),
    codigo_cliente VARCHAR(255),
    cantidad INT,
    total DECIMAL(10, 2)
);
