-- Script para insertar usuarios de prueba
-- Contraseñas: administrador123 y alumno123

INSERT INTO `usuarios` (`nombre`, `correo`, `contraseña_hash`, `rol`, `activo`, `creado_en`) VALUES
-- Administrador (contraseña: administrador123)
('Juan Pérez', 'administrador@ejemplo.com', 'scrypt:32768:8:1$qwerty1234abcdef$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0', 'administrador', 1, CURRENT_TIMESTAMP),
-- Alumno (contraseña: alumno123)  
('María García', 'alumno@ejemplo.com', 'scrypt:32768:8:1$qwerty5678abcdef$b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0p1', 'alumno', 1, CURRENT_TIMESTAMP),
-- Otro administrador (contraseña: administrador123)
('Carlos López', 'administrador2@ejemplo.com', 'scrypt:32768:8:1$qwerty1234abcdef$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0', 'administrador', 1, CURRENT_TIMESTAMP),
-- Otro alumno (contraseña: alumno123)
('Ana Rodríguez', 'alumno2@ejemplo.com', 'scrypt:32768:8:1$qwerty5678abcdef$b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0p1', 'alumno', 1, CURRENT_TIMESTAMP);
