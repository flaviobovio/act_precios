from flask import Flask, jsonify, request, render_template
import dbf
import pandas as pd

app = Flask(__name__)


ruta_tabla = 'PRUEBA.DBF'

try:
    tabla = dbf.Table(ruta_tabla, codepage='cp1252')
    tabla.open()
except:
    print "ERROR, no se pudo abrir el archivo ", ruta_tabla

regs = [[reg._recnum, reg.NUMERO, reg.DESCRI, reg.P_VENTA] for reg in tabla]

df = pd.DataFrame(regs)
df.columns = ['registro', 'numero', 'descri', 'p_venta']


@app.route("/")
def index():
    return render_template('index.html', archivo=ruta_tabla, registros=len(tabla), precios=df[0:20].values.tolist())



@app.route('/buscar/<codigo>', methods=['GET'])
def buscar(codigo):

    producto = df[df['numero']==codigo]
    respuesta = {}
    if len(producto)>0:
        respuesta = {
            'registro' : producto['registro'].values[0],
            'numero'   : producto['numero'].values[0],
            'descri'   : producto['descri'].values[0],
            'precio'   : producto['p_venta'].values[0]
        }
    return jsonify(respuesta)


@app.route('/cambiar/<codigo>/<precio>', methods=['PUT'])
def cambiar(codigo, precio):
    #'registro' : record._recnum   
    pass 



if __name__ == '__main__':
    app.run(debug=True)