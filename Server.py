class Server:
    def __init__(self, ptype = "", cpuCore = 0, ram = 0, hardWareCost = 0, energyCost = 0):
        self.stype = ptype  #服务器型号
        self.ram = ram     #总内存
        self.cpuCore = cpuCore   #总cpu核数
        self.hardWareCost =  hardWareCost  #硬件成本
        self.energyCost = energyCost   #开机功耗
        self.nodeA_usr = []
        self.nodeB_usr = []
        self.sid = 0
        self.availableCpuCoreA = self.cpuCore / 2 #A剩余核心数
        self.availableRamA = self.ram / 2       #A剩余内存
        self.availableCpuCoreB = self.cpuCore / 2 #B剩余核心数
        self.availableRamB = self.ram / 2       #B剩余内存

    
    #当在节点A或B中添加一个用户申请虚拟机时
    def node_A_Add(self, VM):
        self.NodeA_usr.append(VM)
        self.availableCpuCoreA -= VM.cpuCore
        self.availableRamA -= VM.ram
    
    def node_B_Add(self, VM):
        self.nodeB_usr.append(VM)
        self.availableCpuCoreA -= VM.cpuCore
        self.availableRamB -= VM.ram
    
    #双节点申请时
    def bothNodeAdd(self, VM):
        self.NodeA_usr.append(VM)
        self.availableCpuCoreA -= VM.cpuCore / 2
        self.availableRamA -= VM.ram / 2
        self.NodeB_usr.append(VM)
        self.availableCpuCoreB -= VM.cpuCore / 2
        self.availableRamB -= VM.ram / 2

    #服务器性价比排序
    def __lt__(self, rhs):
        factor1 = self.hardWareCost / (self.availableCpuCoreA + self.availableCpuCoreB) + \
                self.hardWareCost / (self.availableRamA + self.availableRamB) + self.energyCost
        factor2 = rhs.hardWareCost / (rhs.availableCpuCoreA + rhs.availableCpuCoreB) + \
                rhs.hardWareCost / (rhs.availableRamA + rhs.availableRamB) + rhs.energyCost
        return factor1 < factor2
    

    






