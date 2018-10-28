import socket
import os
import argparse
import json
import sys
import threading

sys.path.extend(["./"])
def server_run(host, port, dir):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)

    while True:
        (csock, addr) = server_socket.accept()
        #threading.Thread(target=handle_client, args=(conn, addr, dir)).start()
        data_recv = csock.recv(1024)
        decode_data=data_recv.decode()
        csock.sendall(decode_data.encode("utf-8"))

        csock.shutdown(socket.SHUT_WR)
        csock.close()


def handle_client(conn, addr, dir):
    if args.debugging:
        print('Handle New client from', addr)
        while True:
            if (data):
             data = conn.recv(2048)
             data = data.decode("utf-8")
            if (not data):
             break

             (method, path, query, body, headers) = parseRequest(data)
             if (args.debugging):
                 print(method, path, body, headers)



def parse_request(port,) #include the parsing from different server



        parser = argparse.ArgumentParser(description='Socket based HTTP fileserver')
        parser.add_argument("-p", action="store", dest="port", help="Set server port", type=int, default=8080)
        parser.add_argument("-v", action="store_true", dest="debugging", help="Echo debugging mesages", default=False)
        parser.add_argument("-d", action="store", dest="directory", help="Set directory path", default='./')
    args = parser.parse_args()

    if (args.debugging):
        server_run('', args.port, args.directory)
