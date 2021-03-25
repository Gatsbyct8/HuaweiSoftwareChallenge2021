from Command import Command
from VirtualMachine import VirtualMachine
from Server import Server

def readFile(filepath):
    f = open(filepath,'r')
    inputList = f.read().splitlines()
    f.close()
    return inputList

def input2format(inputList):
    N = int(inputList[0])
    #server = inputList[1:N+1]
    ServerList = [] #存储服务器信息
    for i in range(1,N+1):
        snew = inputList[i].replace(" ","")
        snew = snew[1:-1]
        s = snew.split(',')
        serv = Server(s[0],int(s[1]),int(s[2]),int(s[3]),int(s[4]))
        ServerList.append(serv)

    M = int(inputList[N+1])
    #virtualMachine = inputList[N+2:M+N+2]
    VMList = {} #存储虚拟机信息
    for i in range(N+2,M+N+2):
        snew = inputList[i].replace(" ","")
        snew = snew[1:-1]
        s = snew.split(',')
        vm = VirtualMachine(s[0],int(s[1]),int(s[2]),int(s[3]))
        VMList[vm.vmType] = vm

    T = int(inputList[M+N+2])
    request = []
    index = M+N+3
    day = 0
    CommandList = []  #存储T天的命令信息 
    CommandDayList = []
    while index < len(inputList):
        R = int(inputList[index])
        #requestDay = inputList[index+1:index+R+1]
        CommandDayList = []
        for i in range(index+1, index+R+1):
            snew = inputList[i].replace(" ","")
            snew = snew[1:-1]
            s = snew.split(',')
            if len(s) == 2:
                command = Command(s[0],"",int(s[1]))
            else:
                command = Command(s[0],s[1],int(s[2]))
            CommandDayList.append(command)
        CommandList.append(CommandDayList)
        #request.append([R,requestDay])
        index = index + R + 1
    return ServerList, VMList, CommandList # 返回服务器、虚拟机、命令信息

def input2formatstd():
    N = int(input())
    #server = inputList[1:N+1]
    ServerList = [] #存储服务器信息
    for i in range(0,N):
        snew = input()
        snew = snew.replace(" ","")
        snew = snew[1:-1]
        s = snew.split(',')
        serv = Server(s[0],int(s[1]),int(s[2]),int(s[3]),int(s[4]))
        ServerList.append(serv)

    M = int(input())
    #virtualMachine = inputList[N+2:M+N+2]
    VMList = {} #存储虚拟机信息
    for i in range(N+2,M+N+2):
        snew = input()
        snew = snew.replace(" ","")
        snew = snew[1:-1]
        s = snew.split(',')
        vm = VirtualMachine(s[0],int(s[1]),int(s[2]),int(s[3]))
        VMList[vm.vmType] = vm

    T = int(input())
    request = []
    day = 0
    CommandList = []  #存储T天的命令信息 
    CommandDayList = []
    while day < T:
        R = int(input())
        #requestDay = inputList[index+1:index+R+1]
        CommandDayList = []
        for i in range(0, R):
            snew = input()
            snew = snew.replace(" ","")
            snew = snew[1:-1]
            s = snew.split(',')
            if len(s) == 2:
                command = Command(s[0],"",int(s[1]))
            else:
                command = Command(s[0],s[1],int(s[2]))
            CommandDayList.append(command)
        CommandList.append(CommandDayList)
        #request.append([R,requestDay])
        day += 1
    return ServerList, VMList, CommandList # 返回服务器、虚拟机、命令信息
    
if __name__ == '__main__':
    #filepath = 'training-1.txt'
    #inputList = readFile(filepath)
    ServerList, VMList, CommandList = input2formatstd()
    print(ServerList[0].stype)
    
    
