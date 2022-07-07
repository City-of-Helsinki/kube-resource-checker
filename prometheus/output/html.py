from bs4 import BeautifulSoup
import os
import math

class Html:
    HEADERS = [
        'Name',
        'Namespace',
        'Type',
        'Memory Max',
        'Memory Avg',
        'Memory Min',
        'Memory Req',
        'Memory Req Target',
        'Memory Limit',
        'Memory Limit Target',
        'Cpu Max',
        'Cpu Avg',
        'Cpu Min',
        'Cpu Req',
        'Cpu Req Target',
        'Cpu Limit',
        'Cpu Limit Target',
        'Message',
    ]

    def __init__(self):
        self.filename = os.environ.get('OUTPUT_HTML_FILE', 'resource_analyse.html')
        self.soup = BeautifulSoup("", "html5lib")

    def setBody(self, workloadList):
        table = self.soup.new_tag("table")
        self.soup.body.append(table)

        table.append(self.tableHeaderRow())

        for workload in workloadList:
             table.append(self.tableDataRow(workload))

    def tableHeaderRow(self):
        tr = self.soup.new_tag("tr")

        for header in self.HEADERS :
            th = self.soup.new_tag("th")
            th.string = header
            tr.append(th)

        return tr


    def tableDataRow(self, workload):
        tr = self.soup.new_tag("tr")

        self.appendTd(tr, workload.name)
        self.appendTd(tr, workload.namespace)
        self.appendTd(tr, workload.type)

        self.appendTd(tr, workload.memoryMax)
        self.appendTd(tr, workload.memoryAvg)
        self.appendTd(tr, workload.memoryMin)
        self.appendTd(tr, workload.memoryRequest)
        self.appendTd(tr, workload.properMemoryRequest(), len(workload.analyseMemoryRequest())) # something to notice -> set bgcolor
        self.appendTd(tr, workload.memoryLimit)
        self.appendTd(tr, workload.properMemoryLimit(), len(workload.analyseMemoryLimit())) # something to notice -> set bgcolor

        self.appendTd(tr, workload.cpuMax)
        self.appendTd(tr, workload.cpuAvg)
        self.appendTd(tr, workload.cpuMin)
        self.appendTd(tr, workload.cpuRequest)
        self.appendTd(tr, workload.properCpuRequest(), len(workload.analyseCpuRequest())) # something to notice -> set bgcolor
        self.appendTd(tr, workload.cpuLimit)
        self.appendTd(tr, workload.properCpuLimit(), len(workload.analyseCpuLimit())) # something to notice -> set bgcolor

        self.appendTd(tr, workload.analyseMessage())

        return tr

    def appendTd(self, tr, content, setColor = 0) : 
        td = self.soup.new_tag("td")
        self.addText(td, content)
        if setColor :
            td['bgcolor'] = "red"

        tr.append(td)

    def addText(self, td, content):
        if type(content) is list:
            for index, item in enumerate(content): 
                span = self.soup.new_tag("span")
                span.string = str(item)
                td.append(span)
                if index < len(content):
                    td.append(self.soup.new_tag("br"))

            return 

        if type(content) is float:
            td.string = str(math.ceil(content))
            return
        
        td.string = str(content)

    def dump(self):
        soup = BeautifulSoup("", "html5lib")
        print (soup.prettify())

    def writeHtml(self):
        with open(self.filename, "w", encoding='utf-8') as file:
            file.write(str(self.soup))
