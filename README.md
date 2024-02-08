# Problema

Queremos implementar una pequeña aplicación en Python con mysql connector que, tomando las tres primeras letras de la entrada estándar, devuelva por la salida estándar todas las coincidencias de hospedajes existentes en una base de datos MYSQL, ordenados por nombre, incluyendo sus características y su ubicación.

Tenemos dos tipos de hospedajes: Hoteles y Apartamentos, cada uno con sus características específicas. En el caso de los hoteles, además de su nombre, necesitamos conocer el número de estrellas y el tipo de habitación estándar que tienen (dejamos a tu elección proponer unos cuantos tipos de habitación como doble, doble con vistas, ...). En el caso de los apartamentos y además de su nombre, necesitamos conocer para cada propiedad cuantos apartamentos tienen disponibles y para cuantos adultos tienen capacidad, teniendo en cuenta que sólo tienen un tipo de apartamentos.

Para la ubicación de cualquier hospedaje nos basta con indicar la ciudad y provincia.

La salida (a mostrar por salida estándar) debería ser un listado del siguiente tipo:

- Hotel Azul, 3 estrellas, habitación doble con vistas, Valencia, Valencia
- Apartamentos Beach, 10 apartamentos, 4 adultos, Almeria, Almeria
- Hotel Blanco, 4 estrellas, habitación doble, Mojacar, Almeria
- Hotel Rojo, 3 estrellas, habitación sencilla, Sanlucar, Cádiz
- Apartamentos Sol y playa, 50 apartamentos, 6 adultos, Málaga, Málaga

# Solución

1. Construimos la imagen Docker con la Base de datos MySQL:
```
docker run --name some-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=viajes_pass_root -e MYSQL_DATABASE=viajes_db -e MYSQL_USER=viajes_user -e MYSQL_PASSWORD=viajes_pass -d mysql:latest
```

2. Instalamos las dependencias del sistema
```
sudo apt-get install pkg-config build-essential libmysqlclient-dev
```

3. Instalamos los requerimientos
```
pip3 install mysqlclient mysql-connector-python
```

Al ejecutar el archivo buscador.py nos mostrará un menú como la siguiente imagen:

  <img src="https://github.com/m4ty4s28/Buscador-de-Hoteles-y-Apartamentos/blob/main/imagen_menu_buscador.png">
  
Aquí debemos seleccionar la primera opción (1) para que se creen los datos en la Base de Datos, 

Y luego la segunda opción (2) para acceder al Buscador de Hospedajes
