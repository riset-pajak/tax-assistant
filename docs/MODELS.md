# Models

## Embedding
`multilingual-e5-large-instruct`

## Reranker
`bge-reranker-v2-m3`

## LLM Baseline
`cpatonn/Qwen3-Coder-30B-A3B-Instruct-AWQ-4bit`

## Runtime
Ollama on compute plane.

## Compatibility Rule
Before deployment, verify that each model is actually supported by the selected Ollama/runtime path. Do not silently replace models.

Model names must be configurable, not hard-coded.
