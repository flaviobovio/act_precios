from flask import Flask, jsonify, request, render_template
import dbf
import pandas as pd
import logging
from logging.handlers import TimedRotatingFileHandler
import os

app = Flask(__name__)

# Set up logging
log_directory = "logs" # Must exists
log_file = os.path.join(log_directory, "app.log")
handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7)
handler.suffix = "%Y-%m-%d"
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# DBF Table setup
ruta_tabla = 'PRUEBA.DBF'
debug = True

try:
    tabla = dbf.Table(ruta_tabla, codepage='cp1252')
    tabla.open(dbf.READ_WRITE)
    app.logger.info("DBF file opened successfully: %s", ruta_tabla)
except Exception as e:
    app.logger.error("ERROR: Could not open DBF file %s: %s", ruta_tabla, e)

precios = []

@app.route("/")
def index():
    return render_template('index.html', archivo=ruta_tabla, registros=len(tabla), precios=precios)

@app.route('/buscar/<codigo>', methods=['GET'])
def buscar(codigo):
    respuesta = {'status': 'Not found'}
    try:
        with tabla:
            for record in tabla:
                if record.NUMERO == codigo:
                    respuesta = {
                        'registro': record._recnum,
                        'codigo': record.NUMERO,
                        'descripcion': record.DESCRI,
                        'precio': record.P_VENTA
                    }
                    break
        app.logger.info("Search completed for codigo: %s, result: %s", codigo, respuesta)
    except Exception as e:
        app.logger.error("ERROR during search: %s", e)
        respuesta = {'status': 'error', 'message': str(e)}

    return jsonify(respuesta)

@app.route('/cambiar/<int:n_registro>/<float:precio>', methods=['PUT'])
def cambiar(n_registro, precio):
    global precios
    try:
        record = tabla[int(n_registro)]
        precio_anterior = float(record.P_VENTA)
        with record:
            record.P_VENTA = float(precio)
            precios.append([n_registro, record.NUMERO, record.DESCRI, precio_anterior, record.P_VENTA])

        app.logger.info(
            "Updated record %d: NUMERO=%s, DESCRI=%s, Precio Anterior=%.2f, Precio Nuevo=%.2f",
            record._recnum, record.NUMERO, record.DESCRI, precio_anterior, record.P_VENTA
        )

        return jsonify({'status': 'success', 'precio': record.P_VENTA})
    except Exception as e:
        app.logger.error("ERROR during update: %s", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
