# Send a file to the server
# @author: @omegaui <github.com/omegaui>
# @license: GNU GPL v3

import socket, os, keyboard, pathlib
from pick import pick
from termcolor import colored, cprint
import magic

print('Finding the Server ...')

try:
	serverSocket = socket.socket()
	serverSocket.connect(('192.168.43.1', 20000))
	print('Connected to the Server!')
except:
	print('Unable to connect to the server!')
	print('Make sure that the Server is running.')
	exit()

def process_response(filePath):
	response = serverSocket.recv(1024)
	message = response.decode('utf-8')
	if not message == 'Request Denied':
		print('Server has accepted the last request')
		send_file(filePath)
	else:
		print('Server has denied the last request')

def send_file(filePath):
	mimetype = magic.Magic(mime=True).from_file(filePath)
	isTextFile = mimetype.startswith('text/')
	serverSocket.send('Mimetype : {0}'.format(isTextFile).encode('utf-8'))

	with open(filePath, 'r' if isTextFile else 'rb') as fileObj:
		content = fileObj.read()

		
		blobSize = len(content.encode('utf-8') if isTextFile else content)
		print('transfered blob size : ', blobSize)
		serverSocket.send('{0}'.format(blobSize).encode('utf-8'))

		serverSocket.send(content.encode('utf-8') if isTextFile else content)
		cprint('File received by the Server!', 'white', 'on_green')

def pick_file_to_send(root):
	osGeneratedFileList = os.listdir(root)
	fileList = ['.']
	for item in osGeneratedFileList:
		fileList.append(item)
	if len(fileList) != 0:
		fileName, index = pick(sorted(fileList), 'Select the file to send: ', indicator='=>')
		if index == 0 and root.rfind('/') != 0:
			pick_file_to_send(root[:root.rfind('/')])
		path = root + '/' + fileName
		filePath = pathlib.Path(path)
		if not filePath.is_file():
			return pick_file_to_send(path)
		else:
			return path
	else:
		return pick_file_to_send(root[:root.rfind('/')])

root, _ = pick(['/', os.environ['HOME']], 'Choose Initial Directory', indicator='=>')
path = pick_file_to_send(root)
if path != None:
	choice, index = pick(['Yes', 'No'], 'Do you really want to send {0}?'.format(path), indicator='=>')
	if index == 0:
		request = 'Sending File : {0}'.format(path)
		serverSocket.send(request.encode('utf-8'))
		process_response(path)

