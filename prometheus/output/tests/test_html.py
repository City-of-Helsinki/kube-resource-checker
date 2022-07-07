import pytest

from prometheus.metric.workload import Workload

from prometheus.output.html import Html

@pytest.fixture
def workloadList():
    wl = Workload("test_pod", "ns", "type")
    wl.memoryMax = 20
    wl.memoryMin = 1
    wl.memoryAvg = 8
    wl.memoryRequest = 10
    wl.memoryLimit = 25

    wl.cpuMax = 100
    wl.cpuMin = 10
    wl.cpuAvg = 50
    wl.cpuRequest = 20
    wl.cpuLimit = 200

    return [wl]


def test_html_generation(capsys, workloadList):
    html = Html()
    html.setBody(workloadList)

#    with capsys.disabled():
#        html.dump()

    assert len(html.soup.find_all('tr')) == 2
