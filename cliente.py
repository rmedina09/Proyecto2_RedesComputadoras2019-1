"""Cliente Pokemon

Este script permite a un usuario conectarse a un servidor pokemon,
para poder capturar un pokemon. Este pokemon es en forma de imagen,
por medio de la implementacion de una maquina de estados finitos.

"""
__author__      = "Raul Medina Peña"
__version__    = "1.0.0"
__email__      = "raulmp@ciencias.unam.mx"

import sys
import io
import struct
import psycopg2
from socket import socket
from PIL import Image
from socket import error

def select_pokemones(id_user):
    """ Obtiene una lista de cadenas de una Base de Datos

    Args :
        id_user: int
            es el identificador del usuario en la Base de datos.

    Returns:
        list de str que son los nombres de lo pokemones del usuario.
    """
    arr_pokemones = []
    conn = None
    try:
        conn_string = "host='localhost' dbname='dbpokemon' user='postgres' password='postgres'"
        conn = psycopg2.connect(conn_string)

        cursor = conn.cursor()
        cursor.execute("SELECT pokemon.nombre FROM pokemon INNER JOIN usuario_pokemon ON usuario_pokemon.id_pokemon = pokemon.id_pokemon WHERE usuario_pokemon.id_usuario = %s;", (id_user,))
        rows = cursor.fetchone()        
        #arr_pokemones.append(str(rows[0]))

        while rows is not None:
            arr_pokemones.append(str(rows[0]))
            rows = cursor.fetchone()

        conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("hola")
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return arr_pokemones


def main(argv):
    """Comienza la ejecucion del programa
    
    Funcion principal del script que simula una Maquina Finita de Estados (FSM).

    Args:
        argv: list de str
            argv[1] es la direccion IP y argv[2] es el numero de puerto.

    Returns:
        str los mensajes de aslida en la terminal.

    """
    s = socket()
    servidor = argv[1]
    puerto = int(argv[2])
    s.connect((servidor, puerto))
    usuario = 0
    mensaje = '\x00'
    nombres_pokemon = {1:'pikachu', 2:'charmander', 3:'bulbasaur', 4:'squirtle', 5:'meowth'}
    path_out = 'salidas_tmp/'

    # ESTADO INICIAL : 
    print ("\nIMPLEMENTACION DEL JUEGO POKEMON\n")

    print("\nUSUARIOS : \n 1 - Usuario1 \n 2 - Usuario2 \n 3 - Usuario3\n")
    entrada = input("Teclea el numero de usuario:  ")
    
    try:
        usuario = int(entrada)
    except:
        codigo = bytes([40])
        mensaje = codigo
        s.send(mensaje)
        s.close()
        print("\nOpcion invalida  \nTerminando conexion ...")
        sys.exit()

    if usuario == 1 or usuario == 2 or usuario == 3:
        pass
    else:
        codigo = bytes([40])
        mensaje = codigo
        s.send(mensaje)
        s.close()
        print("\nOpcion invalida  \nTerminando conexion ...")
        sys.exit()
        
    print("\n\nMENU \n 1 - Jugar \n 2 - Ver pokemones capturados \n")
    opcion = input("Tecla tu opcion:  ")

    try:
        op = int(opcion)
    except:
        codigo = bytes([40])
        mensaje = codigo
        s.send(mensaje)
        s.close()
        print("\nOpcion invalida  \nTerminando conexion ...")
        sys.exit()

    if op == 1:
        pass
    elif op == 2:
        print("\n POKEMONES : \n")
        l_pokemones = select_pokemones(usuario)
        print(l_pokemones if l_pokemones else "\nNo tienes pokemones")
    else:
        codigo = bytes([40])
        mensaje = codigo
        s.send(mensaje)
        s.close()
        print("\nOpcion invalida  \nTerminando conexion ...")
        sys.exit()

    print ("\n Comenzamos ... \n")
    # simulamos el estado incial enviando el primer mensaje 10
    codigo = bytes([10])
    mensaje = codigo
    s.send(mensaje)

    # FIN ESTADO INICIAL

    while True:
        try:
            #Recibimos el mensaje
            input_data = s.recv(4096)

            if input_data[0] == 20:
                id_pokemon = input_data[1]
                print("\n Quieres capturar al pokemon %s \n" % nombres_pokemon.get(id_pokemon,""))
                respuesta = input("Teclea si o no : ")

                if respuesta == 'si':
                    #creamos el codigo 30
                    codigo = bytes([30])
                    mensaje = codigo
                elif respuesta == 'no':
                    #creamos el codigo 31
                    codigo = bytes([31])
                    mensaje = codigo
                    print("\nEs una lastima, hasta luego !!!\n")
                else:
                    print ("\nRespuesta invalida ...")
                    print ("\nTerminando conexion ...")                    
                    codigo = bytes([32])
                    mensaje = codigo
                    s.send(mensaje)
                    s.close()
                    break
            
            elif input_data[0] == 21:
                attemps = input_data[2]
                print("No lo has capturado ..\n")
                print("\n ¿Intentar capturar de nuevo?  Quedan %d intentos \n" % attemps)
                respuesta = input("Teclea si o no : ")

                if respuesta == 'si':
                    #creamos el codigo 30
                    codigo = bytes([30])
                    mensaje = codigo
                elif respuesta == 'no':
                    #creamos el codigo 31
                    codigo = bytes([31])
                    mensaje = codigo
                    print("\nEs una lastima, hasta luego !!!\n")
                else:
                    print ("respuesta invalida ...")
                    print ("cerrando conexion ...")
                    #sleep
                    s.close()
                    break

            elif input_data[0] == 22:
                id_pokemon = input_data[1]
                aux = input_data[2:6]
                tam_aux = struct.unpack("I", aux) 
                tamanio_imagen = int(tam_aux[0])

                bytes_recibidos = input_data[6:]
                num_bytes_recibidos = len(bytes_recibidos)

                # guardamos toda la imagen, en caso de que el tamanio de la imagen
                # sea mas grande que el buffer del socket
                while num_bytes_recibidos < tamanio_imagen:
                    input_data_aux = s.recv(4096)
                    bytes_recibidos = bytes_recibidos + input_data_aux
                    num_bytes_recibidos = len(bytes_recibidos)

                print("\nCapturaste al pokemon %s \n" % nombres_pokemon.get(id_pokemon, ""))
                #sleep
                
                #guardamos la imagen
                open(path_out + nombres_pokemon.get(id_pokemon,"") + '.jpg', 'wb').write(bytes_recibidos)
                print("guardamos el pokemon....\n")

                #abrimos la imagen en una ventana
                imagen = Image.open(io.BytesIO(bytes_recibidos))
                imagen.show()
                
                #construimos el mensaje 
                codigo = bytes([33])
                #enviamos el id de usuario para que el servidor lo almacene en la base de datos
                id_user = bytes([usuario])
                mensaje = codigo + id_user
                s.send(mensaje)
                print("Terminando conexion ...")
                usuario = 0
                s.close()
                break

            elif input_data[0] == 23:
                print("\nNumero de intentos de captura agotados\n")
                print("cerrando sesion")
                #creamos el codigo 32 
                codigo = bytes([32])
                mensaje = codigo                
                s.send(mensaje)
                usuario = 0
                s.close()
                break

            elif input_data[0] == 31:
                print("Cerrando sesion")
                #creamos el codigo 32 
                codigo = bytes([32])
                mensaje = codigo                
                s.send(mensaje)
                usuario = 0
                s.close()
                break

            elif input_data[0] == 32:
                print("Terminando conexion ..\n")
                usuario = 0
                s.close()
                break

            elif input_data[0] == 40:
                print("Error en los datos ...")
                print("Terminando conexion ..\n")
                usuario = 0
                s.close()
                break

        except error:
            print("Error en los datos ....")
            print("\nTerminando conexion\n")
            codigo = bytes([40])
            mensaje = codigo
            s.send(mensaje)
            s.close()
            break
        else:
            # Enviamos el mensaje
            s.send(mensaje)
                            
if __name__ == "__main__":
    if (len(sys.argv) == 3):
        main(sys.argv)
    else :
        print("Uso : python cliente.py <servidor> <puerto>")