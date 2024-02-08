import mysql.connector
import sys

host = '127.0.0.1'
user = 'viajes_user'
password = 'viajes_pass'
database = 'viajes_db'
port = '3306'

configuracion_bd = {
    'host': host,
    'user': user,
    'password': password,
    'database': database,
    'port': port
}

# Datos de ejemplo
datos_hoteles = [
    ('Hotel Azul', 'Valencia', 'Valencia', 3, 'doble con vistas'),
    ('Hotel Blanco', 'Mojacar', 'Almeria', 4, 'doble'),
    ('Hotel Rojo', 'Sanlucar', 'Cádiz', 3, 'sencilla'),
]

datos_apartamentos = [
    ('Apartamentos Beach', 'Almeria', 'Almeria', 10, 4),
    ('Apartamentos Sol y playa', 'Málaga', 'Málaga', 50, 6),
]

def obtener_value_de_diccionario(dic, value):
    return [key for key, val in dic.items() if val == value][0]

def conectar_db():
    try:
        return mysql.connector.connect(**configuracion_bd)
    except Exception as e:
        sys.exit(f"Error al conectarse con la Base de Datos: {e} \n")

def check_conexiones():

    conexion = conectar_db()

    try:
        cursor = conexion.cursor()
        # Consulta para obtener la cantidad de conexiones activas
        consulta = "SHOW STATUS LIKE 'Threads_connected';"
        cursor.execute(consulta)
        resultado = cursor.fetchone()
        print("Cantidad de conexiones activas:", resultado[1])

    except mysql.connector.Error as e:
        print(f"Error al ver las conexiones: {e}")

    finally:
        cursor.close()
        conexion.close()

class Buscador():

    def __init__(self):
        self.datos_hoteles = datos_hoteles
        self.datos_apartamentos = datos_apartamentos

    def crear_tablas(self):

        conexion = conectar_db()
        cursor = conexion.cursor()

        try:
            # Crear tabla Hospedaje
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Hospedaje (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255),
                    ciudad VARCHAR(255),
                    provincia VARCHAR(255)
                )
            """)

            # Crear tabla Hotel (relacionada con Hospedaje)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Hotel (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    estrellas INT,
                    tipo_habitacion VARCHAR(255),
                    hospedaje_id INT,
                    FOREIGN KEY (hospedaje_id) REFERENCES Hospedaje(id)
                )
            """)

            # Crear tabla Apartamento (relacionada con Hospedaje)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Apartamento (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cantidad_apartamentos INT,
                    capacidad_adultos INT,
                    hospedaje_id INT,
                    FOREIGN KEY (hospedaje_id) REFERENCES Hospedaje(id)
                )
            """)

            # Confirmar los cambios
            conexion.commit()

            print(f"Se crearon las tablas correctamente")

        except mysql.connector.Error as e:
            print(f"Error al crear las tablas: {e}")

        finally:
            cursor.close()
            conexion.close()

    def insertar_datos(self):

        conexion = conectar_db()
        cursor = conexion.cursor()

        try:
            # Insertar datos en la tabla Hospedaje
            for nombre, ciudad, provincia, *_ in self.datos_hoteles + self.datos_apartamentos:
                cursor.execute("""
                    INSERT INTO Hospedaje (nombre, ciudad, provincia) VALUES (%s, %s, %s)
                """, (nombre, ciudad, provincia))

            # Obtener los IDs de los hospedajes insertados
            cursor.execute("SELECT id, nombre FROM Hospedaje")
            id_hospedajes = dict(cursor.fetchall())

            # Insertar datos en la tabla Hotel
            for nombre, _, _, estrellas, tipo_habitacion in self.datos_hoteles:
                id_hospedaje = obtener_value_de_diccionario(id_hospedajes, nombre)
                cursor.execute("""
                    INSERT INTO Hotel (estrellas, tipo_habitacion, hospedaje_id)
                    VALUES (%s, %s, %s)
                """, (estrellas, tipo_habitacion, id_hospedaje))

            # Insertar datos en la tabla Apartamento
            for nombre, _, _, cantidad_apartamentos, capacidad_adultos in self.datos_apartamentos:
                id_hospedaje = obtener_value_de_diccionario(id_hospedajes, nombre)
                cursor.execute("""
                    INSERT INTO Apartamento (cantidad_apartamentos, capacidad_adultos, hospedaje_id)
                    VALUES (%s, %s, %s)
                """, (cantidad_apartamentos, capacidad_adultos, id_hospedaje))

            # Confirmar los cambios
            conexion.commit()

            print(f"Se insertaron los datos correctamente")

        except mysql.connector.Error as e:
            print(f"Error al insertar datos: {e}")

        finally:
            cursor.close()
            conexion.close()

    def eliminar_tablas(self):
        def eliminar_tabla(nombre_tabla):

            conexion = conectar_db()
            cursor = conexion.cursor()

            try:
                # Deshabilitar claves foráneas temporalmente
                cursor.execute("SET foreign_key_checks = 0")

                # Ejecutar la instrucción DROP TABLE
                cursor.execute(f"DROP TABLE {nombre_tabla}")

                print(f"Tabla {nombre_tabla} eliminada exitosamente.")

            except mysql.connector.Error as e:
                print(f"Error al eliminar la tabla {nombre_tabla}: {e}")

            finally:
                cursor.close()
                conexion.close()

        tablas = ["Hospedaje", "Hotel", "Apartamento"]
        for tabla in tablas:
            eliminar_tabla(tabla)

    def buscar_hospedajes(self):
        def buscar_hospedaje(letras):

            conexion = conectar_db()
            cursor = conexion.cursor()

            try:
                # Realizar la consulta para obtener los hospedajes
                cursor.execute("""
                    SELECT h.nombre, h.ciudad, h.provincia, 
                        COALESCE(CONCAT(ht.estrellas, ' estrellas'), CONCAT(apts.cantidad_apartamentos, ' apartamentos')),
                        COALESCE(CONCAT('habitacion ', ht.tipo_habitacion), CONCAT(apts.capacidad_adultos, ' adultos'))
                    FROM Hospedaje h
                    LEFT JOIN Hotel ht ON h.id = ht.hospedaje_id
                    LEFT JOIN Apartamento apts ON h.id = apts.hospedaje_id
                    WHERE INSTR(LOWER(h.nombre), %s)
                    ORDER BY h.nombre
                """, (letras,))

                # en la query de arriba, también se puede utilizar WHERE LEFT(h.nombre, 3) = %s
                # esto hace que sólo coincidan las 3 primeras letras, pero creo que es mejor que las letras coincidan con el nombre completo,
                # por eso decidí hacerlo con INSTR

                resultados = cursor.fetchall()

                # Mostrar los resultados
                n = 1
                if len(resultados) == 0:
                    print("No se encontraron hospedajes, vuelve a intentarlo con otras letras")
                else:
                    print("Los resultados de su busqueda son: \n")
                    print("-"*70)
                    for resultado in resultados:
                        print(f"{n}: {resultado[0]}, {resultado[3]}, {resultado[4]}, {resultado[1]}, {resultado[2]}")
                        n += 1
                    print("-"*70)
                    print("\n")

            except mysql.connector.Error as e:
                print(f"Error al buscar hospedajes: {e}")

            finally:
                cursor.close()
                conexion.close()

        # Entrada estándar para obtener las tres primeras letras
        while True:
            entrada = input("Ingrese las tres primeras letras de su hospedaje o ingrese 0 para salir: ")
            if entrada == "0":
                break
            while len(entrada) < 3:
                print("Por favor, debe ingresar como mínimo 3 letras: ")
                entrada = input("Ingrese las tres primeras letras de su hospedaje: ")
            
            # Llamamos a la función para buscar y mostrar los hospedajes
            buscar_hospedaje(entrada)

def salir():
    print("¡Hasta luego!")
    sys.exit()

if __name__ == "__main__":
    
    while True:
        print("¿Qué desea hacer? \n")

        print("1. Crear las tablas e insertar los datos")
        print("2. Buscar un Hospedaje")
        print("3. Eliminar todas las tablas y los datos")
        print("4. salir \n")
        
        opcion = input("Ingrese su opción: ")

        buscador = Buscador()

        if opcion == "1":
            buscador.crear_tablas()
            buscador.insertar_datos()
        elif opcion == "2":
            buscador.buscar_hospedajes()
        elif opcion == "3":
            buscador.eliminar_tablas()
        elif opcion == "4":
            salir()
        else:
            print("Opción inválida. Intente nuevamente.")
        print("\n")
