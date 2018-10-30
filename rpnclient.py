#!/usr/bin/python

import socket
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server, defaulted to 65432

class ExpHandler:
	def __init__(self, postFix):
		self.postFix = postFix
		self.operandStack = [] # Used by the client to maintain the state of Postfix expression evaluation
		self.expPointer = 0 # Pointer to the expression, helps in the sequential evaluation of the expression
		self.exp = []
		self.lastExpReq = False #Flag used by the program to know if the request being sent is the last or not.

	def checkOperator(self, val):
		#check if the operator is valid or not
		if(len(val) == 1 and (val == "+" or val == "*" or val == "-" or val == "/")):
			return True
		return False

	def checkNum(self, val):
		#check if an operand if a valid int/float
		try:
			temp = float(val)
			return True
		except:
			return False

	def checkDelimiter(self):
		#splits the given expression with " ", and validates the correctness of operators and operands in it. 
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
		#Checks if the given expression is in a valid reverse polish notation or not
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
		#only space delimiter allowed, validates the given postfix expression
		checkDelimiter = self.checkDelimiter()
		checkExpFormat = self.isPostFixValid()
		# print(self.postFix, checkDelimiter, checkExpFormat)
		return checkDelimiter and len(self.exp) >= 3 and checkExpFormat

	def hasNext(self):
		#hasNext() method tells if there still a chunk (Op1 Op2 Operator) in the expression yet to be processed. 
		#In other words, it tells the program when to stop the execution of the given Postfix expression
		return self.expPointer < len(self.exp)

	def next(self):
		#next returns the next request to be dispatched to the server in the format "Op1 Op2 Operator"
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
		#Pushes the result from the server into the operand stack, helps in the correct evaluation of the expression
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
	#Validates if the given port number is an integer and lies in the zone of non-privileged ports
    try:
        return int(portNumber) >= 1024 and int(portNumber) <= 65535
    except:
        return False

def validateCmdLineArgs():
	#Validates the length of cmd line args and validates the port number as well.
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
		#ExpHandler provides routines to split, validate and dispatch the given Postfix expression in chunks
		expHandler = ExpHandler(postFix)
		if(not expHandler.validateExpression()):
			#If the given Postfix expression is wrong, the client is terminated
			print("Postfix Expression format incorrect, try again!")
			sys.exit(-1)
		#sendServer() function handles the job of sending requests to the server in chunks
		sendServer(expHandler)
		s.close()
	except Exception as e:
		print(e)



if __name__ == '__main__':
	# Launches Client: Connects socket to Server on a given Port number and sends out requests in chunks to evaluate the given Postfix expression
    launchClient()