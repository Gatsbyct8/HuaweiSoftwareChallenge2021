class VirtualMachine:
    def __init__(self, vtype="", cpuCore = 0, ram = 0, deploy = 0, vmId = 0):
        self.vtype = vtype
        self.cpuCore = cpuCore
        self.ram = ram
        self.deploy = deploy
        self.vmId = vmId