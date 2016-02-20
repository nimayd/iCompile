#!/usr/bin/python

import subprocess
import os
import socket

def runCode(codeString):
    header = "#include <stdlib.h>\n#include <stdio.h>\n"
    program = open("program.c", "w+")
    program.write(header)
    program.write(codeString)

    program.close()
    subprocess.call(["gcc", "program.c", "-o",  "program"])
    subprocess.call(["./program"])

def main():
    f = open("lol.txt", "r+")
    str = f.read()
#    print str
    print "WTF"
    runCode(str)

if __name__ == "__main__":
    main()


def runServer():
    host = "130.126.255.67"
    port = 3000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(host, port)
    server.listen(1)

    with open("code.jpg", "wb") as img:
        while True:
            conn, addr = server.accept()
            data = conn.recv(1024)
            if not data:
                break
            img.write(data)
            print data


        conn.close()
