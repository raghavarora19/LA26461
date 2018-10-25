import socket
import argparse

def get(verbose, header, optional, URL):
    geturl = URL.split('/')
    if "127.0.0.1" in URL:
        surl =''.join(geturl)
    elif 'http:' in URL:
        if "localhost" in URL:
            surl = "localhost"
        elif 'www.' in URL:
            surl = geturl[2]
        else:
            surl = 'www.' + geturl[2]
    elif 'http:' and 'www.' and "localhost" not in URL:
        surl = 'www.' + geturl[0]
    else:
        surl = geturl[0]

    getdir = ''
    if len(geturl) > 1:
        if 'http' in URL:
            for i in range(3, len(geturl) - 1):
                getdir += geturl[i] + '/'
        else:
            for i in range(1, len(geturl) - 1):
                getdir += geturl[i] + '/'

        getdir += geturl[len(geturl) - 1]
    request = "GET /" + getdir + " HTTP/1.0\r\nHost: " + surl + "\r\n\r\n"
    # print(request)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((surl, 8083))
    s.sendall(request.encode())
    result = s.recv(1024)
    abc = result.decode()
    body = abc.split('\r\n\r\n')

    if optional:
        f1 = open(optional, "w+")
        f1.write(body[1])
        if verbose:
            print('Output Get with Verbose + Body Output to file ' + optional + ': \n ', body[0])
            exit(0)
        else:
            exit(0)
    #For Verbose
    if verbose == True:
        print('Output Get with Verbose : \n', result.decode())
    else:
        print('Output Get w/o Verbose : \n ', abc)

    s.close()


def post(verbos, header, data, file, optional, URL):

    if (data == None):
        data = ""
    if file:
        f1 = open(file, "r")
        read_file = f1.read()
        body = '' + data + ' ' + read_file + ''
    else:
        body = '' + data + ''

    # for the extraction of the URL for connection
    geturl = URL.split('/')
    if "127.0.0.1" in URL:
        surl =''.join(geturl)
    elif 'http:' in URL:
        if "localhost" in URL:
            surl = "localhost"
        elif 'www.' in URL:
            surl = geturl[2]
        else:
            surl = 'www.' + geturl[2]
    elif 'http:' and 'www.' and "localhost" not in URL:
        surl = 'www.' + geturl[0]
    else:
        surl = geturl[0]

    print(surl)

    host = URL
    port = 80
    head = ""
    for i in header:
        head = head + str(i) + " \r\n"

    lbody = len(body)
    #longurl = '/'.join(surl[1:])

    headers = """\
POST http://""" + URL + """ HTTP/1.1\r
Content-Type: application/json\r
Content-Length: """ + str(lbody) + """\r
Host: """ + URL + """\r
Connection: close\r""" + """\n""" + head + """\r
"""

    body_bytes = body.encode('ascii')
    header_bytes = headers.format(
        content_type="application/json",
        content_length=len(body_bytes),
        host=str(host) + ":" + str(port)
    ).encode('iso-8859-1')

    payload = header_bytes + body_bytes
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((surl, 8083))
    s.sendall(payload)
    payload = s.recv(1024)
    abc = payload.decode()
    body = abc.split('\r\n\r\n')

    if optional:
        f2 = open(optional, "w+")
        f2.write(body[1])
        if verbos:
            print('Output Post with Verbose + Body Output to file ' + optional + ': \n ', body[0])
            exit(0)
        else:
            exit(0)
    if verbos == True:
        print('\rOutput with Verbose:\n', payload.decode())
    else:
        print('\rOutput w/o Verbose:\n', body[0])
    s.close()


def main():
    argParser = argparse.ArgumentParser()

    argParser.add_argument('req_type', type=str, help="GET/POST")
    argParser.add_argument('-v', "--verbose", action='store_true', help="Increase output ")
    argParser.add_argument('-s', '--header', action='append', help="Headers to HTTP Request with the format")
    argParser.add_argument('-d', '--data', action='store', help="An inline data to the body HTTP POST request")
    argParser.add_argument('-f', '--file', action='store', help="Use -f filename")
    argParser.add_argument('-o', '--optional', action='store', help="Write Body of Response to File")
    argParser.add_argument('URL', type=str, help='Enter the URL ')
    args = argParser.parse_args()
    if args.data and args.file:
        print("Request format incorrect use one of -d or -f")
        exit(1)

    # print("Result : ", args.verbose,args.header,args.data,args.file,args.optional,args.URL)
    if args.req_type == 'get' and 'GET':
        if args.header == None:
            nhead = " "
            get(args.verbose, nhead, args.optional, args.URL)
        else:
            get(args.verbose, args.header, args.optional, args.URL)

    elif args.req_type == 'post' and 'POST':
        if args.header == None:
            nhead = " "
            post(args.verbose, nhead, args.data, args.file, args.optional, args.URL)
        else:
            post(args.verbose, args.header, args.data, args.file, args.optional, args.URL)


main()
