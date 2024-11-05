import dbf

tabla = dbf.Table('/home/ozzy/Dropbox/dos/ges/dbf/ARTICU.DBF', codepage='cp1252')
tabla.open(dbf.READ_WRITE)

record = tabla[11]
print record.P_VENTA
dbf.write(record, P_VENTA=37.0)
print record.P_VENTA
tabla.close()

