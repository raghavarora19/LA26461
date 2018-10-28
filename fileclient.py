import socket
import argparse




def get(directory, action, port):
    request= "GET / HTTP/1.0\r\n" + directory + "\r\n\r\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    request_new =request.split("/")
    if request_new[0] == " ":
      s.connect(("127.0.0.1", port))
      s.sendall(request.encode())
    else:
      def get(directory, action, port):
       request = "GET / HTTP/1.0\r\n" + directory + "\r\n\r\n"
       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.connect(("127.0.0.1", port))
       s.sendall(request.encode())
def post(directory, data, portx):
    request = "POST / HTTP/1.0\r\n" + directory + " " + data + "\r\n\r\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", port))
    s.sendall(request.encode())

def main():

        argParser = argparse.ArgumentParser(description='Socket based HTTP fileserver')
        argParser.add_argument('req_type', type=str, help="GET/POST")
        argParser.add_argument('action', type=str, help="specific action user is doing")
        argParser.add_argument("p", action="store", dest="port", help="Set server port", type=int, default=8080)
        argParser.add_argument("data", type= str, action="store", nargs="+", help="Echo debugging mesages", default=False)
        argParser.add_argument("d", action="store", dest="directory", help="Set directory path", default='./')
        args = argParser.parse_args()

        if args.req_type == "get" and "GET" :
            get(args.directory, args.action, args.port)
        if args.re_type == "post" and "POST":
            post(args.directory, args.action, args.port, ''.join(args.data))
main()