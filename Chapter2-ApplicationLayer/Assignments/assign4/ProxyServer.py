#!/usr/bin/python

import io, os, socket, ssl

def get_start_fields(start_line):
    return tuple(start_line.decode('ASCII').split(' '))

def get_hostname_from_url(url):
    protocol, sep, rest_url = url.partition('://')
    hostname, sep, rest_url = rest_url.partition('/')
    return hostname

def get_protocol_from_url(url):
    protocol, sep, rest_url = url.partition('://')
    return protocol


def get_header_fields(header_lines):
    header_fields = {}
    rest_lines = header_lines.decode('ASCII')
    while len(rest_lines) > 0:
        current_line, sep, rest_lines = rest_lines.partition('\r\n')
        name, sep, value = current_line.partition(': ')
        header_fields[name] = value

    return header_fields


def separate_http_message(message):
    start_line, sep, rest_message = message.partition(b'\r\n')
    header_lines, sep, body = rest_message.partition(b'\r\n\r\n')
    header_lines += b'\r\n'

    return start_line, header_lines, body

def create_to_server_socket(server_name, server_port):
    server_sock = None
    if server_port == 80:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.connect((server_name, server_port))
    else:
        sslContext = ssl.create_default_context()
        server_sock = sslContext.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=server_name)
        server_sock.connect((server_name, server_port))

    return server_sock
        
def do_proxy(client_sock, pid):
    # get the request from the client
    request = client_sock.recv(4096)

    # get request line, header lines and entity body
    request_line, header_lines, body = separate_http_message(request)
    
    # get header fields dictionary
    header_fields = get_header_fields(header_lines)

    # remove Connection and Proxy-Connection from header fields
    if 'Connection' in header_fields:
        del header_fields['Connection']
    if 'Proxy-Connection' in header_fields:
        del header_fields['Proxy-Connection']

    # connect to the server
    server_name = header_fields['Host'] if 'Host' in header_fields else\
            get_hostname_from_url(get_start_fields(request_line)[1])
    server_name = server_name.split(':')[0]
    protocol = get_protocol_from_url(get_start_fields(request_line)[1])
    server_port = 80 if protocol == 'http' else 443


    print '------------ Debug info -----------------'
    print 'request_line:', request_line
    print 'start fields:', get_start_fields(request_line)
    print 'server_name:', server_name
    print 'after split??:', server_name.split(':')[0]
    print 'protocol:', protocol
    print 'server_port:', server_port
    print '========================================='


    print('---Connect to the server %s, pid=%d' % (server_name, pid))
    server_sock = create_to_server_socket(server_name, server_port)

    # send the new request, assuming that the whole request is less than 4096 bytes
    print('---Send the new request to the server, pid = %d' % pid)
    new_header_lines = ''
    for header_name in iter(header_fields):
        new_header_lines += '%s: %s\r\n' % (header_name, header_fields[header_name])
    server_sock.send(request_line + b'\r\n' + new_header_lines.encode('ASCII') + b'\r\n' + body)

    # get and send back the response 
    print('---Send the response back to the client, pid=%d' % pid)
    response = server_sock.recv(4096)
    while len(response) > 0:
        client_sock.send(response)
        response = server_sock.recv(4096)

    # close server socket
    print('--- Close server socket, pid=%d' %pid)
    server_sock.close()


if __name__ == '__main__':

    # initialize the socket as a server
    proxy_ip = ''
    proxy_port = 8003
    proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_sock.bind((proxy_ip, proxy_port))
    proxy_sock.listen(5)

    parent_pid = os.getpid()

    # infinite loop waiting for and processing requests
    while 1:
        client_sock, client_address = proxy_sock.accept()
        print('---Request comes, IP = ' + str(client_address[0]))

        # process the request in the subprocess
        if os.fork() == 0:
            pid = os.getpid()
            print('--- Process teh request in a subprocess, pid = %d' % pid)

            print('--- Close proxy socket in the subprocess, pid= %d' % pid)
            proxy_sock.close()

            do_proxy(client_sock, pid)

            print('---Close the Client socket in the subprocess, pid = %d' % pid)
            client_sock.close()

            print('---Subprocess exists, pid = %d' %pid)
            exit()

        print('---Close the client socket in the parent process')
        client_sock.close()
