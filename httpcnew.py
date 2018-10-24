import socket
import argparse

FLAG = 0


def get(verbose, header, optional, URL):
    geturl = URL.split('/')
    surl=''.join(geturl)
    #if 'http:' in URL:
        #if 'www.' in URL:
            #surl = geturl[2]
        #else:
            #surl = 'www.' + geturl[2]
    #elif 'http:' and 'www.' not in URL:
        #surl = 'www.' + geturl[0]
    #else:
        #surl = geturl[0]

    # print(geturl)

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
    s.connect((surl, 80))
    s.sendall(request.encode())
    result = s.recv(1024)
    abc = result.decode()
    body = abc.split('\r\n\r\n')
    global FLAG  # for  accessing global variable
    FLAG += 1
    if FLAG < 6:
        redirectget(body, False, verbose, header, optional, abc)  # call to redirect function
    else:
        print("Exiting Redirection Attempts Failed")
    if optional:
        f1 = open(optional, "w+")
        f1.write(body[1])
        if verbose:
            print('Output Get with Verbose + Body Output to file ' + optional + ': \n ', body[0])
            exit(0)
        else:
            exit(0)
    # For Verbose
    if verbose == True:
        print('Output Get with Verbose : \n', result.decode())
    else:
        print('Output Get w/o Verbose : \n ', body[1])

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

    host = URL
    port = 80
    head = ""
    for i in header:
        head = head + str(i) + " \r\n"

    lbody = len(body)
    surl = URL.split('/')
    shorturl = surl[0]
    longurl = '/'.join(surl[1:])

    headers = """\
POST http://""" + URL + """ HTTP/1.1\r
Content-Type: application/json\r
Content-Length: """ + str(lbody) + """\r
Host: """ + URL + """\r
Connection: close\r""" + """\n""" + head + """\r
"""
    if URL == "www.ptsv2.com/t/raghav/post":
        headers = """\
POST /""" + longurl + """ HTTP/1.1\r
Content-Type: application/json\r
Content-Length: """ + str(lbody) + """\r
Host: """ + shorturl + """\r
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
    s.connect((shorturl, 80))
    s.sendall(payload)
    payload = s.recv(1024)
    abc = payload.decode()
    body = abc.split('\r\n\r\n')
    global FLAG  # for  accessing global variable
    FLAG += 1
    if FLAG < 6:
        redirectput(body, True, verbos, header, data, file, optional, abc)  # For Redirection
    else:
        print("Exiting Redirection Attempts Failed")
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
        print('\rOutput w/o Verbose:\n', body[1])
    s.close()


def redirectget(payload, reqtype, verbose, header, optional, d_response):
    stat = payload[0].splitlines()
    status = stat[0].split()
    status_code = status[1]
    global FLAG
    if (FLAG == 1):
        print(payload[0])
    # print(int(status_code))
    if (int(status_code) >= 300) & (int(status_code) < 400):  # TEST WITH URL www.amazon.org
        if reqtype == False:
            print("You are being Redirected:", status_code)
            if d_response.find('Location:'):
                # Splitting Response
                split = d_response.splitlines()
                res = [i for i in split if 'Location:' in i]
                reurl = res[0].split(': ')
                result = reurl[1].split('/')
                finalreurl = [i for i in result if 'www.' in i]
                get(verbose, header, optional, finalreurl[0])
                exit(0)
            else:
                exit(1)


def redirectput(payload, reqtype, verbose, header, data, file, optional, d_response):
    stat = payload[0].splitlines()
    status = stat[0].split()
    status_code = status[1]
    global FLAG
    if (FLAG == 1):
        print(payload[0])
    if (int(status_code) >= 300) & (int(status_code) < 400):  # test with amazon.org|amazon.org/post
        if reqtype == True:
            print("You have been Redirected: ", status_code)
            if d_response.find('Location:'):
                # Split Payload
                split = d_response.splitlines()
                res = [i for i in split if 'Location:' in i]
                reurl = res[0].split(': ')
                result = reurl[1].split('/')
                finalreurl = [i for i in result if 'www.' in i]
                post(verbose, header, data, file, optional, finalreurl[0])
                exit(0)
            else:
                exit(1)


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
