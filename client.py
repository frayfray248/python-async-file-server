#!/usr/bin/python3.8

import sys, asyncio

# constants
HOST = 'localhost'
PORT = 12345
BUFF_SIZE = 1028

# exit if no arguements (filename) was provided
if len(sys.argv) != 2:
    print(sys.argv[0] + " error: one argument (a file name) is required")
    sys.exit()

# This is the main function of the asyncio client. It sends a file name provided by a program argument, and waits
# to receive/write the requested file in 1024 bytes at a time.
async def main():
    try:
        # connect to the host and send it a requested filename provided by the program argument
        reader, writer = await asyncio.open_connection(HOST, PORT)
        writer.write((sys.argv[1]+'\n').encode('utf-8'))
        # print client send request status
        print("CLIENT: sent file request")

        # open file for writing
        f = open(sys.argv[1], 'wb')

        # write and receive data in BUFF_SIZE bytes at a time
        while (True):
            data = await reader.read(BUFF_SIZE)
            f.write(data)
            if data == b'':
                break
            

        # file received message
        print("CLIENT: received file")
        
        # file and asyncio writer/reader close statements
        f.close()
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(e)

# asyncio wrapper
asyncio.run(main())