from .workload import Workload
import math

class Workloads:
    def __init__(self):
        self.workloads = {}
        
    def initWorkload(self, metric):
        workloadName = metric['metric']['workload']
        if not workloadName in self.workloads:
            self.workloads[workloadName] = Workload(workloadName,metric['metric']['namespace'],  metric['metric']['workload_type'])

        return workloadName

    # Memory
    def addMemoryMax(self, metric):
        self.workloads[self.initWorkload(metric)].memoryMax = float(metric['value'][1])

    def addMemoryMin(self, metric):
        self.workloads[self.initWorkload(metric)].memoryMin = float(metric['value'][1])

    def addMemoryAvg(self, metric):
        self.workloads[self.initWorkload(metric)].memoryAvg = float(metric['value'][1])

    def addMemoryRequest(self, metric):
        self.workloads[self.initWorkload(metric)].memoryRequest = float(metric['value'][1])

    def addMemoryLimit(self, metric):
        self.workloads[self.initWorkload(metric)].memoryLimit = float(metric['value'][1])

    # Memory
    def addCpuMax(self, metric):
        self.workloads[self.initWorkload(metric)].cpuMax = float(metric['value'][1])

    def addCpuMin(self, metric):
        self.workloads[self.initWorkload(metric)].cpuMin = float(metric['value'][1])

    def addCpuAvg(self, metric):
        self.workloads[self.initWorkload(metric)].cpuAvg = float(metric['value'][1])

    def addCpuRequest(self, metric):
        self.workloads[self.initWorkload(metric)].cpuRequest = float(metric['value'][1])

    def addCpuLimit(self, metric):
        self.workloads[self.initWorkload(metric)].cpuLimit = float(metric['value'][1])

    # Analyse
    def analyse(self):
        for workload in self.workloads.values():
            ret = workload.analyseMessage()

            if len(ret) :
                print (workload.name)
                for r in ret:
                    print (f"  {r}")

    def analyseMemoryBalance(self):
        requested = 0.0
        usedAvg = 0.0
        usedMax = 0.0
        for workload in self.workloads.values():
            if workload.memoryRequest is not None and  workload.memoryAvg is not None :
                requested += workload.memoryRequest
                usedAvg += workload.memoryAvg
                usedMax += workload.memoryMax

        print(f"Memory used (avg) vs requested : {math.ceil(usedAvg)} Mi/ {math.ceil(requested)} Mi")
        print(f"Memory used (max) vs requested : {math.ceil(usedMax)} Mi/ {math.ceil(requested)} Mi")

    def analyseCpuBalance(self):
        requested = 0.0
        usedAvg = 0.0
        usedMax = 0.0
        for workload in self.workloads.values():
            if workload.cpuRequest is not None and  workload.cpuAvg is not None :
                requested += workload.cpuRequest
                usedAvg += workload.cpuAvg
                usedMax += workload.cpuMax

        print(f"Cpu used (avg) vs requested : {math.ceil(usedAvg)} m/ {math.ceil(requested)} m")
        print(f"Cpu used (max) vs requested : {math.ceil(usedMax)} m/ {math.ceil(requested)} m")

    def dump(self):
        for workload in self.workloads.values():
            print (workload.asString())

    def getWorkloadListByName(self):
        return dict(sorted(self.workloads.items())).values()

    def getWorkloadListByNameAndTypeAndNamespace(self):
        sortedList = sorted(self.workloads.values(), key=lambda x: x.name)
        sortedList = sorted(sortedList, key=lambda x: x.type)
        return sorted(sortedList, key=lambda x: x.namespace)
