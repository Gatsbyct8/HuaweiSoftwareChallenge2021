class VirtualMachine:
    def __init__(self, vmType="", cpuCore = 0, ram = 0, deploy = 0, vmId = 0):
        self.vmType = vmType
        self.cpuCore = cpuCore
        self.ram = ram
        self.deploy = deploy
        self.vmId = vmId