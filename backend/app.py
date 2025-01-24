from flask import Flask, jsonify, render_template
import dbf
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import ConfigParser


app = Flask(__name__)

# Read configuration from config.ini 
config = ConfigParser.ConfigParser()
config.read('config.ini')

app.config['DEBUG'] = config.getboolean('default', 'DEBUG')
app.config['RUTA_TABLA'] = config.get('default', 'RUTA_TABLA')



# Set up logging
log_directory = "logs" # Must exist
log_file = os.path.join(log_directory, "app.log")
handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=30)
handler.suffix = "%Y-%m-%d"
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


class DbfTable:
    """Creates a dbf.table object
    """

    def __init__(self, **kwargs):
        """ Creates a dbf.table object
            Args:
                dbf_file (str): Absolute or relative DBF file path (Required)
                codepage (str, optional): DBF file coding. Defaults to 'cp1252'.
        """
        self.dbf_file = kwargs['dbf_file']
        self.codepage = kwargs.get('codepage', 'cp1252')
        self.debug = kwargs.get('debug', False)
        self.table = None
        self.reccount = 0

        try:
            self.table = dbf.Table(self.dbf_file, codepage=self.codepage)
            self.reccount = len(self.table)
            app.logger.info("DBF file located: %s", app.config['RUTA_TABLA'])
        except Exception as e:
            app.logger.error("ERROR: Could not locate DBF file %s: %s", app.config['RUTA_TABLA'], e)
       
    def open(self):
        """Open dbf_file
        """
        try:
            self.table.open(dbf.READ_WRITE)
            app.logger.info("DBF file opened successfully: %s", app.config['RUTA_TABLA'])
        except Exception as e:
            app.logger.error("ERROR: Could not open DBF file %s: %s", app.config['RUTA_TABLA'], e)
    
    def close(self):
        """Close dbf_file
        """
        try:
            self.table.close()
            app.logger.info("DBF file closed successfully: %s", app.config['RUTA_TABLA'])
        except Exception as e:
            app.logger.error("ERROR: Could not close DBF file %s: %s", app.config['RUTA_TABLA'], e)









tabla = DbfTable(dbf_file=app.config['RUTA_TABLA'])
precios = []

@app.route("/")
def index():
    return render_template('index.html', archivo=tabla.dbf_file, registros=tabla.reccount, precios=precios)

@app.route('/buscar/<codigo>', methods=['GET'])
def buscar(codigo):
    """Search code in DBF
    Args:
        codigo (str): 

    Returns:
        json : Product fields
    """

    respuesta = {'status': 'Not found'}
    try:
        tabla.open()
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

    tabla.close()
    return jsonify(respuesta)

@app.route('/cambiar/<int:n_registro>/<float:precio>', methods=['PUT'])
def cambiar(n_registro, precio):
    """Update price

    Args:
        n_registro (str): Record number 
        precio (float): new price

    Returns:
        json : status
    """


    global precios
    try:
        tabla.open()
        record = tabla[int(n_registro)]
        precio_anterior = float(record.P_VENTA)
        with record:
            record.P_VENTA = float(precio)
            precios.append([n_registro, record.NUMERO, record.DESCRI, precio_anterior, record.P_VENTA])

        app.logger.info(
            "Updated record %d: NUMERO=%s, DESCRI=%s, Precio Anterior=%.2f, Precio Nuevo=%.2f",
            record._recnum, record.NUMERO, record.DESCRI, precio_anterior, record.P_VENTA
        )
        tabla.close()

        return jsonify({'status': 'success', 'precio': record.P_VENTA}), 200
    except Exception as e:
        app.logger.error("ERROR during update: %s", e)
        tabla.close()

        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
