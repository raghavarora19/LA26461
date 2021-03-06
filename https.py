import socket
import datetime
import json


def createServer():
    servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servsock.bind(("127.0.0.1", 8083))
    servsock.listen(5)
    while (True):
        (csock, address) = servsock.accept()
        data_recv = csock.recv(1024)
        decode_data = data_recv.decode()
        time = datetime.datetime.now()
        output = ""

        if "GET" in decode_data:

            fragment = decode_data.split('\r\n')
            getheader = fragment[2:]
            arg = fragment[0].split(' ')
            newg_header = []
            for i in range(0, len(getheader)-1):
                newg_header.append('\t"' + getheader[i] + '"')
            get_header = "\n".join(newg_header)
            getoutput = """
HTTP/1.1 200 OK
Server: gunicorn/19.9.0 
http://localhost
Connection: close
Content-length: """+ str(len(decode_data))+"""""
Content-type: application/json
date:""" + str(time) + """
via: 1.1 vegur \r\n\r\n
{
  "args": {"""+arg[1]+"""},
  "headers": {
  """ + get_header + """ 
       }
"json": null,
"origin": "127.0.0.1",
"url": "http://localhost"
}"""
            csock.sendall(getoutput.encode())

        elif "POST" in decode_data:
            frag = decode_data.split('\n\n')
            header = frag[0]
            head = frag[1]
            inline_file = frag[2]
            inl_file = json.dumps(inline_file)

            # Header Conversion
            head = head.replace(':', "\r\n")
            head_new = head.split("\r\n")
            head_new = head_new[1:len(head_new) - 1]
            new_header = []
            for i in range(0, len(head_new) - 1, 2):
                new_header.append('\t"' + head_new[i] + '"' + ":" + '"' + head_new[i + 1] + '"')
            head = "\n".join(new_header)
            output = """
HTTP/1.1 200 OK
Server: gunicorn/19.9.0 
http://localhost
Connection: close
Content-length:""" +str(len(decode_data))+"""
Content-type: application/json
date:""" + str(time) + """
via: 1.1 vegur \r\n\r\n
 {
  "args": {},
  "data":""" + inl_file + """, 
  "files": {},
  "form": {},
  "headers": {
  """ + head + """ 
 }
"json": null,
"origin": "127.0.0.1",
"url": "http://localhost"
}"""
            csock.sendall(output.encode("utf-8"))

        csock.shutdown(socket.SHUT_WR)
        csock.close()

    servsock.close()


createServer()
