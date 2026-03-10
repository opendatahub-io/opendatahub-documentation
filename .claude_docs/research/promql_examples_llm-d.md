# PromQL Examples for LLM-D Monitoring

**Source**: https://gist.github.com/sallyom/375d7bbfc33270c5791b0ac0430b6998

This gist provides comprehensive PromQL queries for monitoring LLM-D deployments using Prometheus metrics.

## Content Summary

### Tier 1: Immediate Failure & Saturation Indicators
- Overall and per-model error rates
- Request preemptions
- Latency percentiles (P50, P90, P99)
- Time to First Token (TTFT) and Time Per Token (TPT)
- Scheduler health and error rates
- GPU utilization
- Request rates
- EPP E2E latency and plugin processing

### Tier 2: Diagnostic Drill-Down

**Path A: Basic Model Serving & Scaling**
- KV Cache utilization
- Request queue lengths
- Model throughput (tokens/sec)
- Generation token rate
- Queue utilization

**Path B: Intelligent Routing & Load Balancing**
- Request distribution (QPS per instance)
- Token distribution
- Idle GPU time
- Routing decision latency

**Path C: Prefix Caching**
- Prefix cache hit rate
- Per-instance hit rate
- Cache utilization

**Path D: P/D Disaggregation**
- Prefill/Decode worker utilization
- Prefill queue length

## Key Technical Details

### Metric Naming
- Older deployments: `inference_model_*` prefix
- Newer deployments: `inference_objective_*` prefix
- vLLM-specific metrics: `vllm:*` prefix

### Missing Metrics
The gist identifies metrics that require additional instrumentation:
- Cache eviction rate
- Prefix cache memory usage (absolute)
- KV cache transfer times for P/D disaggregation

### Dependencies
- Requires Prometheus and User Workload Monitoring (UWM)
- Requires ServiceMonitor configuration
- Load generation script available for testing error metrics
