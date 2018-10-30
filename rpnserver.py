#!/usr/bin/env python3

import socket
import select
import sys

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)



class ExpHandler:
    def __init__(self, postFix):
        self.postFix =self.parseExp(postFix)

    def parseExp(self, postFix):
        temp = postFix.split(" ")
        return [float(temp[0]), float(temp[1]), temp[2]]

    def eval(self, op1, op2, operator):
        try:
            result = 0.0
            if(operator == '+'):
                result = float(op1+op2)
            elif(operator == "-"):
                result = float(op1-op2)
            elif(operator == "*"):
                result = float(op1*op2)
            elif(operator == "/"):
                result = float(op1/(op2*1.0))
            return result
        except Exception as e:
            return str(e)

    def isOperator(self, s):
        if( s == "+" or s == "-" or s == "*" or s == "/"):
            return True
        return False

    def evalExp(self):
        expSplit = self.postFix
        return self.eval(expSplit[0], expSplit[1], expSplit[2]) 

def processExp(postFixExp):
    expHandler = ExpHandler(postFixExp)
    return str(expHandler.evalExp())

def serverOutput(result):
    return ("Server Received: \"" + result + "\"")

def validatePort(portNumber):
    try:
        return int(portNumber) >= 1024 and int(portNumber) <= 65535
    except:
        return False

def validateCmdLineArgs():
    if(len(sys.argv) != 2):
        return False
    return validatePort(sys.argv[1])

def hostServer():
    if( not validateCmdLineArgs()):
        print("Invalid Command line Arguments, please try again")
        sys.exit(-1)
    try:
        PORT = int(sys.argv[1])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        while(1):
            try:    
                conn, addr = s.accept()
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    postFix = data.decode("utf-8") 
                    print(serverOutput(postFix))
                    result = processExp(postFix)
                    conn.send(result.encode("UTF-8"))
                s.shutdown(socket.SHUT_RDWR)
                s.close()
            except:
                pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    hostServer()

