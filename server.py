from socket import *


def createServer():
    servsock = socket(AF_INET, SOCK_STREAM)
    servsock.bind(("127.0.0.1", 8082))
    servsock.listen(5)
    while (1):
        (csock, address) = servsock.accept()

        data_recv = csock.recv(1024)
        decode_data=data_recv.decode()
        frag = decode_data.split('\n\n')
        header = frag[0]
        head = frag[1]
        inline_file = frag[2]
        print(frag)
        print(head)

        output = "\n" + head

        csock.sendall(output.encode("utf-8"))

        csock.shutdown(SHUT_WR)
        csock.close()

    servsock.close()


createServer()
