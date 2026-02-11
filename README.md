# AI Document Structuring Pipeline

A reliability-focused automation pipeline that converts unstructured text documents into validated structured data using both local and cloud-based Large Language Models (LLMs).

---

## Overview

This project demonstrates production-style design patterns for integrating LLMs into automated data processing workflows. The pipeline ingests raw text files, extracts structured information using configurable LLM providers, validates output against strict schemas, and produces consolidated reporting output.

The project emphasizes **reliability**, **observability**, and **provider flexibility** — key requirements in real-world applied AI systems.

---

## Features

- Multi-provider LLM support  
  - Local models via **Ollama**
  - Cloud models via **OpenAI API**

- Schema-enforced structured output validation  
- Automatic retry logic for unreliable model responses  
- Output sanitation to handle inconsistent model formatting  
- Batch file ingestion and processing  
- Config-driven runtime behavior  
- CLI-based execution  
- Structured logging for traceability  

---

## Architecture

```
Input Files
     ↓
Processor Pipeline
     ↓
LLM Provider Abstraction
     ↓
Output Sanitization
     ↓
Schema Validation
     ↓
Retry Handling
     ↓
Structured Output + Reporting
```

---

## Reliability Design

Large Language Model outputs are inherently non-deterministic. This project implements several defensive design strategies.

### Output Sanitization
Removes markdown formatting and extracts raw JSON from model responses to support cross-provider compatibility.

### Schema Validation
All extracted data must conform to a defined JSON schema before being accepted.

### Retry Logic
Invalid or malformed model responses trigger automatic retry attempts to improve success rates.

### Provider Abstraction
Supports both local and remote models, enabling cost optimization and fallback strategies.

---

## Project Structure

```
ai-doc-pipeline/
├── main.py              # CLI entry and orchestration
├── processor.py         # Pipeline processing logic
├── llm_client_ollama.py # Provider abstraction
├── llm_client_openai.py # Provider abstraction
├── validator.py         # JSON schema enforcement
├── logger.py            # Logging utilities
├── config.py            # Runtime configuration
├── input/               # Source documents
├── output/              # Generated structured reports
```

---

## Requirements

- Python 3.10+
- Ollama (optional for local models)
- OpenAI API key (optional for cloud models)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/RIPBozoPackwatch/DocumentStructuringUsingAI/
cd ai-doc-pipeline
```

Create virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Runtime behavior is controlled through configuration settings, including:

- Model selection
- Retry limits
- Schema definitions
- Prompt instructions

---

## Usage

Place source documents into the `input` directory, then run:

```bash
python main.py --llm-model <model_name>
```

### Example

```bash
python main.py --ollama
```

---

## Example Input

```
John Doe: My computer has become sentient.
```

---

## Example Output

```json
{
  "user_name": "John Doe",
  "issue_type": "Sentience",
  "priority": "High"
}
```

---

## Supported Providers

| Provider | Example Models |
|-----------|----------------|
| OpenAI | gpt-4.1-mini |
| Ollama | llama3.1:8b-instruct, gemma3 |

---

## Design Tradeoffs

### Why Schema Validation?
LLMs frequently produce inconsistent or partially formatted outputs. Enforcing schemas ensures downstream reliability and predictable data contracts.

### Why Retry Instead of Repair?
Retrying with refined prompts often produces cleaner results than attempting automated correction of malformed output.

### Why Multi-Provider Support?
Local models reduce cost and improve privacy, while cloud models offer higher reliability and performance. Supporting both enables flexible deployment strategies.

---

## Potential Future Enhancements

- Automatic provider fallback strategies  
- Timeout and cancellation handling  
- Support for multiple extraction schemas  
- Metrics tracking for model accuracy and latency  
- Parallel / async processing for scalability  

---

## Purpose

This project was developed as a demonstration of applied AI integration patterns commonly used in:

- Internal automation tooling
- Platform engineering workflows
- AI-driven document processing pipelines
- Reliability-focused LLM integration systems