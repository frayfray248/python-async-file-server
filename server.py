#!/usr/bin/python3.8

import sys, asyncio

# constants
HOST = 'localhost' 
PORT = 12345
BUFF_SIZE = 1024

# This is the main function for the asyncio file server. It waits to receive a file name from a client,
# then if the file name is valid, sends the requested file in 1024 bytes at a time.
# Parameters include an asyncio reader and writer. Exceptions include an invalid file name (a requested 
# file with a '/').
async def sendFile(reader, writer):
    try:
        # receive filename of requested file
        coded_file_name = await reader.readline()
        file_name = coded_file_name.decode('utf-8')

        # file name validation
        if '/' in file_name:
            raise Exception("SERVER (Error): invalid file name was requested")

        # printing client and request details
        addr = writer.get_extra_info('peername') # client address
        print("CLIENT (" + addr[0] + "): " + file_name)
        print('SERVER: received filename' + str(file_name))

        # open file reader
        f = open("library/" + file_name.strip(), 'rb')

        # read and send data in BUFF_SIZE bytes at a time
        while (True):
            data = f.read(BUFF_SIZE)
            if data == b'':
                break
            writer.write(data)
            await writer.drain() # drain writer buffer
        
        
        # file and asyncio writer/reader close statements
        f.close() # close file reader
        writer.close() # close asyncio writer
        await writer.wait_closed()
    except Exception as e:
        print(e)


# asyncio wrapper that launches a file server forever. 
async def main():
    # start server
    server = await asyncio.start_server(sendFile, HOST, PORT)
    # server started message
    print("SERVER: started server (" + str(HOST) + ", " + str(PORT) + ")")
    await server.serve_forever()
asyncio.run(main())