# Reproduction Scripts - Complete Pipeline

This directory contains all scripts needed to reproduce the complete benchmark from scratch.

## 📊 Complete Reproduction Pipeline

```
Input Data → Benchmark → Evaluate → Merge → Analyze → Figures → Paper
```

## Scripts Organization

### `reproduction/` - Main Reproduction Scripts (24 scripts)

All essential scripts to reproduce results are in **scripts/reproduction/**

#### Stage 1: Benchmarking (Generate AI Responses)

| Script | Purpose | Output |
|--------|---------|--------|
| `run_falsereject_benchmark.py` | Run Phase 3 (24 FalseReject questions) | `results/falsereject_benchmark_*.json` |
| `run_all_abliterated_benchmarks.py` | Run all 3 phases for ablated models | Multiple abliterated result files |

**Note**: benchmark_async.py and phase2_benchmark_hybrid.py are in scripts_backup/ if needed

#### Stage 2: Evaluation (Score Responses)

| Script | Purpose | Output |
|--------|---------|--------|
| `create_phase2_batch_evaluation.py` | Prepare Phase 2 for batch eval | Batch eval input file |
| `prepare_abliterated_phase1_eval.py` | Prepare ablated Phase 1 for eval | Batch eval input file |
| `prepare_abliterated_batch_eval.py` | Prepare ablated batch eval | Batch eval input file |
| `submit_batch_eval.py` | Submit to OpenAI Batch API | Batch job IDs |
| `download_all_models_batch_evals.py` | Download completed batch evals | Evaluation score files |

#### Stage 3: Merge & Clean

| Script | Purpose | Output |
|--------|---------|--------|
| `merge_phase1_evaluation_scores.py` | Merge Phase 1 eval scores | `results/phase1_all_models_eval_scores.json` |
| `merge_phase2_evaluation_scores.py` | Merge Phase 2 eval scores | `results/phase2_all_models_eval_scores.json` |
| `merge_all_models_evaluations.py` | Merge all evaluations | Final merged files |
| `deep_dive_evaluation_analysis.py` | Analyze evaluation quality | Analysis reports |

#### Stage 4: Generate Figures

| Script | Purpose | Output |
|--------|---------|--------|
| `generate_final_comprehensive_figures.py` | Generate all 5 paper figures | `figures/figure1-5.pdf` |
| `generate_final_paper_figures.py` | Alternative figure generation | Paper figures |
| `regenerate_all_figures.py` | Regenerate with updated data | Updated figures |

**Best to use**: `generate_final_comprehensive_figures.py`

### `archive/` - Old/Historical Scripts

Archived scripts from development process. Not needed for reproduction but kept for reference.

### `archive/huggingface/` - HuggingFace Upload Scripts

Scripts used to upload dataset to HuggingFace. Data already uploaded, so these are archived.

---

## 🚀 Quick Reproduction Guide

### Prerequisites

```bash
# Install dependencies
pip install openai anthropic pandas numpy matplotlib seaborn scipy

# Set API keys
export OPENAI_API_KEY="your-key-here"
export OPENROUTER_API_KEY="your-key-here"
```

### Step-by-Step Reproduction

```bash
cd /Users/marvin/legal-llm-benchmark

# Step 1: Run benchmarks (optional - results already in repo)
python3 scripts/reproduction/run_falsereject_benchmark.py
python3 scripts/reproduction/run_all_abliterated_benchmarks.py

# Step 2: Evaluate responses (optional - evals already in repo)
python3 scripts/reproduction/create_phase2_batch_evaluation.py
python3 scripts/reproduction/submit_batch_eval.py
# Wait for batch completion...
python3 scripts/reproduction/download_all_models_batch_evals.py

# Step 3: Merge evaluations (optional - merged files already in repo)
python3 scripts/reproduction/merge_phase1_evaluation_scores.py
python3 scripts/reproduction/merge_phase2_evaluation_scores.py
python3 scripts/reproduction/merge_all_models_evaluations.py

# Step 4: Generate figures (can run this to recreate figures)
python3 scripts/reproduction/generate_final_comprehensive_figures.py
```

### Output Files

After running the complete pipeline:

- `results/phase1_responses.json` (1,200 responses)
- `results/phase2_responses.json` (468 responses)
- `results/phase3_responses.json` (240 responses)
- `results/*_eval_scores.json` (evaluation details)
- `figures/figure1-5.pdf` (paper figures)

---

## 📝 Notes

### API Keys

**IMPORTANT**: All scripts expect API keys from environment variables:
- `OPENAI_API_KEY` - For OpenAI models
- `OPENROUTER_API_KEY` - For other models via OpenRouter
- `ANTHROPIC_API_KEY` - For Claude (if using direct API)

**No API keys are hardcoded in scripts** - they must be set as environment variables.

### Cost Estimates

Running the complete benchmark from scratch:
- Phase 1 (100 questions × 12 models): ~$50-100
- Phase 2 (39 contracts × 12 models): ~$30-50
- Phase 3 (24 questions × 10 models): ~$10-20
- Evaluations (via OpenAI Batch API): ~$20-30

**Total estimated cost**: ~$110-200

### Time Estimates

- Benchmarking: 2-4 hours (with retries)
- Batch evaluation: 12-24 hours (OpenAI processing time)
- Merging & figures: 10-30 minutes

---

## 🔍 Troubleshooting

### API Rate Limits

If you hit rate limits, the retry scripts will automatically retry failed requests:
- Wait a few minutes between retries
- Use batch API for evaluations to avoid rate limits

### Missing Dependencies

```bash
pip install openai anthropic pandas numpy matplotlib seaborn scipy python-dotenv
```

### File Not Found Errors

Make sure you're running scripts from the repository root:
```bash
cd /Users/marvin/legal-llm-benchmark
python3 scripts/reproduction/script_name.py
```

---

## 📚 Additional Resources

- **Data Organization**: See `DATA_ORGANIZATION.md`
- **Repository Structure**: See `REPO_STRUCTURE.md`
- **Paper**: See `paper/main.pdf`
- **HuggingFace Dataset**: https://huggingface.co/datasets/marvintong/legal-llm-benchmark

---

**Last Updated**: November 12, 2025
**Repository**: https://github.com/marvintong/legal-llm-benchmark
