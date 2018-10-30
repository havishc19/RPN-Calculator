#!/usr/bin/python

import socket
import sys

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023), port number defaulted to 65432



class ExpHandler:
    def __init__(self, postFix):
        self.postFix =self.parseExp(postFix)

    def parseExp(self, postFix):
        #Splits the given expression into its individual constituents
        temp = postFix.split(" ")
        return [float(temp[0]), float(temp[1]), temp[2]]

    def eval(self, op1, op2, operator):
        #eval() evaluates and returns the result of the expression
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
        #calls the eval() function with parameters submitted in the right order. 
        expSplit = self.postFix
        return self.eval(expSplit[0], expSplit[1], expSplit[2]) 

def processExp(postFixExp):
    #processExp initalizes the class ExpHandler to process the given PostFix Exp
    #ExpHandler has the necessary methods to parse and evaluate the PostFix Exp
    try:
        expHandler = ExpHandler(postFixExp)
        return str(expHandler.evalExp())
    except Exception as e:
        return str(e)

def serverOutput(result):
    return ("Server Received: \"" + result + "\"")

def validatePort(portNumber):
    #Checks if the given port number is a valid integer and lies in the zone of non-privileged ports 
    try:
        return int(portNumber) >= 1024 and int(portNumber) <= 65535
    except:
        return False

def validateCmdLineArgs():
    #validates the length of the cmd line args and the port number
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
                # print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print("\n")
                        break
                    postFix = data.decode("utf-8") 
                    print(serverOutput(postFix))
                    result = processExp(postFix)
                    conn.send(result.encode("UTF-8"))
            except:
                pass
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    #hostServer() method is used to host the server after doing the required validations
    hostServer()

