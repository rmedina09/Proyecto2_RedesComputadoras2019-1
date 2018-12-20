""" Servidor de Pokemon
Este script permite visualizar la ejecucion del protocolo 
para poder capturar un pokemon por parte de un usuario.

Este archivo tambien se puede importar como un modulo y 
contiene las siguientes funciones:

	* inserta_imagen - inserta dentro de la base de datos 
	                   una imagen(bytes)

"""
__author__      = "Raul Medina Peña"
__version__    = "1.0.0"
__email__      = "raulmp@ciencias.unam.mx"

import os
import psycopg2

def inserta_imagen(id_pokemon, nombre_pokemon, ruta_imagen):
	"""Inserta una imagen en bytes dentro de una base de datos 
	
	Args: 
		id_pokemon: int 
			identificador unico del pokemon en la BD.
		nombre_pokemon: str
			nombre de pokemon en la BD.
		ruta_imagen: str
			ruta relativa de donde se guardara la imagen.

	"""

	conn = None
	try:
		conn_string = "host='localhost' dbname='dbpokemon' user='postgres' password='postgres'"
		conn = psycopg2.connect(conn_string)

		imagen = open(ruta_imagen, 'rb').read()
		tamanio = len(imagen)

		cursor = conn.cursor()
		cursor.execute("INSERT INTO pokemon (id_pokemon, nombre, tamanio_imagen, imagen) VALUES (%s,%s,%s,%s);",(id_pokemon, nombre_pokemon, tamanio, psycopg2.Binary(imagen)))
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

if __name__=='__main__':
	inserta_imagen(1, 'pikachu', 'imagenes/pikachu.jpg')
	inserta_imagen(2, 'charmander', 'imagenes/charmander.jpg')
	inserta_imagen(3, 'bulbasaur', 'imagenes/bulbasaur.jpg')
	inserta_imagen(4, 'squirtle', 'imagenes/squirtle.jpg')
	inserta_imagen(5, 'meowth', 'imagenes/meowth.jpg')

