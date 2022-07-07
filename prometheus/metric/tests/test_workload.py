import pytest

from prometheus.metric.workload import Workload

@pytest.fixture
def metric_memory():
    wl = Workload("test_pod", "ns", "type")
    wl.memoryMax = 20
    wl.memoryMin = 1
    wl.memoryAvg = 8
    wl.memoryRequest = 10
    wl.memoryLimit = 25

    return wl

def test_analyse_correct_values(metric_memory):
    workload = metric_memory
    ret = workload.analyseMemoryRequest()
    ret = workload.analyseMemoryLimit()

    assert len(ret) == 0

def test_analyse_memory_request_low(metric_memory):
    workload = metric_memory
    workload.memoryRequest = 9
    ret = workload.analyseMemoryRequest()

    assert len(ret) == 1

def test_analyse_memory_request_high(metric_memory):
    workload = metric_memory
    workload.memoryRequest = 21
    ret = workload.analyseMemoryRequest()

    assert len(ret) == 1

def test_analyse_memory_request_notset(metric_memory):
    workload = metric_memory
    workload.memoryRequest = None
    ret = workload.analyseMemoryRequest()

    assert len(ret) == 1
    
def test_analyse_memory_request_notavg(metric_memory):
    workload = metric_memory
    workload.memoryAvg = None
    propreq = workload.properMemoryRequest()
    ret = workload.analyseMemoryRequest()

    assert propreq == None
    assert len(ret) == 0

def test_analyse_memory_limit_not_set(metric_memory):
    workload = metric_memory
    workload.memoryLimit = None

    ret = workload.analyseMemoryLimit()

    assert len(ret) == 1  

def test_analyse_memory_limit_not_max(metric_memory):
    workload = metric_memory
    workload.memoryMax = None

    ret = workload.analyseMemoryLimit()

    assert len(ret) == 0

def test_analyse_memory_limit_reached(metric_memory):
    workload = metric_memory
    workload.memoryMax = 25

    ret = workload.analyseMemoryLimit()

    assert len(ret) == 1