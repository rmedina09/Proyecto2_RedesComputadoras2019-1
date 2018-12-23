Autor: Raul Medina Peña

Institución: Facultad de Ciencias, UNAM

Fecha: 19/12/2018

-- Aplicacion que simula el juego de pokemon, implementando 
-- la arquitectura cliente servidor.

-- Creamos y cargamos la base de datos

> psql -h localhost -U postgres -f script_database_pokemon.sql 
Ingresamos el password : 'postgres'

-- Creara la Base de Datos dbpokemon

-- Creara 3 usuarios 

id   nombre

1    usuario1 

2    usuario2

3    usuario3

-- Para insertar los pokemones ejecutaremos el script 'inserta_pokemones.py'

-- NOTA: en caso de no tener instalado el modulo 'psycopg2', ejecutamos : pip install psycopg2

Creamos 5 pokemones 

1   pikachu      30

2   charmander   50

3   bulbasaur    100

4   squirtle     200

5   meowth       200   

-- Para la visualizacion de la imagen se necesita instalar el modulo Pillow:

-- ejecutamos : pip install Pillow

-- Se necesitara crear una carpeta 'salidas_tmp/', donde se guardaran las imagenes de los pokemones capturados.

-- EJECUCION

-- En una terminal
   > python servidor.py

-- En otra terminal
   > python cliente.py localhost 9999
