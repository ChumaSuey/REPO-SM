# Tutorial R.E.P.O Save Manager (Español)

Bienvenido al **R.E.P.O Save Manager**. Esta herramienta te permite gestionar tus partidas guardadas del juego *R.E.P.O* de manera fácil y segura.

## Introducción

Este programa te ayuda a crear copias de seguridad (backups) de tus partidas, restaurarlas cuando quieras y organizar tus diferentes estados de juego. Es ideal si quieres probar cosas nuevas sin perder tu progreso actual.

Funciona en Windows, macOS y Linux (incluyendo Steam Deck / Proton).

## Instalación y Ejecución

### Instalación desde el código fuente

1. **Clona o descarga** el repositorio a tu máquina.
2. **Instala las dependencias**:
   Abre una terminal en la carpeta del proyecto y ejecuta:

   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta** el programa:

   ```bash
   python main.py
   ```

### Si usas el Ejecutable (.exe)

1. **Descarga** el archivo `REPO-SM.exe` (o el nombre de la versión).
2. Colócalo en una carpeta de tu preferencia (por ejemplo, en el Escritorio).
3. **Ejecuta** el archivo haciendo doble clic.
   - *Nota*: No necesitas tener Python instalado para usar la versión ejecutable.
   - *Nota*: Si Windows te muestra una advertencia de seguridad, es normal. Puedes darle a "Más información" y "Ejecutar de todas formas".

## Uso del Programa

La interfaz está dividida en dos paneles principales:

### 1. Panel Izquierdo (Steam/REPO Folder)

Aquí ves los archivos que están **actualmente en el juego**. Estos son los que el juego lee cuando lo inicias.

### 2. Panel Derecho (Local Backups)

Aquí se guardan tus **copias de seguridad**. Estos archivos están seguros y no se modifican por el juego. Al entrar al modo Papelera de Reciclaje, el panel muestra los backups eliminados.

### Botones y Funciones

- **Refresh (Actualizar)**:
  Recarga las vistas de ambas carpetas para ver cambios recientes. También puedes usar la tecla `F5`.

- **Backup (Respaldo)**:
  Guarda tu partida actual.
  1. Pulsa el botón.
  2. Escribe un nombre para tu backup (ej: "Antes del Boss", "Partida Nivel 5").
  3. Se creará una copia en el panel derecho.

- **Restore (Restaurar)**:
  Recupera una partida guardada.
  1. Selecciona un backup de la lista de la **derecha**.
  2. Pulsa "Restore".
  3. Confirma la acción.
  4. **¡Cuidado!** Esto sobrescribirá tu partida actual en el juego con la copia seleccionada.
  5. **Restauración Segura**: Si algo falla durante la restauración, el programa recupera automáticamente tu partida original.
  *En modo Papelera, este botón restaura el backup eliminado de vuelta a la lista activa.*

- **Toggle (Alternar Estado)**:
  Añade o quita el sufijo configurable (por defecto `_backup`) para "activar" o "desactivar" backups visualmente. Sirve para organizar tus saves.

- **Rename (Renombrar)**:
  Cambia el nombre de un backup seleccionado sin salir del programa.

- **Delete (Eliminar)**:
  Mueve el backup seleccionado a la Papelera de Reciclaje interna. Puedes restaurarlo después. También puedes usar la tecla `Suprimir`.
  *En modo Papelera, este botón elimina permanentemente.*

- **🗑 Recycle Bin (Papelera)**:
  Alterna entre la vista normal de backups y la Papelera de Reciclaje. En modo Papelera, algunos botones se deshabilitan y las acciones cambian de comportamiento.

- **Open Saves (Abrir Saves)**:
  Abre la carpeta de saves del juego en el explorador de archivos.

- **Open Local (Abrir Local)**:
  Abre la carpeta de backups locales (o la Papelera) en el explorador de archivos.

- **⚙ Settings (Configuración)**:
  Abre un diálogo donde puedes cambiar el sufijo de los backups y la carpeta donde se guardan.

### Menú Contextual (Clic Derecho)

- **Sobre un backup normal**: Restaurar, Alternar Estado, Renombrar, Eliminar.
- **Sobre un backup en la Papelera**: Restaurar, Eliminar Permanentemente.
- **Sobre archivos del REPO**: Abrir en Explorador.

### Atajos de Teclado

| Tecla | Acción |
|---|---|
| `F5` | Actualizar listas |
| `Suprimir` | Eliminar backup seleccionado |

## Solución de Problemas

- **"REPO Folder Not Found"**:
  Asegúrate de que has instalado el juego y lo has abierto al menos una vez para que se cree la carpeta de guardado original.

- **Revisar Logs**:
  Si el programa da algún error, revisa el archivo `app.log` que se crea en la misma carpeta del programa. Allí se registra exactamente qué hace el sistema y qué errores han ocurrido.

- **Errores de Permisos**:
  Si el programa no puede copiar o leer archivos, prueba a ejecutarlo como **Administrador** (clic derecho -> Ejecutar como administrador).
