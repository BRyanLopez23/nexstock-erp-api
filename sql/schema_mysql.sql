-- =============================================================================
-- Script de Base de Datos Relacional (MySQL / MariaDB)
-- Proyecto: Sistema de Gestión de Inventario y Trazabilidad de Lotes
-- Autor: Bryan Francisco López León (github.com/BRyanLopez23)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS gestion_inventario_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE gestion_inventario_db;

-- 1. Tabla de Categorías
CREATE TABLE IF NOT EXISTS categorias_producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    descripcion TEXT,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Tabla de Lotes de Inventario
CREATE TABLE IF NOT EXISTS lotes_inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_lote VARCHAR(30) NOT NULL UNIQUE,
    nombre_producto VARCHAR(120) NOT NULL,
    categoria_id INT NOT NULL,
    cantidad_kg DECIMAL(10, 2) NOT NULL CHECK (cantidad_kg >= 0),
    stock_minimo_kg DECIMAL(10, 2) NOT NULL DEFAULT 50.00,
    costo_unitario_usd DECIMAL(10, 2) NOT NULL CHECK (costo_unitario_usd >= 0),
    estado ENUM('DISPONIBLE', 'EN_PROCESO', 'DESPACHADO') NOT NULL DEFAULT 'DISPONIBLE',
    ubicacion_bodega VARCHAR(60) NOT NULL DEFAULT 'Cámara Frigorífica A1',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_lote_categoria
        FOREIGN KEY (categoria_id) REFERENCES categorias_producto(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_estado_lote (estado),
    INDEX idx_codigo_producto (codigo_lote, nombre_producto)
) ENGINE=InnoDB;

-- =============================================================================
-- CONSULTAS SQL DE ANÁLISIS Y REPORTES (Preparación para Prueba Técnica)
-- =============================================================================

-- Consulta 1: Reporte consolidado por categoría con JOIN, GROUP BY y agregaciones
SELECT
    c.nombre AS categoria,
    COUNT(l.id) AS total_lotes,
    ROUND(SUM(l.cantidad_kg), 2) AS volumen_total_kg,
    ROUND(SUM(l.cantidad_kg * l.costo_unitario_usd), 2) AS valor_total_usd
FROM categorias_producto c
LEFT JOIN lotes_inventario l ON l.categoria_id = c.id
GROUP BY c.id, c.nombre
ORDER BY valor_total_usd DESC;

-- Consulta 2: Detección de lotes con alerta crítica de stock mínimo
SELECT
    l.codigo_lote,
    l.nombre_producto,
    c.nombre AS categoria,
    l.cantidad_kg,
    l.stock_minimo_kg,
    (l.stock_minimo_kg - l.cantidad_kg) AS deficit_kg,
    l.ubicacion_bodega
FROM lotes_inventario l
INNER JOIN categorias_producto c ON c.id = l.categoria_id
WHERE l.cantidad_kg <= l.stock_minimo_kg
  AND l.estado != 'DESPACHADO'
ORDER BY deficit_kg DESC;
