import pathlib
import socket
import os
import argparse
import json
import sys
import threading
import magic
from lockfile import LockFile

sys.path.extend(["./"])


def server(host, port, dir):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        sock.listen(10)
        while True:
            (csock, address) = sock.accept()
            threading.Thread(target=requesthandler, args=(csock, address, dir)).start()
            requesthandler(csock,address,dir)

            # csock.shutdown(socket.SHUT_WR)
    finally:
        sock.close()


def statuscode(statuscode, message, content):
    header = "HTTP /1.0 " + str(statuscode) + "\r\n" + str(message) + "\r\n" + str(content) + ""
    return header


def requesthandler(csock, address, dir):
    if args.debug:
        print("Handles Client:", address)
    try:
        while True:
            data_recv = csock.recv(8096)
            decode_data = data_recv.decode("utf-8")
            if not decode_data:
                break
            data = decode_data.split('\r\n')
            rtype = data[0]
            path = data[1]

            if '..' in path:
                if args.debug:
                    print("Access Denied", path)
                    header_to_return = statuscode(400, 'Access Denied', '')

            else:
                if not dir.endswith("/"):
                    dir = dir + "/"
                    path = (dir + path).replace("//", "/")
                if "GET" in rtype:
                    try:
                        if path.endswith("/"):
                            if args.debug:
                                print("GET REQUEST ->DIRECTORY:", path)
                            file = os.listdir(path)
                            header_to_return = statuscode(200, json.dumps(file).encode("utf-8"),
                                                          "Content-Type: application/json")
                        else:
                            if os.path.exists(path):
                                if args.debug:
                                    print("File", path)
                                type = magic.from_file(path, mime=True)
                                typ = json.dumps("Content-Type:" + type + "")
                                header_to_return = statuscode(200, '', typ)
                                if "text" in type:
                                    with open(path, 'r') as f1:
                                        file_content = f1.read()
                                        header_to_return += json.dumps(
                                            "Content-Length" + str(len(file_content))) + "\r\n"
                                        header_to_return += str(file_content) + "\r\n"
                                else:
                                    with open(path, 'rb') as f1:
                                        file_content = f1.read()
                                        header_to_return += json.dumps(
                                            "Content-Length" + str(len(file_content))) + "\r\n"
                                        header_to_return += str(file_content) + "\r\n"

                                # if "Content-Disposition" in decode_data:
                                # header_to_return +=  "Content-Disposition"
                                # elif "inline" in query:

                            else:
                                header_to_return = statuscode(404, "".encode("utf-8"), "")
                    except OSError as err:
                        if args.debug:
                            print(err)
                        header_to_return = statuscode(400, "Bad Request Error", "")

                elif "POST" in rtype:
                    try:
                        in_data=data[2]
                        if args.debug:
                            print("POSTing File", path)
                        pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
                        filelock = LockFile(path)
                        filelock.acquire()
                        print(os.path.basename(path), "Content", in_data)
                        with open(path, 'a+') as file:
                            file.write(in_data + "\n")
                        filelock.release()
                        header_to_return = statuscode(200,"".encode("utf-8"), "")

                    except OSError as err:
                        if args.debug:
                            print(err)
                        header_to_return = statuscode(400, "Bad Request")
                else:
                    header_to_return = statuscode(400, "", "")

            if args.debug:
                print(header_to_return)
            csock.sendall(header_to_return.encode("utf-8"))

    finally:
        csock.close()


parse = argparse.ArgumentParser(description='HTTP FILE SERVER')
parse.add_argument("-p", action="store", dest="port", help="Set server port", type=int, default=8080)
parse.add_argument("-d", action="store", dest="directory", help="Set directory path", default='./')
parse.add_argument('-v', "--debug", action='store_true', default=False, help="Prints Debugging Messages")
args = parse.parse_args()
server("127.0.0.1", args.port, args.directory)
