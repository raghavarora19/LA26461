from socket import *


def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind(("127.0.0.1", 9000))
    serversocket.listen(10)
    while (1):
        (clientsocket, address) = serversocket.accept()
        print(address)
        output= "it works!!"
        clientsocket.sendall(output.encode("utf-8"))
        clientsocket.shutdown(SHUT_WR)
        clientsocket.close()

    serversocket.close()


createServer()
