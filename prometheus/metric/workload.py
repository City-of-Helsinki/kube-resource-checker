import math

class Workload:
    MEMORY_REQUEST_RESERVE_FACTOR = 1.2
    MEMORY_REQUEST_MAXIMUM_FACTOR = 2
    CPU_REQUEST_RESERVE_FACTOR = 1.5
    CPU_REQUEST_MAXIMUM_FACTOR = 2

    memoryMax = None
    memoryMin = None
    memoryAvg = None
    memoryRequest = None
    memoryLimit = None

    cpuMax = None
    cpuMin = None
    cpuAvg = None
    cpuRequest = None
    cpuLimit = None

    def __init__(self, name, namespace, type):
        self.name = name
        self.namespace = namespace
        self.type = type

    def asString(self):
        return "%s(%s,%s) : %s > %s > %s | %s , %s ; %s > %s > %s | %s , %s" % (self.name, self.namespace, self.type, self.memoryMax, self.memoryAvg,  self.memoryMin, self.memoryRequest, self.memoryLimit, self.cpuMax, self.cpuAvg,  self.cpuMin, self.cpuRequest, self.cpuLimit  )
        
    def analyseMessage(self):
        ret = self.analyseMemoryRequest()
        ret.extend(self.analyseMemoryLimit())

        ret.extend(self.analyseCpuRequest())
        ret.extend(self.analyseCpuLimit())

        return ret 

    def analyseMemoryRequest(self) :
        ret = []
        properRequest = self.properMemoryRequest()
        if properRequest is None:
            return ret

        if self.memoryRequest is None :
            ret.append( "Memory request has not set, proper value would be %sMi" % ( math.ceil(properRequest)) )
            return ret

        if self.memoryRequest < properRequest :
            ret.append( "Memory request is too small: request is %sMi, it should be %sMi" % ( round(self.memoryRequest, 2), math.ceil(properRequest)) )

        if self.memoryRequest > self.memoryMax and self.memoryRequest > math.ceil(properRequest) :
            ret.append( "Memory request is exaggerated: request is %sMi, it should be %sMi" % ( round(self.memoryRequest, 2), math.ceil(properRequest)) )

        return ret

    def analyseMemoryLimit(self) :
        ret = []

        if self.memoryMax is None:
            return ret

        if self.memoryLimit is None:
            ret.append( "Memory limit has not set, proper value would be %sMi" % ( math.ceil(self.properMemoryLimit())) )
            return ret

        # round up to integer
        if math.ceil(self.memoryLimit) <= math.ceil(self.memoryMax) :
            ret.append( "Memory limit has reached: limit is %sMi" % ( round(self.memoryLimit, 2)) )

        return ret

    def analyseCpuRequest(self) :
        ret = []
        properRequest = self.properCpuRequest()
        if properRequest is None:
            return ret

        if self.cpuRequest is None :
            ret.append( "Cpu request has not set, proper value would be %sm" % ( math.ceil(properRequest)) )
            return ret

        if self.cpuRequest < properRequest :
            ret.append( "Cpu request is too small: request is %sm, it should be %sm" % ( round(self.cpuRequest, 2), math.ceil(properRequest)) )

        if self.cpuRequest > self.cpuMax and self.cpuRequest > math.ceil(properRequest) :
            ret.append( "Cpu request is exaggerated: request is %sm, it should be %sm" % ( round(self.cpuRequest, 2), math.ceil(properRequest)) )

        return ret


    def analyseCpuLimit(self) :
        ret = []

        if self.cpuMax is None:
            return ret

        if self.cpuLimit is None:
            ret.append( "Cpu limit has not set, proper value would be %sm" % ( math.ceil(self.properCpuLimit())) )
            return ret

        # round up to integer
        if math.ceil(self.cpuLimit) <= math.ceil(self.cpuMax) :
            ret.append( "Cpu limit has reached: limit is %sm" % ( round(self.cpuLimit, 2)) )

        return ret

    def properMemoryRequest(self) :
        if self.memoryAvg is None:
            return None

        return self.memoryAvg * self.MEMORY_REQUEST_RESERVE_FACTOR

    def properMemoryLimit(self) :
        if self.memoryMax is None:
            return None

        return self.memoryMax * self.MEMORY_REQUEST_MAXIMUM_FACTOR

    def properCpuRequest(self) :
        if self.cpuAvg is None:
            return None

        return self.cpuAvg * self.CPU_REQUEST_RESERVE_FACTOR

    def properCpuLimit(self) :
        if self.cpuMax is None:
            return None

        return self.cpuMax * self.CPU_REQUEST_MAXIMUM_FACTOR
