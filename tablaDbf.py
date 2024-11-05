import dbf

class TablaDbf():

	def __init__(self, **kwargs):
		self.archivo = kwargs['archivo']
		self.codepage = kwargs.get('codepage', 'cp1252')
		self.debug = kwargs.get('debug', False) 		
		self.tabla = None
		try:
			self.tabla = dbf.Table(self.archivo, codepage=self.codepage)
			self.tabla.open(dbf.READ_WRITE)
		except Exception as e:
			self.tabla = None
			print "ERROR, no se pudo abrir el archivo ", self.archivo, ":", e


	def buscar(codigo):
		with self.tabla: 
			for record in tabla:
				if record.NUMERO == codigo:
					respuesta = {'registro' : record._recnum,
								'codigo' : record.NUMERO,
								'descripcion' : record.DESCRI,
								'precio' : record.P_VENTA
								}
					break
