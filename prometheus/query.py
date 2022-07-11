class Query:
    memoryFactor = "/1024/1024"  # MiB
    cpuFactor = "*1000"  # mCpu

    def __init__(self, range):
        self.range = range

    # Memory queries
    def queryMemoryMax(self):
        query = (
            'max( max_over_time(container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", image!=""}[%s])%s * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type)'
            % (self.range, self.memoryFactor)
        )
        return {"query": query}

    def queryMemoryMin(self):
        query = (
            'min( min_over_time(container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", image!=""}[%s])%s * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type)'
            % (self.range, self.memoryFactor)
        )
        return {"query": query}

    def queryMemoryAvg(self):
        query = (
            'avg( avg_over_time(container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", image!=""}[%s])%s * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type)'
            % (self.range, self.memoryFactor)
        )
        return {"query": query}

    def queryMemoryRequest(self):
        query = (
            'sum( kube_pod_container_resource_requests{job="kube-state-metrics", cluster="", resource="memory"}%s * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type) / count( kube_pod_container_resource_requests{job="kube-state-metrics", cluster="", resource="memory"}/1024/1024 * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type)'
            % (self.memoryFactor)
        )
        return {"query": query}

    def queryMemoryLimit(self):
        query = (
            'sum( kube_pod_container_resource_limits{job="kube-state-metrics", cluster="", resource="memory"}%s * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type) / count( kube_pod_container_resource_limits{job="kube-state-metrics", cluster="", resource="memory"}/1024/1024 * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type)'
            % (self.memoryFactor)
        )
        return {"query": query}

    # Cpu queries
    def queryCpuMax(self):
        query = (
            'max( max_over_time( rate( container_cpu_usage_seconds_total{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", image!=""}[1m])[%s:30s])%s * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type)'
            % (self.range, self.cpuFactor)
        )
        return {"query": query}

    def queryCpuMin(self):
        query = (
            'min( min_over_time( rate( container_cpu_usage_seconds_total{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", image!=""}[1m])[%s:30s])%s * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type)'
            % (self.range, self.cpuFactor)
        )
        return {"query": query}

    def queryCpuAvg(self):
        query = (
            'avg( avg_over_time( rate( container_cpu_usage_seconds_total{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", image!=""}[1m])[%s:30s])%s * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type)'
            % (self.range, self.cpuFactor)
        )
        return {"query": query}

    def queryCpuRequest(self):
        query = (
            'sum( kube_pod_container_resource_requests{job="kube-state-metrics", cluster="", resource="cpu"}%s * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type) / count( kube_pod_container_resource_requests{job="kube-state-metrics", cluster="", resource="cpu"} * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type)'
            % (self.cpuFactor)
        )
        return {"query": query}

    def queryCpuLimit(self):
        query = (
            'sum( kube_pod_container_resource_limits{job="kube-state-metrics", cluster="", resource="cpu"}%s * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type) / count( kube_pod_container_resource_limits{job="kube-state-metrics", cluster="", resource="cpu"} * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{cluster=""}) by (namespace, workload, workload_type)'
            % (self.cpuFactor)
        )
        return {"query": query}
