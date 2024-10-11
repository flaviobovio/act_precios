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

records = [[record.NUMERO, record.DESCRI, record.P_VENTA] for record in tabla]

df = pd.DataFrame(records)
df.columns = ['numero', 'descri', 'p_venta']

print df.head()

@app.route("/")
def index():
    return render_template('index.html', archivo=ruta_tabla, registros=len(tabla), precios=df[0:20].values.tolist())



@app.route('/buscar_producto/<codigo>', methods=['GET'])
def buscar_producto(codigo):

    producto = df[df['numero']==codigo]
    respuesta = {
     'numero' : producto['numero'].values[0],
     'descri' : producto['descri'].values[0],
     'precio' : producto['p_venta'].values[0]
    }
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=True)