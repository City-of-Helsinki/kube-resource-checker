import math

class Workload:
    MEMORY_REQUEST_RESERVE_FACTOR = 1.0
    MEMORY_REQUEST_RESERVE_FACTOR_NOTIFY = 1.5 # notify message for user
    MEMORY_REQUEST_MAXIMUM_FACTOR = 2
    CPU_REQUEST_RESERVE_FACTOR = 1.2
    CPU_REQUEST_RESERVE_FACTOR_NOTIFY = 1.5 # notify message for user
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

        if self.memoryRequest < self.memoryAvg :
            ret.append( "Memory request is too small: request is %sMi, it should be %sMi" % ( round(self.memoryRequest, 2), math.ceil(properRequest)) )

        if self.memoryRequest > self.memoryMax and self.memoryRequest > (math.ceil(properRequest) * self.MEMORY_REQUEST_RESERVE_FACTOR_NOTIFY):
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
            ret.append( "Memory limit has reached: limit is %sMi. Is memory leak somewhere?" % ( round(self.memoryLimit, 2)) )

        return ret

    def analyseCpuRequest(self) :
        ret = []
        properRequest = self.properCpuRequest()
        if properRequest is None:
            return ret

        if self.cpuRequest is None :
            ret.append( "Cpu request has not set, proper value would be %sm" % ( math.ceil(properRequest)) )
            return ret

        if self.cpuRequest < self.cpuAvg :
            ret.append( "Cpu request is too small: request is %sm, it should be %sm" % ( round(self.cpuRequest, 2), math.ceil(properRequest)) )

        if self.cpuRequest > self.cpuMax and self.cpuRequest > (math.ceil(properRequest) * self.CPU_REQUEST_RESERVE_FACTOR_NOTIFY ) :
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

        return self.roundProperToHuman(self.memoryAvg * self.MEMORY_REQUEST_RESERVE_FACTOR, 10)

    def properMemoryLimit(self) :
        if self.memoryMax is None:
            return None

        return self.roundProperToHuman(self.memoryMax * self.MEMORY_REQUEST_MAXIMUM_FACTOR, 50)

    def properCpuRequest(self) :
        if self.cpuAvg is None:
            return None

        return self.roundProperToHuman(self.cpuAvg * self.CPU_REQUEST_RESERVE_FACTOR)

    def properCpuLimit(self) :
        if self.cpuMax is None:
            return None

        return self.roundProperToHuman(self.cpuMax * self.CPU_REQUEST_MAXIMUM_FACTOR, 100)

    def roundProperToHuman(self, value, minValue = 0):
        valueInt = math.ceil(value)
        if valueInt <= 5 and minValue <= 5: # value is 0..5 round up to  5
            return 5
        if valueInt < 100 and minValue <= 10:  # value is 6..99 round up to 10
            return math.ceil(value/10)*10
        if valueInt < 500 and minValue <= 50:  # value is 100..999 round up to 10
            return math.ceil(value/50)*50
        
        return math.ceil(value/100)*100 # value is equal or over 1000, round up to 100
