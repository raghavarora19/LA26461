import socket
import os
import argparse
import json
import sys
import threading

sys.path.extend(["./"])

def server(host, port, dir):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(10)
    while True:
        (csock, address) = sock.accept()
        threading.Thread(target=requesthandler(), args=(csock, address, dir)).start()
        #csock.shutdown(socket.SHUT_WR)
    sock.close()

def statuscode(statuscode, message,content):

    header = "HTTP /1.0 " + statuscode + " " + message + " "+ content + " "
    return header



def requesthandler(csock, address,dir):
    if args.debug:
        print("Handles Client:",address)
        while True:
             data_recv = csock.recvall()
             decode_data = data_recv.decode("utf-8")
             if not decode_data:
                break
             data = decode_data.split('\r\n')
             rtype= data[0]
             path = data[1]
             if 'POST' in decode_data:
                 in_data = data[3]
             if '..' in path:
                 if args.debug:
                     print("Access Denied",path)
                 header_to_return = statuscode(400,'Access Denied','')
             else :
                 if not dir.endswith("/"):
                     dir = dir + "/"
                 path = (dir + path).replace("//","/")
             if rtype =="GET":
                if path.endswith("/"):
                  if args.debug:
                   print("GET REQUEST ->DIRECTORY:",path)
                   file =os.listdir(path)
                   header_to_return = statuscode(200,json.dumps(files).encode("ascii"),"Content-Type: application/json")
                  else :
                    if os.path.exists(path):
                     if args.debug:
                      print("File",path)
                      header_to_return = statuscode(200,'','')
                      type = magic.from_file(path, mime=True)
                      header_to_return = statuscode(200,'','')
                     if "text" in type:
                      with open(path,'r') as f1:
                      file_content = f1.read()
                      header_to_return += json.dumps("Content-Length"+str(len(file_content))) + "\r \n"
                      header_to_return += file_content +"\r\n"
                      else :
                       with open(path, 'rb') as f1:
                       file_content = f1.read()
                       header_to_return += json.dumps("Content-Length" + str(len(file_content))) + "\r \n"
                       header_to_return += file_content + "\r\n"

                        #if "Content-Disposition" in decode_data:
                        #header_to_return +=  "Content-Disposition"
                        #elif "inline" in query:

                  else :
                   header_to_return = statuscode(404,"".encode("ascii"),"")

                    except: OSError as e:
                            if args.debug:
                                print(e)
                            header_to_return = http(400, e.strerror)















parse = argparse.ArgumentParser(description='HTTP FILE SERVER')
parse.add_argument("-p", action="store", dest="port", help="Set server port", type=int, default=8080)
parse.add_argument("-d", action="store", dest="directory", help="Set directory path", default='./')
parse.add_argument('-v', "--debug", dest="debug", action='store_true', default=False,help="Prints Debugging Messages")
args = parse.parse_args()
server('127.0.0.1', args.port, args.directory)


