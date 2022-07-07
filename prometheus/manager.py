from .session import Session
from .query import Query
from .metric.workloads import Workloads
from .output.html import Html

class Manager:
    def __init__(self, session, host, range):
        self.session = Session(session, host)
        self.query = Query(range)
        self.workloads = Workloads()

    def collectData(self):
        self.getMemoryMax()
        self.getMemoryMin()
        self.getMemoryAvg()
        self.getMemoryRequest()
        self.getMemoryLimit()

        self.getCpuMax()
        self.getCpuMin()
        self.getCpuAvg()
        self.getCpuRequest()
        self.getCpuLimit()
 
    # Memory
    def getMemoryMax(self) :
        content = self.session.runQuery(self.query.queryMemoryMax())
        for metric in content['data']['result']:
            self.workloads.addMemoryMax(metric)

    def getMemoryMin(self) :
        content = self.session.runQuery(self.query.queryMemoryMin())
        for metric in content['data']['result']:
            self.workloads.addMemoryMin(metric)

    def getMemoryAvg(self) :
        content = self.session.runQuery(self.query.queryMemoryAvg())
        for metric in content['data']['result']:
            self.workloads.addMemoryAvg(metric)

    def getMemoryRequest(self) :
        content = self.session.runQuery(self.query.queryMemoryRequest())
        for metric in content['data']['result']:
            self.workloads.addMemoryRequest(metric)

    def getMemoryLimit(self) :
        content = self.session.runQuery(self.query.queryMemoryLimit())
        for metric in content['data']['result']:
            self.workloads.addMemoryLimit(metric)

    # Cpu
    def getCpuMax(self) :
        content = self.session.runQuery(self.query.queryCpuMax())
        for metric in content['data']['result']:
            self.workloads.addCpuMax(metric)

    def getCpuMin(self) :
        content = self.session.runQuery(self.query.queryCpuMin())
        for metric in content['data']['result']:
            self.workloads.addCpuMin(metric)

    def getCpuAvg(self) :
        content = self.session.runQuery(self.query.queryCpuAvg())
        for metric in content['data']['result']:
            self.workloads.addCpuAvg(metric)

    def getCpuRequest(self) :
        content = self.session.runQuery(self.query.queryCpuRequest())
        for metric in content['data']['result']:
            self.workloads.addCpuRequest(metric)

    def getCpuLimit(self) :
        content = self.session.runQuery(self.query.queryCpuLimit())
        for metric in content['data']['result']:
            self.workloads.addCpuLimit(metric)

    # Analyse & output
    def analyse(self):
        self.workloads.analyse()

    def printResults(self):
        self.workloads.dump()

    def printBalance(self):
        self.workloads.analyseMemoryBalance()
        self.workloads.analyseCpuBalance()

    def outputHtlm(self):
        html = Html()
        html.setBody(self.workloads.getWorkloadListByNameAndTypeAndNamespace())
        html.writeHtml()

