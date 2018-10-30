#!/usr/bin/env python3

import socket
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

class ExpHandler:
	def __init__(self, postFix):
		self.postFix = postFix
		self.operandStack = []
		self.expPointer = 0
		self.exp = []
		self.lastExpReq = False

	def checkOperator(self, val):
		if(len(val) == 1 and (val == "+" or val == "*" or val == "-" or val == "/")):
			return True
		return False

	def checkNum(self, val):
		try:
			temp = float(val)
			return True
		except:
			return False

	def checkDelimiter(self):
		expSplit = self.postFix.split(" ")
		for val in expSplit:
			if(len(val) == 0):
				continue
			elif(self.checkNum(val) or self.checkOperator(val)):
				continue
			else:
				return False
		self.exp = self.postFix.split(" ")
		self.exp = list(filter(None, self.exp))
		return True

	def isPostFixValid(self):
		operandStack = []
		for val in self.exp:
			if(self.checkNum(val)):
				operandStack.append(1)
			elif(self.checkOperator(val)):
				if(len(operandStack) >= 2):
					operandStack.pop();operandStack.pop();
					operandStack.append(1)
				else:
					return False
			else:
				return False
		if(len(operandStack) != 1):
			return False
		return True

	def validateExpression(self):
		#only space delimiter allowed
		checkDelimiter = self.checkDelimiter()
		checkExpFormat = self.isPostFixValid()
		# print(self.postFix, checkDelimiter, checkExpFormat)
		return checkDelimiter and len(self.exp) >= 3 and checkExpFormat

	def hasNext(self):
		return self.expPointer < len(self.exp)

	def next(self):
		i = self.expPointer
		while( i < len(self.exp) ):
			val = self.exp[i]
			if(self.checkNum(val)):
				self.operandStack.append(val)
			else:
				operand2 = self.operandStack[-1]; self.operandStack.pop()
				operand1 = self.operandStack[-1]; self.operandStack.pop()
				self.expPointer = i + 1
				if(self.expPointer == len(self.exp) ):
					self.lastExpReq = True
				return operand1 + " " + operand2 + " " + val
			i = i + 1

	def pushResult(self, operand):
		self.operandStack.append(operand)

def clientOutput(result, final):
    return ("Client Received %s: %s" %(final,result))

def sendServer(expHandler):
	while(expHandler.hasNext()):
    		currExp = expHandler.next()
    		s.send(currExp.encode("utf-8"))
    		data = s.recv(1024)
    		data = data.decode("utf-8")
    		if(expHandler.lastExpReq):
    			print(clientOutput(data, "Final"))
    		else:
    			print(clientOutput(data, ""))

    		if( not expHandler.checkNum(data)):
    			print("Server faced error while processing, terminating current expression execution..")
    			break
    		expHandler.pushResult(data)

def validatePort(portNumber):
    try:
        return int(portNumber) >= 1024 and int(portNumber) <= 65535
    except:
        return False

def validateCmdLineArgs():
    if(len(sys.argv) != 3):
        return False
    return validatePort(sys.argv[1])


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def launchClient():
	if(not validateCmdLineArgs()):
		print("Invalid Command line Arguments, please try again")
		sys.exit(-1)
	try:
		PORT = int(sys.argv[1])
		s.connect((HOST, PORT))
		postFix = sys.argv[2]
		expHandler = ExpHandler(postFix)
		if(not expHandler.validateExpression()):
			print("Postfix Expression format incorrect, try again!")
			sys.exit(-1)
		sendServer(expHandler)
		s.close()
	except Exception as e:
		print(e)



if __name__ == '__main__':
    launchClient()