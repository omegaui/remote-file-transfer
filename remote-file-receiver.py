# Send a file to the server
# @author: @omegaui <github.com/omegaui>
# @license: GNU GPL v3

import socket
from pick import pick
from termcolor import colored, cprint

server = socket.socket()

try:
	print('Starting file server ...')
	server.bind((socket.gethostname(), 20000))
	print('Starting file server ... Done!')
except:
	print('Cannot start the server!')
	exit()

server.listen(5)

def accept_request(clientSocket, address, fileName):
	clientSocket.send('Request Accepted'.encode('utf-8'))
	mimetype = clientSocket.recv(1024).decode('utf-8')
	isTextFile = mimetype.endswith('True')
	
	blobSize = int(clientSocket.recv(1024).decode('utf-8'))
	
	fileBlob = clientSocket.recv(blobSize, socket.MSG_WAITALL)
	fileContent = fileBlob.decode('utf-8') if isTextFile else fileBlob
	
	print('received blob size : ', blobSize)
	print('received content blob size : ', len(fileContent))
	
	with open(fileName, 'w' if isTextFile else 'wb') as fileObj:
		fileObj.write(fileContent)
		cprint('File Saved : {0}'.format(fileName), 'white', 'on_green')

def deny_request(clientSocket, address):
	clientSocket.send('Request Denied'.encode('utf-8'))

def process_request(request, clientSocket, address):
	message = request.decode('utf-8')
	cprint('Processing Request : ' + str(message), 'white', 'on_blue')
	if message.startswith('Sending File : '):
		fileName = message[(message.rfind('/') + 1):]
		decision, index = pick(['Accept', 'Deny'], 'A client (address: {0}) wants to send {1} file!'.format(address, fileName))
		if index == 0:
			accept_request(clientSocket, address, fileName)
		else:
			deny_request(clientSocket, address)

while True:
	clientSocket, address = server.accept()
	request = clientSocket.recv(1024)
	process_request(request, clientSocket, address)

