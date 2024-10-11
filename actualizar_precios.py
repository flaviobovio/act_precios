def buscar_precio (codigo, path_tabla='ARTICU.DBF', debug=False):

	import dbf
	try:
		tabla = dbf.Table(path_tabla)
		tabla.open()
	except:
		print "ERROR, no se pudo abrir el archivo ", path_tabla


	retorno = None
	with tabla: 
		for record in tabla:

			if record.NUMERO == codigo:

				retorno = {'registro' : record._recnum, 'codigo' : record.NUMERO, 'descripcion' : record.DESCRI, 'precio' : record.P_VENTA,}

				break

	tabla.close()

	if debug:
		print 
		print '<== Buscar Codigo: ', codigo, ' ==>'
		print retorno



	return retorno






def actualizar_precio (n_registro, p_actualizado, path_tabla='ARTICU.DBF', debug=False):

	import dbf
	try:
		tabla = dbf.Table(path_tabla)
		tabla.open(dbf.READ_WRITE)
		registro = tabla[n_registro]

		if debug:
			print '<== Registro nro: ', registro._recnum, ' ==>'
			print tabla[n_registro].NUMERO, tabla[n_registro].DESCRI
			print 'Precio Anterior', tabla[n_registro].P_VENTA


		with registro:
			registro.P_VENTA = p_actualizado


		if debug:
			print 'Precio Actualizado', tabla[n_registro].P_VENTA
			print

		tabla.close()

	except:
		print "ERROR, no se pudo abrir el archivo ", path_tabla






 





if __name__ == "__main__":

	
	# La tabla "PRUEBA.DBF" debe estar en la carpeta donde se ejecutan las pruebas
	print "* === TESTING DE FUNCIONES DE ACTUALIZACION DE PRECIOS === *"

	print
	print "* ACTUALIZACION"
	print
	import dbf, random
	# almacena los codigos para despues probar la busqueda
	codigos = []	

	for i in range(5):
		try:
			tabla = dbf.Table("PRUEBA.DBF")
		except:
			print "ERROR, no se pudo abrir el archivo PRUEBA.DBF"
			exit()
		tabla.open(dbf.READ_WRITE)
		p_actualizado = float (random.randrange(1, 1000000)) / 100
		n_registro = random.randrange(0, tabla.last_record._recnum)

		codigos.append(tabla[n_registro].NUMERO)

		tabla.close()
		actualizar_precio(n_registro, p_actualizado, 'PRUEBA.DBF', debug=True)




	print
	print "* BUSQUEDA"
	print
	print codigos
	for cod in codigos:
		buscar_precio(cod, 'PRUEBA.DBF', debug=True)
