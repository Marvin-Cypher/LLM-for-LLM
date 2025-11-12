---
license: mit
task_categories:
- text-generation
- question-answering  
- text-classification
language:
- en
tags:
- legal
- llm-evaluation
- safety
- over-refusal
- benchmark
size_categories:
- 1K<n<10K
pretty_name: Legal LLM Benchmark
configs:
- config_name: questions
  data_files: all_questions_flat.jsonl
- config_name: phase1_evaluations
  data_files: phase1_flat.jsonl
- config_name: phase3_evaluations
  data_files: phase3_flat.jsonl
- config_name: phase2_contracts
  data_files: phase2_contracts.jsonl
- config_name: practice_areas
  data_files: practice_areas.jsonl
- config_name: detailed_evaluations
  data_files: detailed_evaluations.jsonl
- config_name: best_vs_worst
  data_files: best_vs_worst.jsonl
- config_name: refusal_analysis
  data_files: phase3_refusal_analysis.jsonl
---

# Legal LLM Benchmark Dataset

**Safety-Utility Trade-offs in Legal AI: An LLM Evaluation Across 12 Models**

[![Dataset on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/dataset-on-hf-sm.svg)](https://huggingface.co/datasets/marvintong/legal-llm-benchmark)

## Quick Start

```python
from datasets import load_dataset

# Core datasets
questions = load_dataset("marvintong/legal-llm-benchmark", "questions")
phase1_evals = load_dataset("marvintong/legal-llm-benchmark", "phase1_evaluations")
phase3_evals = load_dataset("marvintong/legal-llm-benchmark", "phase3_evaluations")

# Additional helpful datasets
contracts = load_dataset("marvintong/legal-llm-benchmark", "phase2_contracts")
practice_areas = load_dataset("marvintong/legal-llm-benchmark", "practice_areas")
detailed_evals = load_dataset("marvintong/legal-llm-benchmark", "detailed_evaluations")
best_vs_worst = load_dataset("marvintong/legal-llm-benchmark", "best_vs_worst")
refusal_analysis = load_dataset("marvintong/legal-llm-benchmark", "refusal_analysis")
```

## Dataset Description

This benchmark evaluates **12 Large Language Models** across **163 legal tasks** to measure the critical safety-utility tradeoff in production AI systems.

### Key Findings

- **Safety Paradox**: Safety-trained models achieve 87% higher quality (8.5 vs 4.6/10) but 58% higher refusal rates
- **Catastrophic Over-Refusal**: 2 widely-used models refuse 87-96% of legitimate legal questions
  - **GPT-OSS-120B**: 95.8% false positive rate
  - **O3-Mini**: 87.5% false positive rate
- **Human Validation**: Cohen's κ=0.91 [95% CI: 0.84, 0.98]
- **Statistical Rigor**: ANOVA F=142.3, η²=0.93; Spearman ρ=0.82; 5 robustness checks

## Dataset Configs

### Core Evaluation Datasets

| Config | Rows | Description |
|--------|------|-------------|
| **questions** | 124 | All Phase 1 + Phase 3 questions (legal Q&A + FalseReject) |
| **phase1_evaluations** | 1,200 | 12 models × 100 Q&A with quality scores ⭐ |
| **phase3_evaluations** | 240 | 10 models × 24 FalseReject with refusal labels 🚨 |

### Additional Helpful Datasets

| Config | Rows | Description |
|--------|------|-------------|
| **phase2_contracts** | 40 | Contract analysis tasks with embedded contract text (35 real contracts) 📄 |
| **practice_areas** | 77 | Legal practice area taxonomy (10 major categories) 📚 |
| **detailed_evaluations** | 1,000 | Detailed evaluation reasoning for Phase 1 responses 📊 |
| **best_vs_worst** | 100 | Best vs worst response comparisons per question 🏆 |
| **refusal_analysis** | 24 | Question-level refusal statistics across models 🚨 |

## Use Cases

### For Researchers

**1. Test Your Own Model**
```python
# Get questions only
questions = load_dataset("marvintong/legal-llm-benchmark", "questions")
for q in questions['train']:
    response = your_model.generate(q['question'])
    # Evaluate against our rubric
```

**2. Analyze Contract Understanding**
```python
# Get contracts with tasks
contracts = load_dataset("marvintong/legal-llm-benchmark", "phase2_contracts")
for contract in contracts['train']:
    print(f"Task: {contract['task_title']}")
    print(f"Contract length: {contract['contract_length']} chars")
    # Test document-grounded reasoning
```

**3. Study Safety Calibration**
```python
# Analyze refusal patterns
refusals = load_dataset("marvintong/legal-llm-benchmark", "refusal_analysis")
for row in refusals['train']:
    print(f"Question: {row['question'][:100]}...")
    print(f"Refusal rate: {row['refusal_rate']}%")
    print(f"Models refusing: {row['models_refusing']}")
```

### For Educators

**4. Best vs Worst Examples**
```python
# Show students quality differences
comparisons = load_dataset("marvintong/legal-llm-benchmark", "best_vs_worst")
for comp in comparisons['train'][:5]:
    print(f"\nQuestion: {comp['question']}")
    print(f"Best ({comp['best_model']}): {comp['best_score']}/10")
    print(f"Worst ({comp['worst_model']}): {comp['worst_score']}/10")
    print(f"Gap: {comp['score_gap']}")
```

**5. Understand Legal Practice Areas**
```python
# Explore legal domain coverage
areas = load_dataset("marvintong/legal-llm-benchmark", "practice_areas")
for area in areas['train']:
    print(f"{area['major_category']} → {area['subcategory']}")
# Output: 77 distinct legal practice areas across 10 categories
```

## Data Fields

### Core Datasets

**`questions` Config**
- `id`, `question`, `category`, `difficulty`, `expected_behavior`, `phase`

**`phase1_evaluations` and `phase3_evaluations` Configs**
- `question_id`, `question`, `category`, `model`
- `response` (full text)
- `score` (0-10), `appropriateness_score`, `actionability_score`
- `is_refusal` (bool), `refusal_type`, `contains_harmful`

### Additional Datasets

**`phase2_contracts` Config** (40 rows)
- `task_id`, `contract_id`, `task_type`, `task_title`
- `instruction` (what to do)
- `contract_text` (full contract document text)
- `contract_length` (character count)
- `evaluation_criteria` (rubric items)

**`practice_areas` Config** (77 rows)
- `major_category` (e.g., "Corporate & Business Law")
- `subcategory` (e.g., "contract_drafting")
- `category_id` (unique identifier)

**`detailed_evaluations` Config** (1,000 rows)
- `question_index`, `model`
- `appropriateness_score`, `appropriateness_reasoning`
- `actionability_score`, `actionability_reasoning`
- `refusal_type`, `has_specific_steps`, `has_concrete_examples`

**`best_vs_worst` Config** (100 rows)
- `question_id`, `question`, `category`
- `best_model`, `best_score`, `best_response`
- `worst_model`, `worst_score`, `worst_response`
- `has_refusal_example`, `refusal_model`, `refusal_response`
- `score_gap` (difference between best and worst)

**`refusal_analysis` Config** (24 rows)
- `question_id`, `question`
- `total_models`, `refusals_count`, `answers_count`
- `refusal_rate` (%)
- `models_refusing` (comma-separated list)
- `models_answering` (comma-separated list)

## Example: Detailed Evaluation Reasoning

```python
from datasets import load_dataset

# Load detailed evaluations with reasoning
detailed = load_dataset("marvintong/legal-llm-benchmark", "detailed_evaluations")

# Find GPT-5's evaluation for question 0
gpt5_eval = [r for r in detailed['train'] if r['model'] == 'openai/gpt-5' and r['question_index'] == 0][0]

print(f"Appropriateness Score: {gpt5_eval['appropriateness_score']}/10")
print(f"Reasoning: {gpt5_eval['appropriateness_reasoning']}")
print(f"\nActionability Score: {gpt5_eval['actionability_score']}/10")
print(f"Reasoning: {gpt5_eval['actionability_reasoning']}")
```

## Models Evaluated

### Safety-Trained Models (10)

1. **openai/gpt-5** - Top performer: 9.17/10 quality, **0% false refusal** ✅
2. anthropic/claude-sonnet-4.5
3. deepseek/deepseek-chat
4. zhipuai/glm-4-plus - Best balance: 8.2/10 quality, 62.5% non-refusal
5. qwen/qwen-2.5-72b-instruct - **0% false refusal** ✅
6. openai/gpt-4o
7. meta-llama/llama-3.3-70b-instruct
8. google/gemini-pro-1.5
9. **openai/o3-mini** - Catastrophic over-refusal: **87.5% false positive** ❌
10. **openrouter/auto (GPT-OSS-120B)** - Worst over-refusal: **95.8% false positive** ❌

### Ablated Models (2)

11. Mistral-7B-Instruct-abliterated
12. Qwen2.5-7B-Instruct-abliterated

## Paper & Citation

**Full Paper**: [GitHub Repository](https://github.com/marvintong/legal-llm-benchmark)

```bibtex
@article{legal-llm-safety-2025,
  title={Safety-Utility Trade-offs in Legal AI: An LLM Evaluation Across 12 Models},
  author={[Your Name]},
  journal={arXiv preprint arXiv:2501.XXXXX},
  year={2025},
  url={https://github.com/marvintong/legal-llm-benchmark},
  dataset={https://huggingface.co/datasets/marvintong/legal-llm-benchmark}
}
```

## License

MIT

## Contact

- **GitHub Issues**: https://github.com/marvintong/legal-llm-benchmark/issues
- **Repository**: https://github.com/marvintong/legal-llm-benchmark
