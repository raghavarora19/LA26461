import socket
import argparse


def get(directory, port):
    request = "GET / HTTP/1.0\r\n" + directory + "\r\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect(("127.0.0.1", port))
    s.sendall(request.encode())
    result = s.recv(4096)
    incoming = result.decode()
    print(incoming)
    s.shutdown(socket.SHUT_WR)
    s.close()


def post(directory, port,data):
    request = "POST / HTTP/1.0\r\n" + directory + "\r\n" + data + "\r\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect(("127.0.0.1", port))
    s.sendall(request.encode())
    result = s.recv(4096)
    response = result.decode()
    print(response)
    s.shutdown(socket.SHUT_WR)
    s.close()


def main():
    argParser = argparse.ArgumentParser(description='Socket based HTTP fileserver')
    argParser.add_argument('req_type', type=str, help="GET/POST")
    argParser.add_argument("directory", type=str, action="store", help="Set directory path", default='/')

    argParser.add_argument("-d", '--data', type=str, action="store", nargs="+", help="POST DATA")
    argParser.add_argument("-p", '--port', action="store", help="Set server port", type=int, default=8080)
    args = argParser.parse_args()

    if args.req_type == "GET" and "get":
        get(args.directory, args.port)
    elif args.req_type == "POST" and "post":
        post(args.directory,args.port, ''.join(args.data))


main()
