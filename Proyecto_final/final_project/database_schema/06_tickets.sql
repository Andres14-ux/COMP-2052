-- Eliminar la base de datos si ya existe
DROP DATABASE IF EXISTS seguimiento_tickets;

-- Crear una nueva base de datos con codificación UTF-8
CREATE DATABASE seguimiento_tickets CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Seleccionar la base de datos recién creada
USE seguimiento_tickets;

-- Crear tabla de roles
CREATE TABLE role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) UNIQUE
);

-- Crear tabla de usuarios
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(256),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

-- Crear tabla de tickets
CREATE TABLE ticket (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asunto VARCHAR(150),
    descripcion TEXT,
    prioridad ENUM('Baja', 'Media', 'Alta') NOT NULL,
    estado ENUM('Abierto', 'En proceso', 'Cerrado') NOT NULL DEFAULT 'Abierto',
    usuario_id INT NOT NULL,
    tecnico_id INT NULL,  -- ✅ Permite NULL para poder crear tickets sin técnico asignado
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,  -- ✅ Se asigna fecha automáticamente
    FOREIGN KEY (usuario_id) REFERENCES user(id),
    FOREIGN KEY (tecnico_id) REFERENCES user(id)
);

-- Insertar roles por defecto
INSERT INTO role (name) VALUES ('Admin'), ('Usuario'), ('Técnico');
