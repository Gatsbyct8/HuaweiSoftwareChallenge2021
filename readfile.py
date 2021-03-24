'''
class 

class Server():
    def __init__(self,N = 0, ):
        self.N = 0
        self.server = []
        self.M = 0
        self.virtual = []
'''
def readFile(filepath):
    f = open(filepath,'r')
    inputList = f.read().splitlines()
    f.close()
    return inputList

def input2format(inputList):
    N = int(inputList[0])
    server = inputList[1:N+1]
    M = int(inputList[N+1])
    virtualMachine = inputList[N+2:M+N+2]
    T = int(inputList[M+N+2])
    request = []
    index = M+N+3
    while index < len(inputList):
        R = int(inputList[index])
        requestDay = inputList[index+1:index+R+1]
        request.append([R,requestDay])
        index = index + R + 1
    return N, server, M, virtualMachine, T, request

if __name__ == '__main__':
    filepath = 'training-1.txt'
    inputList = readFile(filepath)
    N, server, M, virtualMachine, T, request = input2format(inputList)
    print(request[0])
    
    
