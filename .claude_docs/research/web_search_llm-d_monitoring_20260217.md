# Web Search Findings: llm-d Monitoring

**Date**: 2026-02-17
**Topic**: llm-d inference scheduler, vLLM metrics, ServiceMonitor, and Prometheus monitoring

## llm-d Inference Scheduler

### Overview
- **GitHub**: https://github.com/llm-d/llm-d
- **Official Site**: https://llm-d.ai/
- llm-d achieves state-of-the-art inference performance with modern accelerators on Kubernetes
- Built on vLLM as the default model server and engine
- Inference Gateway serves as request scheduler and balancer

### Key Components
1. **Endpoint Picker (EPP)**: Cache-aware and load-aware scheduling decisions
2. **Disaggregated Serving**: Separate prefill and decode services
3. **Multi-tier KV Cache**: For intermediate values

### Performance (2026 Demonstration)
- P50 TTFT: 92 ms (25% faster than vLLM alone)
- P95 TTFT: 237 ms (63% faster)
- KV cache hit rate: ~90% (45% improvement)

**Sources**:
- [Redefining LLM observability with llm-d in Red Hat OpenShift AI 3.0](https://www.redhat.com/en/blog/tokens-caches-how-llm-d-improves-llm-observability-red-hat-openshift-ai-3.0)
- [Accelerate multi-turn LLM workloads on OpenShift AI with llm-d intelligent routing](https://developers.redhat.com/articles/2026/01/13/accelerate-multi-turn-workloads-llm-d)
- [What is llm-d?](https://www.redhat.com/en/topics/ai/what-is-llm-d)

## llm-d Features

### Intelligent Scheduling
- KV-cache aware routing: Tracks cache state across the cluster
- Prefix-aware scheduling: Routes requests to replicas with relevant KV cache entries
- Built on Kubernetes Gateway API

### Observability
- Combines vLLM engine-level metrics with llm-d routing and cache-aware insights
- Provides operational consistency for running vLLM with advanced observability

**Sources**:
- [Getting started with llm-d for distributed AI inference](https://developers.redhat.com/articles/2025/08/19/getting-started-llm-d-distributed-ai-inference)

## vLLM Prometheus Metrics

### Official Documentation
- **Metrics Design**: https://docs.vllm.ai/en/latest/design/metrics/
- **Prometheus/Grafana Example**: https://docs.vllm.ai/en/v0.7.2/getting_started/examples/prometheus_grafana.html

### Key Metrics
All vLLM metrics use the `vllm:` prefix:
- `vllm:e2e_request_latency_seconds_bucket` - End-to-end request latency
- `vllm:num_requests_running`, `_swapped`, `_waiting` - Request states
- `vllm:kv_cache_usage_perc` - Cache block usage percentage
- `vllm:request_prompt_tokens` - Request prompt length
- `vllm:request_generation_tokens` - Request generation length
- `vllm:request_success` - Finished requests by finish reason
- `vllm:time_to_first_token_seconds_bucket` - TTFT latency
- `vllm:time_per_output_token_seconds_bucket` - TPT latency
- `vllm:prefix_cache_hits`, `vllm:prefix_cache_queries` - Cache performance
- `vllm:num_preemptions` - Request preemptions

### Metrics Endpoint
- Exposed at `/metrics` HTTP endpoint
- Format: Prometheus Exposition Format text
- Labels include: model_name, finished_reason, scheduling_event

**Sources**:
- [Metrics - vLLM](https://docs.vllm.ai/en/latest/design/metrics/)
- [Monitoring vLLM Inference Servers: A Quick and Easy Guide](https://www.dataunboxed.io/blog/monitoring-vllm-inference-servers-a-quick-and-easy-guide)
- [Building Production-Ready Observability for vLLM](https://medium.com/ibm-data-ai/building-production-ready-observability-for-vllm-a2f4924d3949)

## ServiceMonitor and User Workload Monitoring

### ServiceMonitor Resource
- Custom resource that tells Prometheus Operator how to discover and scrape metrics
- Enables dynamic target discovery
- Eliminates need for manual Prometheus configuration
- Applied in same namespace as the application
- Uses label matching to discover metrics endpoints through Kubernetes Service resources

### User Workload Monitoring
- Separate from platform monitoring
- Enabled via ConfigMap in `openshift-monitoring` namespace
- Setting: `enableUserWorkload: true` in cluster-monitoring-config
- Required for app-level metrics

### Permissions
- Role `monitor-edit` required to create ServiceMonitor and PodMonitor resources

**Sources**:
- [User Workload Monitoring Enhancement](https://github.com/openshift/enhancements/blob/master/enhancements/monitoring/user-workload-monitoring.md)
- [How to Monitor Applications on OpenShift](https://oneuptime.com/blog/post/2026-01-28-monitor-applications-openshift/view)
- [How to monitor workloads using OpenShift monitoring stack](https://developers.redhat.com/articles/2023/08/08/how-monitor-workloads-using-openshift-monitoring-stack)
- [Monitoring your own services](https://docs.redhat.com/en/documentation/openshift_container_platform/4.3/html/monitoring/monitoring-your-own-services)

## Integration Points for Documentation

### Required Documentation Sections
1. **Metrics Reference**: Complete list of llm-d and vLLM metrics with descriptions
2. **ServiceMonitor Configuration**: How to create ServiceMonitor for llm-d/vLLM
3. **PromQL Query Examples**: Ready-to-use queries for common monitoring scenarios
4. **Dashboard Creation**: Step-by-step guide for creating custom dashboards
5. **Troubleshooting**: Common issues and their solutions

### Target Audiences
- Data scientists: Understanding model performance
- Platform administrators: Monitoring infrastructure and resource usage
- SRE teams: Creating dashboards and alerts
