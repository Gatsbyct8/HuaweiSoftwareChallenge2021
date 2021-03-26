from readfile import readFile, input2format , input2formatstd
import copy
import sys
import time

class Optimization:
    def __init__(self,ServerList, VMList, CommandList):
        self.ServerList = ServerList
        self.VMList = VMList
        self.CommandList = CommandList
        self.alreadyBuyServerInfo = {}  #已经买了的服务器 <id,server>
        self.vmID2vmType = {}  # 虚拟机ID对虚拟机型号 <vmid, vmtype>
        self.vmID2sid = {}  #虚拟机ID与服务器ID <vmid, serverid>
        self.vmID2End = {}  #虚拟机部署的对应表  <vmid, 1/2>
    
    def optimization(self):
        cnt = 0
        res = []
        days = len(CommandList)
        #start = time.time()
        for i in range(days):
            numsBuyToday = {}  #每天购买 <stype, nums>
            buyHashToday = {}  #申请编号和当天服务器编号 <id, sid>
            buyOrderToday = []  #当天买的服务器 在ServerList中的第几个型号
            tempRes = []
            buyCntToday = 0
            # 扫描第i天的所有请求
            for j in range(len(CommandList[i])):
                tempCommand = CommandList[i][j]
                
                # add
                if tempCommand.commandType == 'add':
                    
                    self.vmID2vmType[tempCommand.vmId] = tempCommand.vmType #建立 虚拟机节点和型号对应 <vmid, vmType>
                    bothFlag = VMList[tempCommand.vmType].deploy #按该虚拟机节点部署
                    cpuCore = VMList[tempCommand.vmType].cpuCore
                    ram = VMList[tempCommand.vmType].ram
                    halfcpuCore = int(cpuCore / 2)
                    halfram = int(ram / 2)
                    #print(cpuCore)

                    availableFlag = False  #判断是否在已有服务器能部署的下
                    if bothFlag == 1:  #A,B双节点部署
                        for key,value in self.alreadyBuyServerInfo.items(): #获取服务器ID,服务器参数
                            # 如果空间足够，能够部署
                            if value.availableCpuCoreA >= halfcpuCore and value.availableRamA >= halfram \
                                and value.availableCpuCoreB >= halfcpuCore and value.availableRamB >= halfram:
                                tempStr = '(' + str(key) + ')\n'
                                tempRes.append(tempStr)
                                value.availableCpuCoreA -= halfcpuCore
                                value.availableRamA -= halfram
                                value.availableCpuCoreB -= halfcpuCore
                                value.availableRamB -= halfram
                                #print("S:",key)
                                #print("CpuAchanged:",value.availableCpuCoreA)
                                #print("ramAchanged:",value.availableRamA)
                                #print("CpuBchanged:",value.availableCpuCoreB)
                                #print("ramBchanged:",value.availableRamB)
                                #print("----------------------")
                                availableFlag = True
                                self.vmID2sid[tempCommand.vmId] = key
                                break
                        #不要购买，直接申请
                        if availableFlag:
                            continue
                        #服务器空间不足，需要购买
                        #查询服务器产品列表
                        # flag = False
                        for k in range(len(ServerList)):
                            server = ServerList[k]
                            #如果当前服务器满足
                            if server.availableCpuCoreA >= halfcpuCore and server.availableRamA >= halfram \
                                and server.availableCpuCoreB >= halfcpuCore  and server.availableRamB >= halfram:
                                buyCntToday += 1 #当天购买数量加1
                                # 当前cnt为空余id，给买的server
                                self.alreadyBuyServerInfo[cnt] = copy.deepcopy(server)     # <id, server>
                                self.alreadyBuyServerInfo[cnt].availableCpuCoreA -= halfcpuCore
                                self.alreadyBuyServerInfo[cnt].availableRamA -= halfram
                                self.alreadyBuyServerInfo[cnt].availableCpuCoreB -= halfcpuCore
                                self.alreadyBuyServerInfo[cnt].availableRamB -= halfram
                                #print("S:",cnt)
                                #print("AB:A",self.alreadyBuyServerInfo[cnt].availableCpuCoreA)
                                #print("AB:A",self.alreadyBuyServerInfo[cnt].availableRamA)
                                #print("AB:B",self.alreadyBuyServerInfo[cnt].availableCpuCoreB)
                                #print("AB:B",self.alreadyBuyServerInfo[cnt].availableRamB)
                                #print("----------------------")
                                buyHashToday[cnt] = k
                                if k not in buyOrderToday:
                                    buyOrderToday.append(k)
                                    exceedResourceFlag = False
                                if not numsBuyToday.get(k): 
                                    numsBuyToday[k] = 0
                                numsBuyToday[k] += 1
                                tempStr = '(' + str(cnt) + ')\n'
                                tempRes.append(tempStr)
                                self.vmID2sid[tempCommand.vmId] = cnt 
                                cnt += 1 #当前服务器ID增加1，给之后新的服务器 
                                break
                    #单节点部署
                    else:
                        for key,value in self.alreadyBuyServerInfo.items():
                            # 如果A节点有空间
                            if value.availableCpuCoreA >= cpuCore and value.availableRamA >= ram :
                                tempStr = '(' + str(key) + ", A)\n"
                                tempRes.append(tempStr)
                                value.availableCpuCoreA -= cpuCore
                                value.availableRamA -= ram
                                #print("S:",key)
                                #print("CpuAchanged:",value.availableCpuCoreA)
                                #print("ramAchanged:",value.availableRamA)
                                #print("----------------------")
                                availableFlag = True # 能够部署，不需要购买
                                self.vmID2End[tempCommand.vmId] = 1  #虚拟机部署在A节点  <vmID, 1>
                                self.vmID2sid[tempCommand.vmId] = key
                                break
                            elif value.availableCpuCoreB >= cpuCore and value.availableRamB >= ram :
                                tempStr = '(' + str(key) + ", B)\n"
                                tempRes.append(tempStr)
                                value.availableCpuCoreB -= cpuCore
                                value.availableRamB -= ram
                                #print("S:",key)
                                #print("CpuBchanged:",value.availableCpuCoreB)
                                #print("ramBchanged:",value.availableRamB)
                                #print("----------------------")
                                availableFlag = True # 能够部署，不需要购买
                                self.vmID2End[tempCommand.vmId] = 2  #虚拟机部署在B节点  <vmID, 2>
                                self.vmID2sid[tempCommand.vmId] = key
                                break
                        if availableFlag:
                            continue #填充进A节点 不进行后续操作
                        for k in range(len(ServerList)):
                            #买一个服务器，默认放在A节点
                            if ServerList[k].availableCpuCoreA >= cpuCore and ServerList[k].availableRamA >= ram:
                                buyCntToday += 1 #当天购买数量+1
                                self.alreadyBuyServerInfo[cnt] = copy.deepcopy(ServerList[k])
                                self.alreadyBuyServerInfo[cnt].availableCpuCoreA -= cpuCore
                                self.alreadyBuyServerInfo[cnt].availableRamA -= ram
                                #print("S:",cnt)
                                #print("AB:",self.alreadyBuyServerInfo[cnt].availableCpuCoreA)
                                #print("AB:",self.alreadyBuyServerInfo[cnt].availableRamA)
                                #print("----------------------")
                                buyHashToday[cnt] = k #购买的服务器id 对应 第k个服务型号
                                if k not in buyOrderToday:
                                    buyOrderToday.append(k)
                                    exceedResourceFlag = False
                                if not numsBuyToday.get(k): #第k个型号的服务器没有买
                                    numsBuyToday[k] = 0 #初始化
                                numsBuyToday[k] += 1
                                tempStr = '(' + str(cnt) + ", A)\n"
                                tempRes.append(tempStr)
                                self.vmID2End[tempCommand.vmId] = 1
                                self.vmID2sid[tempCommand.vmId] = cnt
                                cnt += 1
                                break
                    if exceedResourceFlag:
                        return 0 #单双部署如果都不行，直接返回0
                # 'del'操作
                else:     
                    delVmId = tempCommand.vmId
                    serverId = self.vmID2sid[delVmId]
                    # 对应服务器ID资源恢复
                    tempVmInfo = self.VMList[self.vmID2vmType[delVmId]]
                    temphalfcpuCore = tempVmInfo.cpuCore / 2
                    temphalfram = tempVmInfo.ram / 2
                    # 双节点删除操作
                    if tempVmInfo.deploy:
                        self.alreadyBuyServerInfo[serverId].availableCpuCoreA += temphalfcpuCore
                        self.alreadyBuyServerInfo[serverId].availableRamA += temphalfram
                        self.alreadyBuyServerInfo[serverId].availableCpuCoreB += temphalfcpuCore
                        self.alreadyBuyServerInfo[serverId].availableRamB += temphalfram
                        self.vmID2vmType.pop(delVmId)
                        self.vmID2sid.pop(delVmId)
                    else:
                        # 部署在节点A
                        if self.vmID2End[delVmId] == 1:
                            self.alreadyBuyServerInfo[serverId].availableCpuCoreA += tempVmInfo.cpuCore
                            self.alreadyBuyServerInfo[serverId].availableRamA += tempVmInfo.ram
                        else:
                            self.alreadyBuyServerInfo[serverId].availableCpuCoreB += tempVmInfo.cpuCore
                            self.alreadyBuyServerInfo[serverId].availableRamB += tempVmInfo.ram
                        self.vmID2vmType.pop(delVmId)
                        self.vmID2End.pop(delVmId)
                        self.vmID2sid.pop(delVmId)
            
            tCnt = sIndex = len(self.alreadyBuyServerInfo) - buyCntToday;
            tempServerInfos = {}
            Nmap = {}
            for k1 in range(len(buyOrderToday)): #遍历所有买的服务器型号
                for k2 in range(len(buyHashToday)):
                    tempServerNumber = buyHashToday[k2 + sIndex]
                    if tempServerNumber == buyOrderToday[k1]:
                        Nmap[k2 + sIndex] = tCnt
                        tempServerInfos[tCnt] = self.alreadyBuyServerInfo[k2 + sIndex]
                        tCnt += 1
            
            for k in range(len(buyHashToday)):
                self.alreadyBuyServerInfo[k + sIndex] = tempServerInfos[ k + sIndex]
            
            for key,value in self.vmID2sid.items(): #虚拟机对应的服务器ID需要改变
                if value < sIndex:
                    continue
                self.vmID2sid[key] = Nmap[value]
            
            
            resForRequest = []
            for tres in tempRes:
                tNum = 0
                for t in range(1,len(tres)):
                    if tres[t] >= '0' and tres[t] <= '9':
                        tNum = tNum * 10 + int(tres[t]) 
                    else:
                        break
                if tNum < sIndex:
                    resForRequest.append(tres)
                    continue
                tempStr = '(' + str(Nmap[tNum]) + tres[t:]
                resForRequest.append(tempStr)
            # purchase输出信息
            res.append("(purchase, " + str(len(buyOrderToday)) + ")\n")
            for j in range(0, len(buyOrderToday)):
                tempStr = "(" + self.ServerList[buyOrderToday[j]].stype + ", " + str(numsBuyToday[buyOrderToday[j]]) + ")\n"
                res.append(tempStr)
            #print(buyCntToday)
            
            # migration输出信息
            res.append("(migration, 0)\n")
            for tres in resForRequest:
                res.append(tres)
        #pstarttime = time.time()
        
        for r in res:
            sys.stdout.write(r)
            sys.stdout.flush()
            
        #pendtime =time.time()
        #end = time.time()
        #print("打印时间消耗:",pendtime - pstarttime)
        #print("循环体时间消耗:",end - start)
        #f = open('res.txt','w')
        #f.writelines(res)
        #print(cnt)

        
if __name__ == "__main__":
    #start = time.time()
    #filepath = 'training-1.txt'
    #inputList = readFile(filepath)
    #ServerList, VMList, CommandList = input2format(inputList)
    ServerList, VMList, CommandList = input2formatstd()
    op = Optimization(ServerList, VMList, CommandList)
    op.optimization()
    #end = time.time()
    #print(end-start)
    

    
    