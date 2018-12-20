"""Servidor Pokemon

Este script permite implementar un servidor de pokemones, de manera
que puede recibir solicitudes de conexion de varios cliente de manera
concurrente, por medio de hilos (Threads). Por medio de una Base de 
Datos puede proporcionar en forma de imagenes los pokemones capturados
a los usuarios del juego.
Esta implementacion esta construida a partir de una Maquina Finita de 
Estados (FSM)

"""
__author__      = "Raul Medina Peña"
__version__    = "1.0.0"
__email__      = "raulmp@ciencias.unam.mx"

from socket import socket, error
from threading import Thread
import random
import psycopg2
import struct

class Client(Thread):
    """Simula a un jugador que quiere capturar a un Pokemon
    
    Esta clase ofrece las acciones necesarias para poder capturar los
    pokemones por medio de un usuario. Y simula la creacion de usuarios
    por parte del servidor para poder administrarlos de manera concurrente
    por medio de hilos de ejecucion (Threads)

    Attributes:
        conn: socket
            es el canal de comunicacion (buffer) con el cliente.
        addr: (str, int)
            la direccion ip del servidor, el numero de puerto.

    
    """
    
    def __init__(self, conn, addr):
        """ Inicializa  la clase padre de un cliente en el servidor.
        
        Args: 
            conn (socket) : Describe el socket asignado a un cliente.
            addr (str) : Describe la direccion ip del servidor y el numero de puerto.
        """
        Thread.__init__(self)
        
        self.conn = conn
        self.addr = addr
   
    def run(self):
        """ Ejecuta el hilo 

        Se implementa el comportamiento de la FSM en el servidor.

        """
        #inicializamos el id del pokemon
        id_p = 0
        num_pokemones = 5
        mensaje = '\x00'
        num_attemps = 5

        while True:
            try:
                # Recibir datos del cliente.
                input_data = self.conn.recv(4096)

                if input_data[0] == 10:
                    print("%s:%d Se le ofrece un pokemon aleatorio ... " % self.addr)
                    #creamos el codigo 20 
                    codigo = bytes([20])
                    #generamos un numero aleatorio entre 1 y total de pokemones
                    id_p = random.randint(1,num_pokemones)
                    #cramos el byte para el id del pokemon
                    id_pokemon = bytes([id_p])
                    #creamos el mensaje 
                    mensaje = codigo + id_pokemon

                elif input_data[0] == 30:
                    if num_attemps <= 0:
                        print("%s:%d Se acabaron sus intentos ... " % self.addr)
                        #se crea el mesaje para el codigo 23
                        codigo = bytes([23])
                        mensaje = codigo
                    else:
                        #Indicamos aleatoriamente si se capturo al Pokemon o no
                        resp_capturo = random.randint(1, 10)
                        if resp_capturo == 3 or resp_capturo == 7 or resp_capturo == 9:
                            print("%s:%d Capturo un pokemon ... " % self.addr)
                            #Entonces capturo el pokemon, ingresamos a la BD
                            imagen_db = select_imagen(id_p)
                            tam = imagen_db[2]
                            img = imagen_db[3]

                            #creamos el codigo 22
                            codigo = bytes([22])
                            id_pokemon = bytes([id_p])
                            tam_img = struct.pack("I", int(tam))
                            mensaje = codigo + id_pokemon + tam_img + img

                        else:
                            #creamos el codigo 21 
                            codigo = bytes([21])
                            id_pokemon = bytes([id_p])                            
                            n_att = bytes([num_attemps])
                            mensaje = codigo + id_pokemon + n_att
                            num_attemps-=1
                
                elif input_data[0] == 31:
                    #terminamos la sesion
                    #creamos el codigo 32 
                    codigo = bytes([32])
                    mensaje = codigo
                    self.conn.send(mensaje)
                    print("%s:%d se ha cerrado su sesion." % self.addr)
                    self.conn.close()
                    break;
                
                elif input_data[0] == 33:
                    #antes de terminar la conexion guardamos el pokemon capturado
                    id_user = input_data[1]
                    #actualizamos la base de datos asignando al usuario el pokemon capturado
                    inserta_usuario_pokemon(id_user, id_p)
                    #terminamos la conexion
                    print("%s:%d se ha terminado su conexion" % self.addr)                    
                    self.conn.close()
                    break;

                elif input_data[0] == 40:
                    print("Error ...")
                    print("%s:%d se ha terminado su conexion" % self.addr)                    
                    usuario = 0
                    self.conn.close()
                    break

            except error:
                print("Error en los datos  ...")
                print("%s:%d se ha terminado su conexion" % self.addr)                    
                usuario = 0
                codigo = bytes([40])
                mensaje = codigo
                self.conn.send
                self.conn.close()
                break

            else:
                #Enviamos el mensaje
                self.conn.send(mensaje)

def select_imagen(id_pokemon):
    """ Obtiene la imagen en bytes de una Base de Datos

    Args: 
        id_pokemon : int
            es el identificador del pokemon en la Base de Datos.

    Returns:
        array(bytes) que es la imagen en bytes.

    """
    conn = None
    imagen_db = '\x00'
    try:
        conn_string = "host='localhost' dbname='dbpokemon' user='postgres' password='postgres'"
        conn = psycopg2.connect(conn_string)

        cursor = conn.cursor()
        cursor.execute("SELECT id_pokemon, nombre, tamanio_imagen, imagen FROM pokemon WHERE id_pokemon = %s;", (id_pokemon,))
        imagen_db = cursor.fetchone()

        conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return imagen_db

def inserta_usuario_pokemon(id_usuario, id_pokemon):
    """ Inserta un nuevo elemento en la tabla usuario_pokemon de la base de datos

    Determina la asignacion de los pokemones a los usuarios.

    Args:
        id_usuario : int
            es el identificador del usuario en la Base de Datos.
 
        id_pokemon : int
            es el identificador del pokemon en la Base de Datos.

    """
    conn = None
    try:
        conn_string = "host='localhost' dbname='dbpokemon' user='postgres' password='postgres'"
        conn = psycopg2.connect(conn_string)

        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuario_pokemon (id_usuario, id_pokemon) VALUES (%s,%s);",(id_usuario, id_pokemon))
        conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def main():
    """ Funcion principal del progama

    """
    s = socket()
    
    # Escuchar peticiones en el puerto 9999.
    s.bind(("localhost", 9999))
    s.listen(0)
    
    while True:
        conn, addr = s.accept()
        c = Client(conn, addr)
        c.start()
        print("%s:%d se ha conectado." % addr)

if __name__ == "__main__":
    main()