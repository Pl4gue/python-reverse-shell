import socket
import sys


# create socket

def socket_create(phost, pport):
    try:
        global host
        global port
        global s
        host = phost
        port = pport
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + "\n" + str(msg))


# bind socket to port and wait for connection from client

def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + "\n" + str(msg) + "\nRetrying...")
        tries = 1
        maxtries = 5
        while tries <= maxtries:
            try:
                s.bind((host, port))
                s.listen(5)  # maximum number of connections in queue
            except socket.error as msg:
                print("Retry {0} failed: ".format(tries) + str(msg))  # TODO: replace {0} -> DONE
                tries += 1
                continue
            print("Successfully bound socket to port: " + str(port))
            break


# establish a connection with client -socket must be listening!

def socket_accept():
    # conn is a new socket object usable to send and receive data on the
    # connection
    conn, address = s.accept()
    print("Connection has been established | " +
          "[IP/Port] " + address[0] + "/" + str(address[1]))
    send_commands(conn, address)
    conn.close()


# send commands

def send_commands(conn, address):
    while 1:
        cmd = input()
        if cmd == 'quit':
            print("Bye!")
            s.close()
            sys.exit()
        if cmd == '':
            continue
        conn.send(str.encode(cmd))
        client_response = conn.recv(8192)
        if str(client_response[:1], "utf-8") == '/' \
                or str(client_response[:1], "utf-8") == '#':  # valid response ('/') or error response ('#')
            print(str(client_response[1:], "utf-8"))
        else:
            print("Connection has disconnected: " +
                  "[IP/Port] " + address[0] + "/" + str(address[1]))


def run(run_host, run_port):
    socket_create(run_host, run_port)
    socket_bind()
    socket_accept()


run('localhost', 9282)
