# Documentation Requirements: RHAISTRAT-1206

**Date**: 2026-02-17
**JIRA Ticket**: [RHAISTRAT-1206](https://issues.redhat.com/browse/RHAISTRAT-1206)
**Priority**: Critical
**Status**: New
**Assignee**: Anish Asthana
**Release Note Type**: Enhancement

## Summary

- **Total requirements analyzed**: 1 JIRA ticket with 5 distinct documentation needs
- **New modules needed**: 3
- **Existing modules to update**: 2
- **Breaking changes requiring docs**: 0

## JIRA Ticket Summary

### Title
Documenting llm-d related Metrics and example queries that customer can use to create their own dashboard (self hosted)

### Problem Statement
Users who deploy llm-d (Large Language Model Deployment) lack a guide that explains the data points exported by the system. Without a clear list of these metrics and example queries, it is difficult for users to understand if their hardware is being used effectively or if the system is responding slowly.

### Solution Requirements
The JIRA ticket specifies the need for:

1. Documentation of specific names of data points exported by llm-d
2. PromQL (Prometheus Query Language) example queries
3. Instructions on how to create a ServiceMonitor configuration
4. Guidance on integrating with User Workload Monitoring (UWM)

### Technical References Provided

**Metrics List**:
- Google Doc (internal): https://docs.google.com/document/d/1jfRI6OH72bSL8besUoJ5yxPnrae2K2jpbnN-HNsiAdw/edit?usp=sharing
- Referenced under "llm-d under Components tab"

**PromQL Examples**:
- GitHub Gist: https://gist.github.com/sallyom/375d7bbfc33270c5791b0ac0430b6998
- Comprehensive set of queries organized by tier and monitoring path

## Requirements by Priority

### Critical

#### REQ-001: llm-d Metrics Reference Documentation
- **Source**: [RHAISTRAT-1206](https://issues.redhat.com/browse/RHAISTRAT-1206)
- **Summary**: Create comprehensive reference documentation for llm-d-specific metrics, separate from existing vLLM metrics documentation
- **User impact**: Data scientists, SRE teams, and platform administrators need to understand llm-d scheduler metrics (EPP, routing, cache-aware scheduling) to monitor distributed inference performance
- **Documentation action**:
  - [x] Create `ref-llm-d-metrics.adoc` (REFERENCE)
  - [ ] Update `assemblies/managing-and-monitoring-models.adoc` - include new llm-d metrics reference
- **Acceptance criteria**:
  - [ ] Document all llm-d scheduler metrics with `inference_model_*` and `inference_objective_*` prefixes
  - [ ] Include EPP (Endpoint Picker) metrics: `inference_extension_scheduler_e2e_duration_seconds_bucket`, `inference_extension_plugin_duration_seconds_bucket`
  - [ ] Document routing and scheduling metrics specific to llm-d
  - [ ] Note metric naming differences between deployment versions
  - [ ] Cross-reference existing vLLM metrics documentation
- **References**:
  - [RHAISTRAT-1206 Description](https://issues.redhat.com/browse/RHAISTRAT-1206): Problem statement and solution requirements
  - [PromQL Examples Gist](https://gist.github.com/sallyom/375d7bbfc33270c5791b0ac0430b6998): Comprehensive metric list
  - `/Users/ocbrown/opendatahub-documentation/modules/ref-vllm-metrics.adoc`: Existing vLLM metrics reference
  - [llm-d observability blog](https://www.redhat.com/en/blog/tokens-caches-how-llm-d-improves-llm-observability-red-hat-openshift-ai-3.0): Architecture overview

#### REQ-002: PromQL Query Examples for llm-d Monitoring
- **Source**: [RHAISTRAT-1206](https://issues.redhat.com/browse/RHAISTRAT-1206)
- **Summary**: Provide ready-to-use PromQL query examples organized by monitoring objective (error rates, latency, cache performance, routing efficiency)
- **User impact**: Users can quickly set up monitoring without needing deep Prometheus expertise
- **Documentation action**:
  - [x] Create `ref-llm-d-promql-queries.adoc` (REFERENCE)
  - [ ] Update `assemblies/managing-and-monitoring-models.adoc` - include PromQL queries reference
- **Acceptance criteria**:
  - [ ] Include Tier 1 queries (immediate failure & saturation indicators)
  - [ ] Include Tier 2 queries organized by monitoring path (A: Model Serving, B: Routing, C: Prefix Caching, D: P/D Disaggregation)
  - [ ] Document error rate queries with both total and per-code breakdowns
  - [ ] Include scheduler health and EPP E2E latency queries
  - [ ] Provide GPU utilization and KV cache metrics queries
  - [ ] Add notes about metric naming variations (`inference_model_*` vs `inference_objective_*`)
  - [ ] Document missing metrics and workarounds (cache eviction, transfer times)
- **References**:
  - [PromQL Examples Gist](https://gist.github.com/sallyom/375d7bbfc33270c5791b0ac0430b6998): Complete query list
  - `/Users/ocbrown/opendatahub-documentation/modules/ref-vllm-metrics.adoc`: Existing PromQL examples for vLLM
  - [vLLM metrics documentation](https://docs.vllm.ai/en/latest/design/metrics/): Upstream metric definitions

#### REQ-003: ServiceMonitor Configuration for llm-d
- **Source**: [RHAISTRAT-1206](https://issues.redhat.com/browse/RHAISTRAT-1206)
- **Summary**: Document how to create ServiceMonitor resources to enable Prometheus scraping of llm-d metrics
- **User impact**: Users need to configure ServiceMonitor to expose llm-d metrics to User Workload Monitoring
- **Documentation action**:
  - [x] Create `proc-configuring-servicemonitor-llm-d.adoc` (PROCEDURE)
  - [ ] Update `assemblies/managing-observability.adoc` - include ServiceMonitor procedure for llm-d
- **Acceptance criteria**:
  - [ ] Explain the role of ServiceMonitor in Prometheus metric collection
  - [ ] Provide complete ServiceMonitor YAML example for llm-d endpoints
  - [ ] Document namespace requirements and label selectors
  - [ ] Include port and endpoint path configuration
  - [ ] Reference User Workload Monitoring enablement
  - [ ] Provide verification steps using Prometheus query interface
- **References**:
  - [RHAISTRAT-1206 Description](https://issues.redhat.com/browse/RHAISTRAT-1206): Mentions ServiceMonitor requirement
  - `/Users/ocbrown/opendatahub-documentation/modules/collecting-metrics-from-user-workloads.adoc`: Existing UWM documentation
  - [ServiceMonitor OpenShift docs](https://docs.redhat.com/en/documentation/openshift_container_platform/4.3/html/monitoring/monitoring-your-own-services): Upstream reference
  - [User Workload Monitoring Enhancement](https://github.com/openshift/enhancements/blob/master/enhancements/monitoring/user-workload-monitoring.md): Architecture details

### High

#### REQ-004: Dashboard Creation Guide for llm-d
- **Source**: [RHAISTRAT-1206](https://issues.redhat.com/browse/RHAISTRAT-1206)
- **Summary**: Provide step-by-step procedure for creating custom Grafana dashboards using llm-d metrics
- **User impact**: Users can visualize llm-d performance metrics in custom dashboards tailored to their monitoring needs
- **Documentation action**:
  - [x] Create `proc-creating-llm-d-dashboard.adoc` (PROCEDURE)
  - [ ] Update `modules/deploying-vllm-gpu-metrics-dashboard-grafana.adoc` - add llm-d dashboard variant
- **Acceptance criteria**:
  - [ ] Leverage existing Grafana dashboard deployment procedure
  - [ ] Provide GrafanaDashboard YAML template for llm-d metrics
  - [ ] Document required panels: error rates, latency histograms, cache hit rates, scheduler health
  - [ ] Include panel configuration examples with PromQL queries
  - [ ] Reference the PromQL query documentation for complete query list
  - [ ] Provide troubleshooting tips for missing metrics
- **References**:
  - [PromQL Examples Gist](https://gist.github.com/sallyom/375d7bbfc33270c5791b0ac0430b6998): Dashboard panel queries
  - `/Users/ocbrown/opendatahub-documentation/modules/deploying-vllm-gpu-metrics-dashboard-grafana.adoc`: Existing dashboard procedure
  - [Monitoring vLLM guide](https://www.dataunboxed.io/blog/monitoring-vllm-inference-servers-a-quick-and-easy-guide): Community example

#### REQ-005: Concept Documentation - llm-d Observability Architecture
- **Source**: [RHAISTRAT-1206](https://issues.redhat.com/browse/RHAISTRAT-1206) + [Web Research](https://www.redhat.com/en/blog/tokens-caches-how-llm-d-improves-llm-observability-red-hat-openshift-ai-3.0)
- **Summary**: Explain the observability architecture of llm-d, including how metrics are exposed from different components (EPP, vLLM instances, scheduler)
- **User impact**: Users understand the relationship between llm-d components and their metrics, enabling effective troubleshooting
- **Documentation action**:
  - [x] Create `con-llm-d-observability-architecture.adoc` (CONCEPT)
  - [ ] Update `modules/deploying-models-using-distributed-inference.adoc` - add observability section
- **Acceptance criteria**:
  - [ ] Explain how llm-d extends vLLM metrics with scheduler-level insights
  - [ ] Document metrics endpoints for each component: EPP, prefill workers, decode workers
  - [ ] Describe the relationship between vLLM metrics and llm-d routing metrics
  - [ ] Explain how prefix cache awareness is reflected in metrics
  - [ ] Reference the architecture diagram if available
  - [ ] Link to metrics reference and PromQL queries
- **References**:
  - [llm-d observability blog](https://www.redhat.com/en/blog/tokens-caches-how-llm-d-improves-llm-observability-red-hat-openshift-ai-3.0): Architecture overview
  - [What is llm-d?](https://www.redhat.com/en/topics/ai/what-is-llm-d): High-level explanation
  - [Accelerate multi-turn workloads](https://developers.redhat.com/articles/2026/01/13/accelerate-multi-turn-workloads-llm-d): Use case and architecture
  - `/Users/ocbrown/opendatahub-documentation/modules/deploying-models-using-distributed-inference.adoc`: Existing llm-d deployment docs

## Module Impact Summary

### New Modules Required

| Module name | Type | Related requirement | References |
|-------------|------|---------------------|------------|
| `ref-llm-d-metrics.adoc` | REFERENCE | REQ-001 | [RHAISTRAT-1206](https://issues.redhat.com/browse/RHAISTRAT-1206), [PromQL Gist](https://gist.github.com/sallyom/375d7bbfc33270c5791b0ac0430b6998) |
| `ref-llm-d-promql-queries.adoc` | REFERENCE | REQ-002 | [PromQL Gist](https://gist.github.com/sallyom/375d7bbfc33270c5791b0ac0430b6998) |
| `proc-configuring-servicemonitor-llm-d.adoc` | PROCEDURE | REQ-003 | [RHAISTRAT-1206](https://issues.redhat.com/browse/RHAISTRAT-1206), `modules/collecting-metrics-from-user-workloads.adoc` |
| `proc-creating-llm-d-dashboard.adoc` | PROCEDURE | REQ-004 | [PromQL Gist](https://gist.github.com/sallyom/375d7bbfc33270c5791b0ac0430b6998), `modules/deploying-vllm-gpu-metrics-dashboard-grafana.adoc` |
| `con-llm-d-observability-architecture.adoc` | CONCEPT | REQ-005 | [llm-d observability blog](https://www.redhat.com/en/blog/tokens-caches-how-llm-d-improves-llm-observability-red-hat-openshift-ai-3.0) |

### Modules Requiring Updates

| Module name | Changes needed | Related requirement | References |
|-------------|----------------|---------------------|------------|
| `assemblies/managing-and-monitoring-models.adoc` | Add includes for llm-d metrics and PromQL queries | REQ-001, REQ-002 | Existing assembly structure |
| `assemblies/managing-observability.adoc` | Add include for ServiceMonitor configuration | REQ-003 | Existing observability assembly |
| `modules/deploying-vllm-gpu-metrics-dashboard-grafana.adoc` | Add variant for llm-d dashboard or reference new procedure | REQ-004 | Existing Grafana procedure |
| `modules/deploying-models-using-distributed-inference.adoc` | Add observability section with architecture concept | REQ-005 | Existing llm-d deployment docs |

## Breaking Changes

None identified. This is additive documentation for an existing feature (llm-d) that previously lacked comprehensive monitoring documentation.

## Notes

### Documentation Gap Analysis

**Current State**:
- ODH documentation has comprehensive vLLM metrics reference (`ref-vllm-metrics.adoc`)
- Existing procedures for deploying Grafana dashboards for vLLM
- General User Workload Monitoring documentation exists
- llm-d deployment procedures exist but lack observability guidance

**Gaps Identified by JIRA-1206**:
- No llm-d-specific metrics reference (scheduler, EPP, routing metrics)
- No PromQL query examples for llm-d monitoring use cases
- No ServiceMonitor configuration guide specific to llm-d
- No concept documentation explaining llm-d observability architecture

### Target Audiences

1. **Data Scientists**: Need to understand model performance through TTFT, TPT, cache hit rates
2. **Platform Administrators**: Need to monitor resource utilization (GPU, KV cache, request queues)
3. **SRE Teams**: Need to create dashboards, set up alerts, troubleshoot performance issues

### Metric Naming Considerations

The PromQL gist notes two metric naming conventions:
- **Older deployments**: `inference_model_*` prefix
- **Newer deployments**: `inference_objective_*` prefix

Documentation must address this variation and provide guidance on which metrics to use based on deployment version.

### Missing Metrics Requiring Workarounds

The PromQL gist identifies metrics that are not currently instrumented:
- **Cache eviction rate**: No metrics track when cache entries are evicted
- **Prefix cache memory usage (absolute)**: Only percentage utilization available
- **KV cache transfer times**: No metrics for P/D disaggregation transfer latency

Documentation should note these limitations and provide workaround guidance (e.g., monitoring cache hit rate trends to infer eviction pressure).

### Dependencies

**Prerequisites for users**:
- User Workload Monitoring must be enabled by cluster admin
- Grafana instance must be deployed (if using dashboards)
- llm-d deployment must be active with metrics endpoints exposed

**Documentation dependencies**:
- This work builds on existing observability documentation
- Should reference existing vLLM metrics where llm-d extends vLLM
- Must align with AsciiDoc modular documentation standards

## Sources Consulted

### JIRA Tickets
- [RHAISTRAT-1206](https://issues.redhat.com/browse/RHAISTRAT-1206): Primary requirement source

### Code and Configuration
- [PromQL Examples Gist](https://gist.github.com/sallyom/375d7bbfc33270c5791b0ac0430b6998): Comprehensive PromQL queries for llm-d monitoring
- Google Doc (internal, access restricted): Metrics list under "llm-d Components tab"

### Existing ODH Documentation
- `modules/ref-vllm-metrics.adoc`: Existing vLLM metrics reference
- `modules/deploying-vllm-gpu-metrics-dashboard-grafana.adoc`: Grafana deployment procedure
- `modules/collecting-metrics-from-user-workloads.adoc`: User Workload Monitoring setup
- `modules/deploying-models-using-distributed-inference.adoc`: llm-d deployment overview
- `assemblies/managing-observability.adoc`: Observability assembly structure
- `assemblies/managing-and-monitoring-models.adoc`: Model monitoring assembly

### Upstream and External Documentation
- [llm-d GitHub Repository](https://github.com/llm-d/llm-d): Source code and architecture
- [llm-d Official Site](https://llm-d.ai/): Product overview
- [vLLM Metrics Documentation](https://docs.vllm.ai/en/latest/design/metrics/): Upstream metric definitions
- [vLLM Prometheus/Grafana Example](https://docs.vllm.ai/en/v0.7.2/getting_started/examples/prometheus_grafana.html): Integration guide

### Red Hat Documentation and Blog Posts
- [Redefining LLM observability with llm-d in Red Hat OpenShift AI 3.0](https://www.redhat.com/en/blog/tokens-caches-how-llm-d-improves-llm-observability-red-hat-openshift-ai-3.0): Architecture and observability overview
- [Accelerate multi-turn LLM workloads on OpenShift AI with llm-d intelligent routing](https://developers.redhat.com/articles/2026/01/13/accelerate-multi-turn-workloads-llm-d): Use case and performance data
- [What is llm-d?](https://www.redhat.com/en/topics/ai/what-is-llm-d): High-level product explanation
- [Getting started with llm-d for distributed AI inference](https://developers.redhat.com/articles/2025/08/19/getting-started-llm-d-distributed-ai-inference): Deployment guide

### OpenShift Monitoring Documentation
- [User Workload Monitoring Enhancement](https://github.com/openshift/enhancements/blob/master/enhancements/monitoring/user-workload-monitoring.md): Architecture and design
- [Monitoring your own services](https://docs.redhat.com/en/documentation/openshift_container_platform/4.3/html/monitoring/monitoring-your-own-services): ServiceMonitor configuration
- [How to monitor workloads using OpenShift monitoring stack](https://developers.redhat.com/articles/2023/08/08/how-monitor-workloads-using-openshift-monitoring-stack): Practical guide

### Community Resources
- [Monitoring vLLM Inference Servers: A Quick and Easy Guide](https://www.dataunboxed.io/blog/monitoring-vllm-inference-servers-a-quick-and-easy-guide): Community best practices
- [Building Production-Ready Observability for vLLM](https://medium.com/ibm-data-ai/building-production-ready-observability-for-vllm-a2f4924d3949): Production considerations

## Next Steps - Invoke docs-writer

The following modules need to be drafted. Invoke the docs-writer agent for each:

1. **ref-llm-d-metrics.adoc** (REFERENCE)
   - Requirement: REQ-001
   - Summary: Comprehensive reference of llm-d-specific metrics including scheduler, EPP, and routing metrics
   - Save to: /Users/ocbrown/opendatahub-documentation/.claude_docs/drafts/ref-llm-d-metrics.adoc

2. **ref-llm-d-promql-queries.adoc** (REFERENCE)
   - Requirement: REQ-002
   - Summary: Ready-to-use PromQL queries organized by monitoring objective (Tier 1 and Tier 2)
   - Save to: /Users/ocbrown/opendatahub-documentation/.claude_docs/drafts/ref-llm-d-promql-queries.adoc

3. **proc-configuring-servicemonitor-llm-d.adoc** (PROCEDURE)
   - Requirement: REQ-003
   - Summary: Step-by-step procedure for creating ServiceMonitor to expose llm-d metrics
   - Save to: /Users/ocbrown/opendatahub-documentation/.claude_docs/drafts/proc-configuring-servicemonitor-llm-d.adoc

4. **proc-creating-llm-d-dashboard.adoc** (PROCEDURE)
   - Requirement: REQ-004
   - Summary: Procedure for creating Grafana dashboard with llm-d metrics panels
   - Save to: /Users/ocbrown/opendatahub-documentation/.claude_docs/drafts/proc-creating-llm-d-dashboard.adoc

5. **con-llm-d-observability-architecture.adoc** (CONCEPT)
   - Requirement: REQ-005
   - Summary: Explain llm-d observability architecture and how metrics are exposed from components
   - Save to: /Users/ocbrown/opendatahub-documentation/.claude_docs/drafts/con-llm-d-observability-architecture.adoc

Invoke docs-writer agents in parallel for efficiency.
