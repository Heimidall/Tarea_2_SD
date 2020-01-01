#!/usr/bin/env python3
# coding=utf-8

import pika
import ast
from datetime import datetime
import threading


class Server():
    #init genera una cola al crear un server
    def __init__(self,nombre_cola='Servidor', host='localhost'):
        self.nombre_cola = nombre_cola
        self.host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
        self.channel = self.connection.channel()
        self.hash_clientes = {}
        self.mensajes_sesion = {}
        self.numero_clientes = 0
        self.id_mensaje = 1
        print("El servidor se ha iniciado")

    #este es el metodo que se aplica al recibir mensajes aca es donde tratamos la data
    #recibida
    def callback(self,ch, method, properties, mensaje):
        try:
            msj = ast.literal_eval(mensaje.decode('utf-8'))
            #si el tipo de mensaje que mandamos es 0 entonces quiere deicr que es el mensaje de incio, cuando un cliente crea una cola
            #es por eso que recibimos su mensaje y le enviamos un nombre con el que el resto de los clientes lo van a conocer.
            if(msj["tipo"] == 0):
                self.numero_clientes = self.numero_clientes + 1
                cliente = "Cliente_" + str(self.numero_clientes)
                self.hash_clientes[cliente] = msj['emisor']
                print(str(self.hash_clientes))
                self.channel.basic_publish(exchange = '',routing_key=self.hash_clientes[cliente], body=str({"emisor" : "Servidor","mensaje" : "Bienvendo {}".format(cliente) ,
                                                                                                "timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S"),
                                                                                                "receptor" : cliente,
                                                                                                "tipo" : 0                                                                                            
                                                                                                }))
                print("[X] Mensaje Recibido: %r " % msj['mensaje'])   
            #si el mensaje es de tipo 1 eso quiere decir que el cliente quiere mandar un mensaje a otro cliente
            elif(msj['tipo'] == 1):
                timest = datetime.now().strftime("%d-%b-%Y|%H:%M:%S")
                self.publish(routing_key=self.hash_clientes[msj['receptor']], mensaje={"emisor" : msj['emisor'],"mensaje" : msj['mensaje'] ,
                                                                                                "timestamp" : timest,
                                                                                                "receptor" : msj['receptor'],
                                                                                                "tipo" : 1,
                                                                                                "ID_mensaje" : self.id_mensaje
                                                                                                })
                self.mensajes_sesion[msj['emisor']] = []
                self.mensajes_sesion[msj['emisor']].append({"emisor" : msj['emisor'],"mensaje" : msj['mensaje'] ,
                                                                                                "timestamp" : timest,
                                                                                                "receptor" : msj['receptor'],
                                                                                                "tipo" : 1,
                                                                                                "ID_mensaje" : self.id_mensaje
                                                                                                })
                f = open("log.txt", "a")
                f.write("[{}] |  [{}]   |  [{}]     |      [{}]      | {} \n".format(timest,msj['emisor'], msj['receptor'], self.id_mensaje, msj['mensaje']))
                self.id_mensaje = self.id_mensaje +1
                # self.channel.basic_publish(exchange = '',routing_key=self.hash_clientes[cliente], body=str({"emisor" : self.hash_clientes[msj['emisor']],"mensaje" : "Bienvendo {}".format(cliente) ,
                #                                                                                 "timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S"),
                #                                                                                 "receptor" : cliente}))
            elif(msj['tipo'] == 2):
                lista_clientes = list(self.hash_clientes.keys())
                print("El nombre de la cola que va dirigido el mensaje es: {}".format(self.hash_clientes[msj['receptor']]))
                self.publish(routing_key=self.hash_clientes[msj['emisor']], mensaje={"emisor" : msj['emisor'],"mensaje" : lista_clientes ,
                                                                                                "timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S"),
                                                                                                "receptor" : msj['emisor'],
                                                                                                "tipo" : 2
                                                                                                })
                print("Mensaje enviado {}".format(lista_clientes))

            elif(msj['tipo'] == 3):
                self.publish(routing_key=self.hash_clientes[msj['emisor']], mensaje={"emisor" : msj['emisor'],"mensaje" : self.mensajes_sesion[msj['receptor']] ,
                                                                                    "timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S"),
                                                                                    "receptor" : msj['emisor'],
                                                                                    "tipo" : 3
                                                                                    })
        except:
            print("Hubo algun error con el mensaje, por favor intente nuevmante")


    def crear_cola(self):
        t_connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
        t_channel = t_connection.channel()
        t_channel.queue_declare(queue = self.nombre_cola)
        t_channel.basic_consume(queue = self.nombre_cola, on_message_callback = self.callback, auto_ack=True)
        print("Esperando mensajes")
        t_channel.start_consuming()


    #con publish mandamos el mensaje a una cola determinada
    def publish(self, routing_key, mensaje, exchange = ''):
        self.channel.basic_publish(exchange = exchange, routing_key = routing_key, body = str(mensaje))
        print("Mensaje enviado: {}".format(mensaje))  

    def __exit__(self, exc_type, exc_eval, exc_tb):
        print("Cerrando conexion")
        self.connection.close()


if __name__ == "__main__":
    server = Server()
    #server.publish(routing_key='Cliente_1', mensaje={"emisor" : "Server","mensaje" : "Hola amiguito","timestamp" : datetime.now().strftime("%d-%b-%Y|%H:%M:%S")})
    #server.crear_cola()
    t_receptor = threading.Thread(target= server.crear_cola, daemon=True)
    t_receptor.start()
    input("Presione enter para finalizar \n")
        

