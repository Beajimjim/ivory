import sys
import io
import json
import re
import random
from collections import Counter
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

# Importamos la función principal de ivory.py
from ivory import main as run_block_scripts

app = Flask(__name__, static_url_path='/flask')
socketio = SocketIO(app)  # Habilitamos WebSockets

# 📌 Ruta del archivo .htaccess
HTACCESS_FILE = "/var/www/html/.htaccess"

# 📌 Ruta del log de Apache
ACCESS_LOG_FILE = "/var/log/apache2/access.log"

# 📌 Función para leer las IPs bloqueadas desde `.htaccess`
def read_blocked_ips():
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')  # Expresión regular para detectar IPs
    blocked_ips = []

    try:
        with open(HTACCESS_FILE, "r") as file:
            for line in file:
                if "Deny from" in line:  # Buscar líneas con "Deny from"
                    match = ip_pattern.findall(line)
                    if match:
                        blocked_ips.extend(match)  # Agregar las IPs encontradas
    except FileNotFoundError:
        return []

    return list(set(blocked_ips))  # Elimina duplicados y devuelve las IPs bloqueadas

# 📌 Función para obtener IPs reales desde los logs de Apache y contar repeticiones
def get_real_ips_from_logs():
    """Leer IPs reales desde el archivo de logs de Apache y contar repeticiones"""
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')  # Detectar IPs reales
    ip_counts = Counter()  # Contador para almacenar las repeticiones

    try:
        with open(ACCESS_LOG_FILE, "r") as file:
            for line in file:
                match = ip_pattern.search(line)  # Buscar la IP en cada línea
                if match:
                    ip_counts[match.group()] += 1  # Contar cada aparición
    except FileNotFoundError:
        return {}

    return dict(ip_counts)  # Devolver diccionario con IPs y sus repeticiones

# 📌 Bloquear una nueva IP real desde `access.log` y agregarla a `.htaccess`
@app.route("/flask/run")
def run_script():
    # Capturar salida de la ejecución
    backup_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        run_block_scripts()  # Ejecutamos la función principal
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = backup_stdout

    # 📌 Leer IPs bloqueadas actuales
    blocked_ips = read_blocked_ips()

    # 📌 Obtener IPs reales desde los logs con sus conteos
    real_ips_counts = get_real_ips_from_logs()

    if not real_ips_counts:
        return render_template("results.html", output=f"{output}\n⚠️ No hay IPs reales en los logs.")

    # 📌 Escoger la IP con más intentos (más conexiones)
    new_ip = max(real_ips_counts, key=real_ips_counts.get)

    # 📌 Si la IP ya está bloqueada, no la agregamos otra vez
    if new_ip not in blocked_ips:
        with open(HTACCESS_FILE, "a") as file:
            file.write(f"\nDeny from {new_ip}")

        # 📢 Enviar notificación en tiempo real al Dashboard
        socketio.emit("new_blocked_ip", {"ip": new_ip, "count": real_ips_counts[new_ip]})

        return render_template("results.html", output=f"{output}\nNueva IP real bloqueada: {new_ip} (Intentos: {real_ips_counts[new_ip]})")
    else:
        return render_template("results.html", output=f"{output}\n⚠️ IP {new_ip} ya estaba bloqueada.")

# 📊 Obtener estadísticas de bloqueos desde `.htaccess`
@app.route("/flask/stats")
def get_statistics():
    blocked_ips = read_blocked_ips()  # Obtener IPs bloqueadas de .htaccess
    real_ips_counts = get_real_ips_from_logs()  # Obtener conteo real de IPs

    # Filtrar solo las IPs que están bloqueadas y contar cuántas veces aparecen en los logs
    blocked_ips_counts = {ip: real_ips_counts.get(ip, 0) for ip in blocked_ips}

    if not blocked_ips_counts:
        return jsonify({})  # Si no hay datos, devolver JSON vacío

    return jsonify(blocked_ips_counts)

# 📊 Dashboard con gráficos
@app.route("/flask/dashboard")
def dashboard():
    return render_template("dashboard.html")

# 📌 Página de inicio
@app.route("/flask/")
def index():
    return render_template("index.html")

# 📌 Ejecutar la app con WebSockets
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
