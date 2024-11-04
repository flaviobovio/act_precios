from flask import Flask, jsonify, request, render_template
import dbf
import pandas as pd

app = Flask(__name__)

ruta_tabla = 'PRUEBA.DBF'
debug = True

try:
    tabla = dbf.Table(ruta_tabla, codepage='cp1252')
    tabla.open(dbf.READ_WRITE)
except Exception as e:
    print "ERROR, no se pudo abrir el archivo ", ruta_tabla, ":", e

# regs = [[reg._recnum, reg.NUMERO, reg.DESCRI, reg.P_VENTA] for reg in tabla]
# df = pd.DataFrame(regs)
# df.columns = ['registro', 'numero', 'descri', 'p_venta']

precios = []

@app.route("/")
def index():
    return render_template('index.html', archivo=ruta_tabla, registros=len(tabla), precios=precios)

@app.route('/buscar/<codigo>', methods=['GET'])
def buscar(codigo):
    respuesta = {'status' : 'Not found'}
    with tabla: 
        for record in tabla:
            if record.NUMERO == codigo:
                respuesta = {'registro' : record._recnum,
                            'codigo' : record.NUMERO,
                            'descripcion' : record.DESCRI,
                            'precio' : record.P_VENTA
                            }
                break

    return jsonify(respuesta)

@app.route('/cambiar/<int:n_registro>/<float:precio>', methods=['PUT'])
def cambiar(n_registro, precio):
    global precios
    try:
        record = tabla[int(n_registro)]

        if debug:
            print '<== Registro nro: ', record._recnum, ' ==>'
            print 'NUMERO:', record.NUMERO, 'DESCRI:', record.DESCRI
            print 'Precio Anterior:', record.P_VENTA

        with record:
            precio_anterior = float(record.P_VENTA)
            record.P_VENTA = float(precio)
            precios.append([n_registro, record.NUMERO, record.DESCRI, precio_anterior, record.P_VENTA])

        if debug:
            print 'Precio Actualizado:', record.P_VENTA

        return jsonify({'status': 'success', 'precio': record.P_VENTA})

    except Exception as e:
        print "ERROR:", e
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
