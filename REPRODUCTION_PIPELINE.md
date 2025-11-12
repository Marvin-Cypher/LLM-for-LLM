# Reproduction Pipeline - Complete Workflow

This document describes the complete pipeline to reproduce all results from scratch.

## Pipeline Overview

```
Input Data → Benchmark (AI responses) → Evaluate → Clean/Merge → Analysis → Paper
```

## Stage 1: Input Data (Already Complete)

**Location**: `data/`

Files:
- `phase1_questions.json` (100 legal Q&A)
- `phase3_falsereject_questions.json` (24 adversarial)
- `phase2_contracts/` (35 contracts + 40 tasks)

**Status**: ✅ Already in repository

---

## Stage 2: AI Benchmarking (Generate Model Responses)

**Purpose**: Query 12 LLMs with all 163 tasks

### Required Scripts:

1. **`benchmark_async.py`** - Main benchmark runner
   - Queries Phase 1 (100 Q&A questions)
   - Supports multiple model providers (OpenAI, OpenRouter, etc.)
   - Output: `results/benchmark_YYYYMMDD_HHMMSS.json`

2. **`phase2_benchmark_hybrid.py`** - Contract benchmark
   - Queries Phase 2 (39 contract tasks)
   - Handles file uploads for contract text
   - Output: `results/phase2_benchmark_YYYYMMDD.json`

3. **`run_falsereject_benchmark.py`** - FalseReject benchmark
   - Queries Phase 3 (24 adversarial questions)
   - Output: `results/falsereject_benchmark_YYYYMMDD.json`

4. **`run_all_abliterated_benchmarks.py`** - Ablated models
   - Queries ablated models for all 3 phases
   - Output: Multiple files with ablated responses

### Retry Scripts (for failed API calls):

5. **`retry_failed_requests.py`** - Retry failed OpenRouter requests
6. **`retry_openai_official.py`** - Retry failed OpenAI requests
7. **`retry_missing_phase1.py`** - Fill in missing Phase 1 responses

**Status**: Need to restore from archive/

---

## Stage 3: Evaluation (Score Responses)

**Purpose**: Evaluate all 1,956 responses for quality and refusal

### Required Scripts:

8. **`evaluate_phase1.py`** - Evaluate Phase 1 responses
   - Scores appropriateness (0-10) and actionability (0-10)
   - Detects refusals
   - Output: `results/phase1_all_models_eval_scores.json`

9. **`evaluate_phase2.py`** - Evaluate Phase 2 responses
   - Output: `results/phase2_all_models_eval_scores.json`

10. **`evaluate_phase3.py`** - Evaluate Phase 3 responses
    - Detects false positive refusals
    - Output: `results/falsereject_all_models_eval_scores.json`

**Status**: Need to check if these exist

---

## Stage 4: Data Cleaning & Merging

**Purpose**: Merge evaluations with responses, clean duplicates

### Required Scripts:

11. **`merge_evaluations_to_responses.py`** ✅ (Already in huggingface archive)
    - Merges eval scores into response files
    - Creates final phase1/2/3_responses.json

12. **`clean_and_merge_results.py`** - Clean duplicate benchmark files

**Status**: Need to restore from HuggingFace archive/

---

## Stage 5: Analysis & Figures

**Purpose**: Generate statistical analysis and figures

### Required Scripts:

13. **`generate_figures.py`** - Create all 5 paper figures
    - figure1_all_models_all_work.pdf
    - figure2_work_type_performance.pdf
    - figure3_comprehensive_heatmap.pdf
    - figure4_score_distribution.pdf
    - figure5_rejection_analysis.pdf

14. **`statistical_analysis.py`** - Run ANOVA, Spearman, robustness checks

**Status**: Need to create or find

---

## Complete Reproduction Command Sequence

```bash
# Stage 2: Benchmarking
python3 scripts/benchmark_async.py
python3 scripts/phase2_benchmark_hybrid.py
python3 scripts/run_falsereject_benchmark.py
python3 scripts/run_all_abliterated_benchmarks.py

# Retry failed requests (if needed)
python3 scripts/retry_failed_requests.py results/benchmark_*.json
python3 scripts/retry_openai_official.py results/benchmark_*_retried.json

# Stage 3: Evaluation
python3 scripts/evaluate_phase1.py
python3 scripts/evaluate_phase2.py
python3 scripts/evaluate_phase3.py

# Stage 4: Clean & Merge
python3 scripts/merge_evaluations_to_responses.py
python3 scripts/clean_and_merge_results.py

# Stage 5: Analysis
python3 scripts/generate_figures.py
python3 scripts/statistical_analysis.py
```

---

## Missing Scripts to Create/Find

1. evaluate_phase1.py
2. evaluate_phase2.py
3. evaluate_phase3.py
4. generate_figures.py
5. statistical_analysis.py
6. clean_and_merge_results.py

