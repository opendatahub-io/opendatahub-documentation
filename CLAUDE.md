# CLAUDE.md

## Working with Claude on Open Data Hub documentation

This document provides guidelines for contributors using Claude AI to help maintain and improve the AsciiDoc documentation for Open Data Hub (ODH).

## About this documentation repository

This repository contains AsciiDoc-formatted documentation for **Open Data Hub**, an open-source AI/ML platform for OpenShift. Open Data Hub serves as the upstream community project for [Red Hat OpenShift AI](https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-ai).

Open Data Hub provides a platform for developing, training, and serving AI/ML models on OpenShift Container Platform. Key components include:

- Jupyter notebook workbenches
- Model serving (KServe, ModelMesh)
- Data science pipelines
- Distributed training workloads
- Model registry
- Model observability (TrustyAI)

The documentation is published to https://opendatahub.io/docs via Read the Docs.

## Repository structure

```
opendatahub-documentation/
├── _artifacts/
│   └── document-attributes-global.adoc (global AsciiDoc attributes)
├── .github/
│   └── workflows/ (GitHub Actions CI)
├── .vale/
│   └── styles/ (Vale linting styles)
├── assemblies/ (assembly files that organize modules)
├── modules/ (reusable documentation modules)
├── images/ (image assets)
├── examples/ (code examples and notebooks)
├── scripts/ (build and validation scripts)
├── out/ (generated output directory)
│
├── [topic-name].adoc (top-level book entry points)
├── .vale.ini (Vale configuration)
├── .readthedocs.yaml (Read the Docs configuration)
└── CLAUDE.md (this file)
```

Each top-level `.adoc` file in the root directory is a book entry point that includes modules from the shared `modules/` and `assemblies/` directories.

## Key directories

| Directory | Purpose |
|-----------|---------|
| `modules/` | Reusable content modules (concepts, procedures, references) |
| `assemblies/` | Assembly files that include and organize modules |
| `_artifacts/` | Global document attributes and shared configuration |
| `images/` | Image assets |
| `examples/` | Code examples and Jupyter notebooks |
| `scripts/` | Build, validation, and link-checking scripts |

## Build and preview

**Build Tool:** Asciidoctor

**Build Command:**
```bash
./scripts/build-docs-ci.sh
```

**Build Process:**
1. Creates `out/` directory with index.html
2. Loops over each top-level `.adoc` file
3. Runs Asciidoctor with table of contents and book doctype
4. Generates static HTML to `out/[topic-name]/index.html`

**Preview:** Read the Docs generates previews for pull requests automatically.

## Git workflow

**Main Branch:** `main`

**Branch Naming:**
- Feature branches: descriptive names based on the change (e.g., `add-pipeline-docs`, `fix-kserve-instructions`)
- Issue-based branches: reference GitHub issue numbers when applicable

**Remotes:**
- `origin` - Personal fork
- `upstream` - Main repository (https://github.com/opendatahub-io/opendatahub-documentation)

**Downstream Relationship:**
- This repository is the upstream source for Red Hat OpenShift AI documentation
- Changes here flow downstream to the productized documentation at Red Hat GitLab
- Content uses the `upstream` attribute for Open Data Hub-specific values

## Effective prompts for Claude

### Documentation analysis and improvement

**Good prompts:**
- "Review this AsciiDoc file for technical accuracy and suggest improvements to clarity"
- "Help me restructure this module to follow Red Hat modular documentation standards"
- "Generate cross-references and include statements for this module"
- "Convert this content to proper AsciiDoc format with appropriate attributes"

**Include context:**
- Specify the ODH component being documented
- Mention the target audience (data scientists, administrators, developers)
- Reference the specific feature being documented

### Content generation

**For new documentation:**
```
I need to document [specific ODH feature].
Please create AsciiDoc documentation that includes:
- Overview and purpose
- Prerequisites
- Step-by-step procedure (if applicable)
- Verification steps
- Uses product attributes from _artifacts/document-attributes-global.adoc
```

### AsciiDoc-specific requests

- "Convert this content to use AsciiDoc tables instead of plain text formatting"
- "Add proper cross-references between these documentation pages using xref syntax"
- "Help me set up include statements to reuse content from assemblies/ directory"
- "Update attributes to use product names from \_artifacts/document-attributes-global.adoc"

## Best practices when using Claude

### 1. Provide repository context

Always share:
- The current AsciiDoc files you're working with
- The ODH component being documented
- Any related GitHub issues

### 2. Follow Red Hat documentation standards

- Use the Red Hat documentation style guide: https://redhat-documentation.github.io/supplementary-style-guide
- Use the Red Hat modular documentation reference guide: https://redhat-documentation.github.io/modular-docs/
- Follow established product naming conventions using attributes from `_artifacts/document-attributes-global.adoc`
- Use sentence case headings

### 3. Specify AsciiDoc requirements

Mention when you need:
- Specific AsciiDoc attributes or formatting
- Cross-module references between assemblies and modules
- Integration with the existing documentation structure

### 4. Use AsciiDoc templates

When creating new content, use the following AsciiDoc templates:

**Concept module template:**
```asciidoc
:_module-type: CONCEPT
[id="module-id_{context}"]
= Module title

[role="_abstract"]
Write a short introductory paragraph that provides an overview of the module.
The text that immediately follows the `[role="_abstract"]` tag is used for search metadata.

// Module content here
```

**Procedure module template:**
```asciidoc
:_module-type: PROCEDURE
[id="module-id_{context}"]
= Module title

[role="_abstract"]
Short introductory paragraph that provides an overview of the procedure.

.Prerequisites

* List procedure prerequisites one per bullet

.Procedure

. Start each step with an active verb.
. Use numbered steps for procedures.

.Verification

* Provide verification methods for the procedure.
```

**Reference module template:**
```asciidoc
:_module-type: REFERENCE
[id="module-id_{context}"]
= Module title

[role="_abstract"]
Short introductory paragraph that provides an overview of the reference content.

.Labeled list
Term 1:: Definition
Term 2:: Definition

.Table
[options="header"]
|====
|Column 1|Column 2|Column 3
|Row 1, column 1|Row 1, column 2|Row 1, column 3
|====
```

### 5. Request code verification

Ask Claude to:
- Verify code examples against the actual product behavior
- Check that API signatures match the implementation
- Validate that configuration examples are current

## Documentation standards for this project

### AsciiDoc conventions

- Use sentence case for headings
- Use a single heading per module
- Include `id` attributes for all major sections with `_{context}` suffix
- Use `source` blocks with appropriate language highlighting
- Include `include::` statements for reusable content
- Add `xref:` links between related documentation
- Follow the Red Hat Style supplementary guide when drafting content
- Do not use file prefixes to denote topic type (avoid `con-`, `proc-`, `ref-` prefixes)
- Use AsciiDoc description lists for discrete paragraphs focused on a single idea
- Use AsciiDoc NOTE and IMPORTANT admonitions where appropriate:

```asciidoc
[NOTE]
====
Add note content here.
====
```

```asciidoc
[IMPORTANT]
====
Add important note content here.
====
```

### Code examples

- All code examples should be tested and current
- Include both minimal and complete examples where appropriate
- Use callouts (`<1>`, `<2>`) to explain complex code
- Provide context about when/why to use each approach

### Product attributes

Always use product attributes from `_artifacts/document-attributes-global.adoc`:

| Attribute | Usage |
|-----------|-------|
| `{productname-long}` | Full product name (Open Data Hub) |
| `{productname-short}` | Short product name (Open Data Hub) |
| `{vernum}` | Product version number |
| `{odhdocshome}` | Documentation base URL |

Note: This repository uses the `upstream` attribute. The downstream Red Hat OpenShift AI repository uses `cloud-service` or `self-managed` attributes.

## Validation and linting

**Vale Configuration:** `.vale.ini`
- **Styles:** RedHat, AsciiDoc, AsciiDocDITA
- **Min Alert Level:** suggestion

**Run Vale locally:**
```bash
vale path/to/file.adoc
```

**CI/CD Validation:**
- Link checking on push and pull requests via GitHub Actions
- Uses `scripts/check-updated-books.sh` to identify affected books
- Uses `scripts/check-book-links.sh` to verify links

## Review checklist

When Claude helps generate or improve documentation:

- [ ] Technical accuracy verified against current product behavior
- [ ] AsciiDoc formatting follows project conventions
- [ ] Cross-references and includes work correctly
- [ ] Code examples are complete and tested
- [ ] Content matches the intended audience level
- [ ] Product attributes used instead of hardcoded names

## Keeping CLAUDE.md current

When working on this repository, Claude should proactively review and update CLAUDE.md to reflect changes:

- **New directories:** Update the repository structure section
- **Version updates:** Update when product versions change in `_artifacts/document-attributes-global.adoc`
- **New documentation patterns:** Document any new AsciiDoc conventions or standards
- **Deprecated content:** Remove or update references to deprecated features

## Getting help

If Claude suggests changes that seem incorrect or incomplete:
1. Verify against the actual product behavior
2. Check recent commits for changes Claude might not know about
3. Test any code examples in your development environment
4. Consult the Red Hat modular documentation guide

## Working with downstream (Red Hat OpenShift AI)

This repository is the upstream source for Red Hat OpenShift AI documentation. Content from this repository is periodically synced to the downstream productized documentation.

### Downstream relationship

- **Downstream Repository:** Red Hat GitLab (internal)
- **Product:** Red Hat OpenShift AI (cloud-service and self-managed variants)
- **Published Location:** https://docs.redhat.com/en

### Content considerations

When writing documentation:

- Focus on Open Data Hub functionality and namespaces
- Use `{productname-long}` and `{productname-short}` attributes (resolved via `upstream` ifdef)
- Downstream teams will adapt content for Red Hat-specific features and support

## Open Data Hub repositories and technologies

The following repositories under https://github.com/opendatahub-io contain the source code for Open Data Hub components. Use this reference when investigating features, troubleshooting documentation questions, or understanding component architecture.

### Core platform and management

| Repository | Purpose |
|------------|---------|
| [opendatahub-operator](https://github.com/opendatahub-io/opendatahub-operator) | Primary operator for deploying and managing all ODH components using DataScienceCluster CRD |
| [odh-dashboard](https://github.com/opendatahub-io/odh-dashboard) | Unified UI/dashboard for Open Data Hub components |
| [odh-model-controller](https://github.com/opendatahub-io/odh-model-controller) | Controller for managing model lifecycle |

### Model serving

| Repository | Purpose |
|------------|---------|
| [kserve](https://github.com/opendatahub-io/kserve) | Standardized serverless ML inference platform on Kubernetes |
| [modelmesh](https://github.com/opendatahub-io/modelmesh) | Distributed model serving management/routing layer for high-scale use cases |
| [modelmesh-serving](https://github.com/opendatahub-io/modelmesh-serving) | Controller for managing ModelMesh with runtime adapters (Triton, MLServer, OpenVINO, TorchServe) |
| [vllm-tgis-adapter](https://github.com/opendatahub-io/vllm-tgis-adapter) | Adapter for vLLM with TGIS-compatible gRPC server |
| [openvino_model_server](https://github.com/opendatahub-io/openvino_model_server) | Scalable inference server for OpenVINO-optimized models |
| [MLServer](https://github.com/opendatahub-io/MLServer) | Multi-framework inference engine supporting Python, C++, and Java clients |
| [caikit-tgis-serving](https://github.com/opendatahub-io/caikit-tgis-serving) | Caikit framework integration with TGIS gRPC server |

### Model registry

| Repository | Purpose |
|------------|---------|
| [model-registry](https://github.com/opendatahub-io/model-registry) | Central repository for storing and managing models, versions, and artifacts metadata |
| [model-registry-operator](https://github.com/opendatahub-io/model-registry-operator) | Kubernetes operator for Model Registry lifecycle management |
| [ml-metadata](https://github.com/opendatahub-io/ml-metadata) | System for recording and retrieving ML workflow metadata and lineage |

### Data science pipelines

| Repository | Purpose |
|------------|---------|
| [data-science-pipelines](https://github.com/opendatahub-io/data-science-pipelines) | Machine Learning Pipelines for Kubeflow; orchestrates complex ML workflows |
| [data-science-pipelines-operator](https://github.com/opendatahub-io/data-science-pipelines-operator) | Kubernetes operator for Data Science Pipelines lifecycle management |
| [argo-workflows](https://github.com/opendatahub-io/argo-workflows) | Container-native workflow engine for orchestrating parallel jobs on Kubernetes |
| [elyra](https://github.com/opendatahub-io/elyra) | AI-centric JupyterLab extensions including visual pipeline editor |

### Notebooks and workbenches

| Repository | Purpose |
|------------|---------|
| [notebooks](https://github.com/opendatahub-io/notebooks) | Pre-configured Jupyter notebook images (CPU, GPU/CUDA/ROCM, PyTorch, TensorFlow variants) |
| [odh-ide-extensions](https://github.com/opendatahub-io/odh-ide-extensions) | Custom JupyterLab extensions for ODH IDE enhancements |

### Distributed training and workloads

| Repository | Purpose |
|------------|---------|
| [training-operator](https://github.com/opendatahub-io/training-operator) | Kubernetes-native operator for distributed ML training (PyTorch, JAX, TensorFlow) |
| [trainer](https://github.com/opendatahub-io/trainer) | Kubeflow Trainer for scalable LLM fine-tuning with HuggingFace, DeepSpeed, Megatron-LM |
| [codeflare-operator](https://github.com/opendatahub-io/codeflare-operator) | Operator for CodeFlare distributed workload stack; manages RayCluster and AppWrapper controllers |
| [distributed-workloads](https://github.com/opendatahub-io/distributed-workloads) | Artifacts for distributed workloads (fine-tuning, image generation, hyperparameter optimization) |
| [kuberay](https://github.com/opendatahub-io/kuberay) | Toolkit to run Ray applications on Kubernetes |
| [kueue](https://github.com/opendatahub-io/kueue) | Kubernetes-native job queueing system for workload scheduling |
| [spark-operator](https://github.com/opendatahub-io/spark-operator) | Kubernetes operator for Apache Spark application management |

### LLM frameworks and infrastructure

| Repository | Purpose |
|------------|---------|
| [llama-stack](https://github.com/opendatahub-io/llama-stack) | Meta's composable framework for AI applications (inference, RAG, agents, tools, safety) |
| [llama-stack-k8s-operator](https://github.com/opendatahub-io/llama-stack-k8s-operator) | Kubernetes operator for Llama Stack lifecycle management |
| [llama-stack-demos](https://github.com/opendatahub-io/llama-stack-demos) | Demo applications for building Llama Stack-based apps on OpenShift |
| [litellm](https://github.com/opendatahub-io/litellm) | Unified interface for calling 50+ LLM APIs in OpenAI format |
| [llm-d-inference-scheduler](https://github.com/opendatahub-io/llm-d-inference-scheduler) | Inference scheduler for distributed LLM inference |

### Model observability and safety (TrustyAI)

| Repository | Purpose |
|------------|---------|
| [trustyai-service-operator](https://github.com/opendatahub-io/trustyai-service-operator) | Kubernetes operator for TrustyAI; enables explainability, fairness monitoring, drift tracking |
| [trustyai-explainability](https://github.com/opendatahub-io/trustyai-explainability) | Java toolkit for fairness metrics, explainable AI algorithms, and XAI tools |
| [fms-guardrails-orchestrator](https://github.com/opendatahub-io/fms-guardrails-orchestrator) | Orchestrator for LLM guardrailing; manages detectors for input/output safety checks |
| [guardrails-detectors](https://github.com/opendatahub-io/guardrails-detectors) | Collection of detectors for FMS Guardrails Orchestrator |
| [NeMo-Guardrails](https://github.com/opendatahub-io/NeMo-Guardrails) | Toolkit for adding programmable guardrails to LLM-based systems |
| [lm-evaluation-harness](https://github.com/opendatahub-io/lm-evaluation-harness) | Framework for few-shot evaluation and benchmarking of language models |

### Feature store and experiment tracking

| Repository | Purpose |
|------------|---------|
| [feast](https://github.com/opendatahub-io/feast) | Open source feature store for machine learning |
| [mlflow](https://github.com/opendatahub-io/mlflow) | Platform for tracking, evaluating, and managing ML models and experiments |
| [mlflow-operator](https://github.com/opendatahub-io/mlflow-operator) | Kubernetes operator for MLflow lifecycle management |

### Model optimization

| Repository | Purpose |
|------------|---------|
| [openvino](https://github.com/opendatahub-io/openvino) | Open-source toolkit for optimizing and deploying AI inference across Intel hardware |
| [openvino.genai](https://github.com/opendatahub-io/openvino.genai) | Framework to run generative AI models with C++/Python API using OpenVINO |

### Infrastructure and build

| Repository | Purpose |
|------------|---------|
| [kubeflow](https://github.com/opendatahub-io/kubeflow) | Machine Learning Toolkit for Kubernetes |
| [opendatahub-documentation](https://github.com/opendatahub-io/opendatahub-documentation) | This repository - official Open Data Hub documentation |
| [opendatahub-tests](https://github.com/opendatahub-io/opendatahub-tests) | Testing suite for OpenDataHub |
| [architecture-decision-records](https://github.com/opendatahub-io/architecture-decision-records) | Architectural Decision Records for the project |

### Technology categories summary

| Category | Key Technologies |
|----------|------------------|
| Model Serving | KServe, ModelMesh, vLLM, OpenVINO Model Server, MLServer, Caikit |
| Distributed Training | Training Operator, Kubeflow Trainer, CodeFlare, Ray, Kueue, Spark |
| Pipelines | Data Science Pipelines (Kubeflow Pipelines), Argo Workflows, Elyra |
| Notebooks | JupyterLab with custom ODH extensions |
| LLM Infrastructure | Llama Stack, LiteLLM, vLLM adapters |
| Model Safety | TrustyAI, FMS Guardrails, NeMo Guardrails |
| Feature Store | Feast |
| Experiment Tracking | MLflow |
| Model Registry | Kubeflow Model Registry |

## Version compatibility

This documentation repository tracks:
- **Project:** Open Data Hub
- **Website:** https://opendatahub.io
- **Documentation Format:** AsciiDoc
- **Build System:** Asciidoctor
- **Published Location:** https://opendatahub.io/docs (via Read the Docs)

Version information is maintained in `_artifacts/document-attributes-global.adoc`. Always refer to this file for current version numbers when documenting features.

**Remember: Claude is a powerful tool for documentation work, but always verify technical details against the actual product and test any code examples before publishing.**
