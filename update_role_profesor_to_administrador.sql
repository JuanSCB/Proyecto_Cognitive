-- Script para renombrar el rol profesor a administrador en la tabla usuarios.
-- No elimina usuarios; solo actualiza el valor del campo rol.

UPDATE usuarios
SET rol = 'administrador'
WHERE rol = 'profesor';
