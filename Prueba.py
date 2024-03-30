import mysql.connector
from datetime import datetime

# Establecer la conexión con la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ServidorRasa"
)

# Crear un cursor para ejecutar consultas SQL
cursor = conexion.cursor()

# Datos a insertar en la tabla
nombre_operacion = "Operación 1"
fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
estado = "EXITO"

# Consulta SQL para insertar datos
sql = "INSERT INTO Operaciones (nombre_operacion, fecha_hora, estado) VALUES (%s, %s, %s)"
valores = (nombre_operacion, fecha_hora, estado)

# Ejecutar la consulta
cursor.execute(sql, valores)

# Confirmar la inserción de datos
conexion.commit()

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()

print("Datos insertados correctamente en la tabla Operaciones.")
