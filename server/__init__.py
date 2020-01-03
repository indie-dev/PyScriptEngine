import engine
import sys
import os
import socketserver
import imp
class Handler(socketserver.BaseRequestHandler):
    #For setting the file to parse
    FILE_TO_PARSE = "test/test.html"
    #For handling the request for data
    def handle(self):
        #Reload the engine module
        imp.reload(engine)
        #Initiate the engine
        self.__engine = engine.Engine(Handler.FILE_TO_PARSE)
        #For getting the byte array results
        __results = bytearray()
        #This header will be sent first
        __header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode()
        #Parse all of the scripts
        self.__data = self.__engine.execute_all_scripts()
        #Loop through the bits in the header
        for __bit in __header:
            #Add the bit ti our results array
            __results.append(__bit)
        #Loop through the bits in self.__data
        for __bit in self.__data:
            #Add the bit to our results array
            __results.append(__bit)
        #Send the data
        self.request.sendall(__results)

class Server:
    #Creates our server
    def create_server(self, port, file="test/test.html"):
        self.__path = file
        #Set the class-wide variable for port
        self.__port = port
    #Hosts our file
    def host(self, always_listen=True, serve_once=True):
        try:
            #Set the file to parse for the handler
            Handler.FILE_TO_PARSE = self.__path
            #Create the server
            server = socketserver.TCPServer(("localhost", self.__port), Handler)
            #Serve forever, or until keyboard is interruped
            server.serve_forever()
        except KeyboardInterrupt:
            #End the python program
            exit()