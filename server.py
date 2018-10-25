from socket import *


def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind(("127.0.0.1", 8083))
    serversocket.listen(10)
    while (1):
        (clientsocket, address) = serversocket.accept()
        print(address)
        output= "it works!!"
        data= clientsocket.recv(1024)
        print(data.decode())
        clientsocket.sendall(output.encode("utf-8"))
        clientsocket.shutdown(SHUT_WR)
        clientsocket.close()

    serversocket.close()


createServer()


