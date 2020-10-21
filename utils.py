#!/usr/bin/python3

import socket, sys, asyncio



#function that writes data to a file with a name stored in 'file_name'
def writeFile(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()

#function that reads and returns data from a file with a name stored in 'file_name'
def readFile(file_name):
    f = open(file_name, "rb")
    data = f.read()
    f.close()
    return data

#uses a socket to receive data and return it as a string until a newline is found
def getLine(sc):
	data = sc.recv(1)
	new_buffer = b''
	while (data != b'\n'):
		new_buffer += data
		data = sc.recv(1)
	return new_buffer

# this function uses a socket to receive data up to a size amount.
# Parameters include a valid TCP socket, and an int representing 
# size of the data to receive. 
def getBuff(sock, size):
    buffer = b''
    buffer_size = 0
    while buffer_size < size:
        chunk = size - buffer_size
        buffer += sock.recv(min(chunk, BUFF_SIZE))
        buffer_size = len(buffer)
    return buffer

