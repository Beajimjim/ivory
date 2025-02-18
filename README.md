Bloqueo Automático de IPs con Flask y Apache

Este proyecto implementa un sistema de bloqueo automático de IPs en un servidor Apache basado en patrones de acceso sospechosos. Utiliza Flask para la interfaz web, WebSockets para actualizaciones en tiempo real y archivos de logs de Apache para detectar IPs sospechosas.

Tecnologías Utilizadas

- Python (Flask, Flask-SocketIO): Para la API y la comunicación en tiempo real.
- Apache: Servidor web donde se aplican las reglas de bloqueo.
- Regular Expressions (re): Para detectar y extraer IPs de los logs.
- JavaScript (Chart.js, Socket.io): Para el Dashboard en tiempo real.
- HTML y CSS (Bootstrap): Para la interfaz web.

Estructura del Proyecto

app.py                - Servidor Flask principal
templates/
    index.html        - Página principal
    dashboard.html    - Panel de control con gráficos en tiempo real
    results.html      - Página de resultados del script de bloqueo
static/
    styles.css        - Estilos CSS
    script.js         - Script de actualización en tiempo real
ivory.py              - Script de bloqueo importado
client_config.json    - Configuración del cliente
server_config.json    - Configuración del servidor
.htaccess             - Archivo donde se bloquean las IPs
access.log            - Logs de acceso de Apache

Instalación y Configuración

1. Clonar el repositorio

git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

2. Instalar dependencias

pip install flask flask-socketio

3. Configurar el servidor

- Asegúrate de que Apache está instalado y configurado.
- Revisa que .htaccess esté habilitado en Apache.

Uso del Proyecto

1. Iniciar el Servidor Flask

python app.py

2. Acceder a la Interfaz Web

- Página Principal: http://localhost:5000/flask/
- Dashboard en Tiempo Real: http://localhost:5000/flask/dashboard

3. Ejecutar el Bloqueo de IPs Manualmente

Puedes ejecutar el bloqueo manualmente accediendo a:

http://localhost:5000/flask/run

Dashboard en Tiempo Real

- Muestra un gráfico con las IPs bloqueadas y el número de intentos.
- Se actualiza en tiempo real con WebSockets.
- Muestra la última IP bloqueada en una lista.

Posibles Errores y Soluciones

- Error de conexión: Verifica que el servidor Flask está en ejecución y Apache está corriendo.
- No bloquea IPs: Asegúrate de que el archivo .htaccess tiene permisos de escritura.
- No se muestran gráficos: Verifica que la API /flask/stats devuelve datos correctamente.

Licencia

Este proyecto está bajo la licencia MIT.

Si necesitas más detalles o ajustes, dime.


