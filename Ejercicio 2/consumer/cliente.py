#!/usr/bin/env python3
# coding=utf-8

import pika
import ast
from datetime import datetime
import threading
import random
import string


class Cliente():
    #init genera una cola al crear un server
    def __init__(self,nombre_cola='Cliente', host='localhost'):
        temp_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        self.nombre_cola = temp_name
        self.nombre_cliente = temp_name
        self.host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
        self.channel = self.connection.channel()
        #print("El servidor se ha iniciado")

    #este es el metodo que se aplica al recibir mensajes aca es donde tratamos la data
    #recibida
    def callback(self,ch, method, properties, mensaje):
        msj = ast.literal_eval(mensaje.decode('utf-8'))
        #print("CallBack {}\n".format(msj))
        if(msj['tipo'] == 0):
            self.nombre_cliente = msj['receptor']
            print("Bienvenido su ID es {}".format(self.nombre_cliente))

        elif(msj['tipo'] == 1):
            print("MENSAJE RECIBIDO")
            print("----------------------------------------------------------------------------")
            print("[Timestamp]            |  [  Emisor ]  | [ID_mensaje]  |  [Mensaje] ")
            print("[{}] |  [{}]  |      [{}]      | {}".format(msj['timestamp'],msj['emisor'], msj['ID_mensaje'], msj['mensaje'])) 
            print("----------------------------------------------------------------------------")

        elif(msj['tipo'] == 2):
            print("Los clientes conectados al chat son:")
            for name in msj['mensaje']:
                print(name)
        elif(msj['tipo'] == 3):
            print("LISTA DE MENSAJES:")
            for his_mensaje in msj['mensaje']:
                print("----------------------------------------------------------------------------")
                print("[Timestamp]            |  [  Emisor ]   |  [  Receptor ]  | [ID_mensaje]  |  [Mensaje] ")
                print("[{}] |  [{}]   |  [{}]     |      [{}]      | {}".format(his_mensaje['timestamp'],his_mensaje['emisor'], his_mensaje['receptor'] ,his_mensaje['ID_mensaje'], his_mensaje['mensaje'])) 
                print("----------------------------------------------------------------------------")

        #print("[X] Mensaje Recibido: %r " % msj['mensaje'])   

    def crear_cola(self):
        try:
            t_connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
            t_channel = t_connection.channel()
            t_channel.queue_declare(queue = self.nombre_cola)
            t_channel.basic_consume(queue = self.nombre_cola, on_message_callback = self.callback, auto_ack=True)
            #print("Esperando mensajes")
            self.channel.basic_publish(exchange = '', routing_key='Servidor', body=str({"emisor" : self.nombre_cola,
                                                            "mensaje" : "Necesito nombre",
                                                            "timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S"),
                                                            "tipo" : 0 
                                                            }))
            t_channel.start_consuming()
        except:
            print("Ocurrió un problema creando la cola, por favor intente nuevamente")


    #con publish mandamos el mensaje a una cola determinada
    def publish(self, routing_key, mensaje, exchange = ''):
        try:
            self.channel.basic_publish(exchange = exchange, routing_key = routing_key, body = str(mensaje))
            #print("Mensaje enviado: {}".format(mensaje))  
        except:
            print("Ocurrió un problema, por favor intente de nuevo")    

    def __exit__(self, exc_type, exc_eval, exc_tb):
        print("Cerrando conexion")
        self.connection.close()

if __name__ == "__main__":
    cliente = Cliente()
    #server.publish(routing_key='Cliente_1', mensaje={"emisor" : "Server","mensaje" : "Hola amiguito","timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S")})
    #server.crear_cola()
    t_receptor = threading.Thread(target= cliente.crear_cola, daemon=True)
    t_receptor.start()
    '''    cliente.publish(routing_key='Servidor', mensaje={"emisor" : cliente.nombre_cola,
                                                        "mensaje" : "Necesito nombre",
                                                        "timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S"),
                                                        "tipo" : 0 
                                                        })'''
    #print("El nombre de la cola es {}".format(cliente.nombre_cola))

    value1 = True
    while value1:
        print("----------------------------------------------------------------------------")
        print("Elija una opcion a ejecutar:")
        print("1) Enviar mensaje")
        print("2) Revisar mensajes enviados")
        print("3) Ver lista de clientes")
        print("4) Salir")
        print("----------------------------------------------------------------------------")
        seleccion = input()
        if(seleccion == '1'):
                cliente_name = str(input("ingrese el nombre del cliente al que desea enviar el mensaje: "))
                if(cliente_name):
                    print("Ingrese el mensaje a enviar:")
                    mensaje = input()
                    #Este mensaje tiene que pasar por el servidor, porque sabemos el nombre máscara que tiene cada cliente, pero al fin y al cabo
                    #El server es el que sabe cada uno de los nombres verdaderos de las colas.
                    cliente.publish(routing_key='Servidor', mensaje={"emisor" : cliente.nombre_cliente,
                                                            "mensaje" : mensaje,
                                                            "timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S"),
                                                            "tipo" : 1,
                                                            "receptor" : cliente_name,
                                                            })
                    # t_mensaje = threading.Thread(target=cliente.publish(routing_key=cliente, mensaje={"emisor" : cliente.nombre_cola,
                    #                                         "mensaje" : mensaje,
                    #                                         "timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S"),
                    #                                         "tipo" : 1 
                    #                                         }), daemon=True)
                    # t_mensaje.start()

                else:
                    print("El nombre ingresado no corresponde")
        elif(seleccion == '2'):
            cliente.publish(routing_key='Servidor', mensaje={"emisor" : cliente.nombre_cliente,
                                                "mensaje" : "Necesito la lista de mensajes",
                                                "timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S"),
                                                "tipo" : 3,
                                                "receptor" : cliente.nombre_cliente 
                                                })
        elif(seleccion == '3'):
            #mensaje tipo dos significa que solicito por la lista de todos los clientes conectados.
            cliente.publish(routing_key='Servidor', mensaje={"emisor" : cliente.nombre_cliente,
                                                            "mensaje" : "Necesito la lista de clientes",
                                                            "timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S"),
                                                            "tipo" : 2,
                                                            "receptor" : cliente.nombre_cliente 
                                                            })

        elif(seleccion == '4'):
            print("Terminando conexion")
            value1 = False
