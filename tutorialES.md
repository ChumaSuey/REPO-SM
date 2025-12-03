# Tutorial R.E.P.O Save Manager (Español)

Bienvenido al **R.E.P.O Save Manager**. Esta herramienta te permite gestionar tus partidas guardadas del juego *R.E.P.O* de manera fácil y segura.

## Introducción
Este programa te ayuda a crear copias de seguridad (backups) de tus partidas, restaurarlas cuando quieras y organizar tus diferentes estados de juego. Es ideal si quieres probar cosas nuevas sin perder tu progreso actual.

## Instalación y Ejecución

### Si usas el Ejecutable (.exe)
1. **Descarga** el archivo `REPO-SM.exe` (o el nombre que tenga la versión final).
2. Colócalo en una carpeta de tu preferencia (por ejemplo, en el Escritorio o en una carpeta de Documentos).
3. **Ejecuta** el archivo haciendo doble clic.
   - *Nota*: No necesitas tener Python instalado para usar la versión ejecutable.
   - *Nota*: Si Windows te muestra una advertencia de seguridad, es normal en programas nuevos. Puedes darle a "Más información" y "Ejecutar de todas formas".

## Uso del Programa

La interfaz es muy sencilla y está dividida en dos paneles principales:

### 1. Panel Izquierdo (Steam/REPO Folder)
Aquí ves los archivos que están **actualmente en el juego**. Estos son los que el juego lee cuando lo inicias.

### 2. Panel Derecho (Local Backups)
Aquí se guardan tus **copias de seguridad**. Estos archivos están seguros y no se modifican por el juego.

### Botones y Funciones

- **Refresh Lists (Actualizar Listas)**:
  Si has jugado o movido archivos manualmente, pulsa este botón para recargar las listas y ver los cambios.

- **Backup (REPO -> Local)**:
  Guarda tu partida actual.
  1. Pulsa el botón.
  2. Escribe un nombre para tu backup (ej: "Antes del Boss", "Partida Nivel 5").
  3. Se creará una copia en el panel derecho.

- **Restore (Local -> REPO)**:
  Recupera una partida guardada.
  1. Selecciona un backup de la lista de la **derecha**.
  2. Pulsa "Restore".
  3. Confirma la acción.
  4. **¡Cuidado!** Esto sobrescribirá tu partida actual en el juego con la copia seleccionada.

- **Toggle State (Cambiar Estado)**:
  Sirve para "desactivar" o "activar" backups visualmente.
  - Si un backup tiene el sufijo `_backup`, el programa lo considera "desactivado" o simplemente guardado.
  - Puedes usar esto para organizar qué saves quieres tener más visibles, aunque funcionalmente es más para organización interna.

- **Change Local (Cambiar Carpeta Local)**:
  Por defecto, los backups se guardan en una carpeta junto al programa. Si prefieres guardarlos en otro sitio (ej: en un disco duro externo), usa este botón para elegir la nueva carpeta.

## Solución de Problemas

- **"REPO Folder Not Found"**:
  Asegúrate de que has instalado el juego y lo has abierto al menos una vez para que se cree la carpeta de guardado original.

- **Errores de Permisos**:
  Si el programa no puede copiar o leer archivos, prueba a ejecutarlo como **Administrador** (clic derecho -> Ejecutar como administrador).
