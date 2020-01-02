import grpc
import time

from concurrent import futures

from syntax import server_pb2, server_pb2_grpc

class msgServiceServicer(server_pb2_grpc.msgServiceServicer):
	allUsers = []
	allMsgs = dict()
	newMsgs = dict()
	allSend = dict()
	file = open('log.txt', 'w')
	file.close()

	def sendMsg(self, request, context):
		if request.dest in self.allUsers:
			orig = request.orig
			dest = request.dest
			msg = request.msg
			self.allMsgs[dest].append([orig, msg])
			self.newMsgs[dest] += 1
			self.allSend[orig].append([dest, msg])

			file = open('log.txt', 'a')
			file.write('DE ' + orig + ' PARA ' + dest + ' - ' + msg +'\n')
			file.close()

			confirmation = server_pb2.confirmation(
				conf = 'verdad'
			)

		else:
			confirmation = server_pb2.confirmation(
				conf = 'falso'
			)

		return confirmation

	def askMsg(self, request, context):
		userID = request.userID
		qtyMsgs = self.newMsgs[userID]

		if userID in self.newMsgs.keys():
			if(qtyMsgs > 0):
				lastMsg = self.allMsgs[userID][-1*qtyMsgs]
				self.newMsgs[userID] -= 1
			else:
				lastMsg = ['0', 'NM']

			msg = server_pb2.chatMsg(
				orig = lastMsg[0],
				dest = userID,
				msg = lastMsg[1]
			)

		else:
			msg = server_pb2.chatMsg(
				orig = '0',
				dest = userID,
				msg = 'NM'
			)

		return msg

	def joinChat(self, request, context):
		userID = request.userID

		if userID in self.allUsers:
			userIdMsg = server_pb2.userID(
				userID = '-no'
			)

		else:
			self.allMsgs[userID] = []
			self.newMsgs[userID] = 0
			self.allUsers.append(userID)
			self.allSend[userID] = []

			userIdMsg = server_pb2.userID(
				userID = userID
			)

		return userIdMsg

	def getUsers(self, request, context):
		allUsersMsg = []

		for user in self.allUsers:
			userID = server_pb2.userID(
				userID = user
			)

			allUsersMsg.append(userID)

		allUsersMsgPak = server_pb2.userIDS(
			userIDS = allUsersMsg
		)

		return allUsersMsgPak

	def getAllMsgs(self, request, context):
		allMsgs = []
		userID = request.userID

		for msg in self.allSend[userID]:
			chatMsg = server_pb2.chatMsg(
				orig = userID,
				dest = msg[0],
				msg = msg[1]
			)

			allMsgs.append(chatMsg)

		allMsgsPak = server_pb2.allMsgs(
			allMsgs = allMsgs
		)

		return allMsgsPak

if __name__ == '__main__':
	# Run a gRPC server with one thread.
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
	# Adds the servicer class to the server.
	server_pb2_grpc.add_msgServiceServicer_to_server(msgServiceServicer(), server)
	server.add_insecure_port('0.0.0.0:8500')
	server.start()
	print('API server started. Listening at 0.0.0.0:8500.')
	while True:
		time.sleep(60)
