import grpc
import time
import threading

from syntax import server_pb2, server_pb2_grpc

SERVER_ADRESS = '0.0.0.0'
PORT = 8500
USER_ID = ''

class msgServiceClient(object):
	def __init__(self):
		self.channel = grpc.insecure_channel('0.0.0.0:8500')
		self.stub = server_pb2_grpc.msgServiceStub(self.channel)


	def sendMsg(self):
		while True:
			mensaje = input()

			mensaje = mensaje.split(' ')

			if len(mensaje) == 1:
				if mensaje[0] == '--usuarios':
					self.getUsers()
				elif mensaje[0] == '--mensajes':
					self.getAllMsgs()
				else:
					print('Comando invalido')

			elif len(mensaje) > 1:

				request = server_pb2.chatMsg(
					orig = USER_ID,
					dest = mensaje[0],
					msg = ' '.join(mensaje[1:])
				)

				try:
					response = self.stub.sendMsg(request)
					if response.conf == 'falso':
						print('Destinatario inexistente')
				except grpc.RpcError as err:
					print(err.details())
					print('{}, {}'.format(err.code().name, err.code().value))

	def askMsg(self):
		while True:
			time.sleep(1)
			request = server_pb2.userID(
				userID = USER_ID
			)

			try:
				response = self.stub.askMsg(request)
				if response.orig != '0':
					print('De', response.orig, '-', response.msg)
			except grpc.RpcError as err:
				print(err.details())
				print('{}, {}'.format(err.code().name, err.code().value))

	def joinChat(self):
		seguir = True
		global USER_ID

		while seguir:
			username = input('Ingrese nombre de usuario: ')

			request = server_pb2.userID(
				userID = username
			)

			try:
				response = self.stub.joinChat(request)
				print('Has iniciado sesion como:', response.userID)
				if response.userID != '-no':
					USER_ID = response.userID
					print('COMANDOS PARA EL CHAT:')
					print('* --usuarios: OBTENER TODOS LOS USUARIOS')
					print('* --mensajes: OBTENER TODOS LOS MENSAJES ENVIADOS')
					print('* (destinatario) (mensaje): ENVIAR MENSAJE A DESTINATARIO')
					seguir = False
				else:
					print('Nombre de usuario ocupado')
			except grpc.RpcError as err:
				print(err.details())
				print('{}, {}'.format(err.code().name, err.code().value))

	def getUsers(self):
		request = server_pb2.emptyz()

		try:
			response = self.stub.getUsers(request)
			print('Usuarios en el chat:')
			for userID in response.userIDS:
				print('*', userID.userID)
		except grpc.RpcError as err:
			print(err.details())
			print('{}, {}'.format(err.code().name, err.code().value))


	def getAllMsgs(self):
		request = server_pb2.userID(
			userID = USER_ID
		)

		try:
			response = self.stub.getAllMsgs(request)
			print('Mensajes:')
			for msg in response.allMsgs:
				print('* Para', msg.dest, '-', msg.msg)
		except grpc.RpcError as err:
			print(err.details())
			print('{}, {}'.format(err.code().name, err.code().value))

	def chatear(self):
		self.joinChat()

		t1 = threading.Thread(target=self.askMsg)
		t2 = threading.Thread(target=self.sendMsg)
		t1.start()
		t2.start()
		t1.join()
		t2.join()

if __name__ == '__main__':

	enviar = msgServiceClient()
	enviar.chatear()
	while True:
		time.sleep(1)