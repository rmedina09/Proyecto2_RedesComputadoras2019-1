-- Author : Raul Medina Peña
-- Version: 1.0.0
-- Fecha  : 19/12/2018

-- Creamos la base de datos
CREATE DATABASE dbpokemon;

-- Nos cambiamos a la base de datos 'dbpokemon'
\c dbpokemon;

-- Creamos la tabla usuario
CREATE TABLE usuario(
	id_usuario int PRIMARY KEY,
	nombre varchar(100)	
);

-- Creamos la tabla pokemon
CREATE TABLE pokemon(
	id_pokemon int PRIMARY KEY,
	nombre varchar(100),
	tamanio_imagen int,
	imagen bytea
);

-- Creamos la tabla usuario_pokemon, esta tabla relaciona las tablas usuario y pokemon
CREATE TABLE usuario_pokemon(
	id_usuario int REFERENCES usuario (id_usuario) ON UPDATE CASCADE ON DELETE CASCADE,
	id_pokemon int REFERENCES pokemon (id_pokemon) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT usuario_pokemon_pkey PRIMARY KEY (id_usuario, id_pokemon)
);

-- Insertar usuarios por default
INSERT INTO usuario (id_usuario, nombre) VALUES (1, 'nombre1');
INSERT INTO usuario (id_usuario, nombre) VALUES (2, 'nombre2');
INSERT INTO usuario (id_usuario, nombre) VALUES (3, 'nombre3');
