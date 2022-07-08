from bs4 import BeautifulSoup
import os
import math

class Html:
    HEADERS = [
        'Namespace',
        'Name',
        'Type',
        'Memory Max (MiB)',
        'Memory Avg (MiB)',
        'Memory Min (MiB)',
        'Memory Req (MiB)',
        'Memory Req Proposal (MiB)',
        'Memory Limit (MiB)',
        'Memory Limit Proposal (MiB)',
        'Cpu Max (m)',
        'Cpu Avg (m)',
        'Cpu Min (m)',
        'Cpu Req (m)',
        'Cpu Req Proposal (m)',
        'Cpu Limit (m)',
        'Cpu Limit Proposal (m)',
        'Message',
    ]

    def __init__(self, footer = ""):
        self.filename = os.environ.get('OUTPUT_HTML_FILE', 'resource_analyse.html')
        self.soup = BeautifulSoup("", "html5lib")
        self.setStyle()
        self.footer = footer

    def setBody(self, workloadList):
        table = self.soup.new_tag("table")
        self.soup.body.append(table)

        table.append(self.tableHeaderRow())

        for workload in workloadList:
             table.append(self.tableDataRow(workload))

        self.setFooter()

    def setStyle(self):
        style = self.soup.new_tag("style")
        style['type'] = "text/css"
        style.string = '''
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
.memory {
  text-align: center;
}
.cpu {
  text-align: center;
}
tr:hover {background-color: #D6EEEE;}
'''
        
        self.soup.head.append(style)

    def setFooter(self):
        if not self.footer:
            return

        footer = self.soup.new_tag("footer")
        self.soup.body.append(footer)

        for line in self.footer.split("\n") :
            p = self.soup.new_tag("p")
            p.string = line
            footer.append(p)

    def tableHeaderRow(self):
        tr = self.soup.new_tag("tr")

        for header in self.HEADERS :
            th = self.soup.new_tag("th")
            th.string = header
            tr.append(th)

        return tr


    def tableDataRow(self, workload):
        tr = self.soup.new_tag("tr")

        self.appendTd(tr, workload.namespace)
        self.appendTd(tr, workload.name)
        self.appendTd(tr, workload.type)

        self.appendTd(tr, workload.memoryMax, "memory")
        self.appendTd(tr, workload.memoryAvg, "memory")
        self.appendTd(tr, workload.memoryMin, "memory")
        self.appendTd(tr, workload.memoryRequest, "memory")
        self.appendTd(tr, workload.properMemoryRequest(), "memory", self.tdBgColor(len(workload.analyseMemoryRequest()) )) # something to notice -> set bgcolor
        self.appendTd(tr, workload.memoryLimit, "memory")
        self.appendTd(tr, workload.properMemoryLimit(), "memory", self.tdBgColor(len(workload.analyseMemoryLimit()))) # something to notice -> set bgcolor

        self.appendTd(tr, workload.cpuMax, "cpu")
        self.appendTd(tr, workload.cpuAvg, "cpu")
        self.appendTd(tr, workload.cpuMin, "cpu")
        self.appendTd(tr, workload.cpuRequest, "cpu")
        self.appendTd(tr, workload.properCpuRequest(), "cpu", self.tdBgColor(len(workload.analyseCpuRequest()))) # something to notice -> set bgcolor
        self.appendTd(tr, workload.cpuLimit, "cpu")
        self.appendTd(tr, workload.properCpuLimit(), "cpu", self.tdBgColor(len(workload.analyseCpuLimit()))) # something to notice -> set bgcolor

        self.appendTd(tr, workload.analyseMessage())

        return tr

    def tdBgColor(self, setBgColor = 0):
        if setBgColor :
            return 'red'

        return ''
        

    def appendTd(self, tr, content, setClass = "", setBgColor = "") : 
        td = self.soup.new_tag("td")
        self.addText(td, content)
        if setBgColor :
            td['bgcolor'] = setBgColor

        if setClass :
            td['class'] = setClass

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
        print (self.soup.prettify())

    def writeHtml(self):
        with open(self.filename, "w", encoding='utf-8') as file:
            file.write(str(self.soup.prettify()))
