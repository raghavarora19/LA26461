from socket import *


def get_server_response(decode_data):
    a = 0


def post_server_response(decode_data):
    frag = decode_data.split('\n\n')
    header = frag[0]
    head = frag[1]
    inline_file = frag[2]

    # Header Conversion
    head = head.replace(':', "\r\n")
    head_new = head.split("\r\n")
    head_new = head_new[1:len(head_new) - 1]
    new_header = []
    for i in range(0, len(head_new) - 1, 2):
        new_header.append('"' + head_new[i] + '"' + ":" + '"' + head_new[i + 1] + '"')
    head = "\n".join(new_header)

    output = "" + head
    return output


def createServer():
    servsock = socket(AF_INET, SOCK_STREAM)
    servsock.bind(("127.0.0.1", 8081))
    servsock.listen(5)
    while (1):
        (csock, address) = servsock.accept()

        data_recv = csock.recv(1024)
        decode_data = data_recv.decode()
        output="Raghav"

        if "GET" or "get" in header:
            get_server_response(decode_data)
        else:
            output = post_server_response(decode_data)
        print(output)
        csock.sendall(output.encode("utf-8"))

        csock.shutdown(SHUT_WR)
        csock.close()

    servsock.close()


createServer()
