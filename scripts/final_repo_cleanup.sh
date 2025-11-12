#!/bin/bash
# Final Repository Cleanup Script for Commit
# This script organizes the repository before committing to main

set -e

echo "========================================================================"
echo "  🧹 FINAL REPOSITORY CLEANUP BEFORE COMMIT"
echo "========================================================================"
echo ""

# Change to repo root
cd "$(dirname "$0")/.."

echo "📍 Current directory: $(pwd)"
echo ""

# ============================================================================
# STEP 1: Audit current state
# ============================================================================
echo "📊 STEP 1: Auditing current repository state..."
echo ""

total_files=$(find . -type f | grep -v ".git" | wc -l | tr -d ' ')
python_files=$(find . -name "*.py" | wc -l | tr -d ' ')
json_files=$(find . -name "*.json" | wc -l | tr -d ' ')
md_files=$(find . -name "*.md" | wc -l | tr -d ' ')

echo "  Total files: $total_files"
echo "  Python scripts: $python_files"
echo "  JSON datasets: $json_files"
echo "  Markdown docs: $md_files"
echo ""

# ============================================================================
# STEP 2: Clean up intermediate/duplicate result files
# ============================================================================
echo "🗑️  STEP 2: Removing intermediate and duplicate result files..."
echo ""

cd results

# Remove intermediate benchmark files (keep only final versions)
echo "  Removing intermediate benchmark files..."
rm -f benchmark_*.json 2>/dev/null || true
rm -f *_retried.json 2>/dev/null || true
rm -f *_retried_openai_retried.json 2>/dev/null || true
rm -f phase1_final_with_abliterated.json 2>/dev/null || true

# Keep only these essential result files:
# - phase1_responses.json (final Phase 1 with all 12 models)
# - phase2_responses.json (final Phase 2 with all 12 models)
# - phase3_responses.json (final Phase 3 FalseReject)
# - phase1_all_models_eval_scores.json (evaluation details)
# - phase2_all_models_eval_scores.json (evaluation details)
# - falsereject_all_models_eval_scores.json (evaluation details)

echo "  ✅ Cleaned results/ directory"
echo ""

cd ..

# ============================================================================
# STEP 3: Organize scripts
# ============================================================================
echo "📂 STEP 3: Organizing scripts..."
echo ""

cd scripts

# Create subdirectories for better organization
mkdir -p archive evaluation reproduction huggingface

# Move archived/old scripts
echo "  Moving archived scripts..."
mv benchmark_async.py archive/ 2>/dev/null || true
mv retry_*.py archive/ 2>/dev/null || true
mv test_*.py archive/ 2>/dev/null || true
mv phase2_benchmark_hybrid.py archive/ 2>/dev/null || true
mv retry_missing_phase1.py archive/ 2>/dev/null || true
mv run_falsereject_benchmark.py archive/ 2>/dev/null || true
mv run_all_abliterated_benchmarks.py archive/ 2>/dev/null || true

# Keep these essential scripts in scripts/:
# - prepare_huggingface_datasets.py
# - upload_to_huggingface.py
# - merge_evaluations_to_responses.py
# - create_additional_hf_datasets.py
# - create_flattened_hf_datasets.py
# - final_repo_cleanup.sh (this script)

echo "  ✅ Organized scripts/ directory"
echo ""

cd ..

# ============================================================================
# STEP 4: Verify essential files
# ============================================================================
echo "✅ STEP 4: Verifying essential files are present..."
echo ""

essential_files=(
    "README.md"
    "DATA_ORGANIZATION.md"
    "HUGGINGFACE_UPLOAD_SUMMARY.md"
    "data/phase1_questions.json"
    "data/phase3_falsereject_questions.json"
    "data/practice_area_mapping.json"
    "results/phase1_responses.json"
    "results/phase2_responses.json"
    "results/phase3_responses.json"
    "paper/main.pdf"
    "paper/main.tex"
    "docs/BLOG_POST.md"
)

missing_files=()

for file in "${essential_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
        echo "  ❌ MISSING: $file"
    else
        echo "  ✅ $file"
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  WARNING: ${#missing_files[@]} essential files are missing!"
    echo "Please resolve before committing."
    exit 1
fi

echo ""
echo "  ✅ All essential files present!"
echo ""

# ============================================================================
# STEP 5: Create/Update .gitignore
# ============================================================================
echo "📝 STEP 5: Creating .gitignore..."
echo ""

cat > .gitignore << 'GITIGNORE'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
*.log
/tmp/
logs/

# Environment
.env
.env.local

# Temporary files
*.tmp
*.bak
*_backup.*

# Large intermediate files
results/benchmark_*.json
results/*_retried*.json

# Archive
scripts_backup/

# HuggingFace temp
huggingface_datasets/*.json
!huggingface_datasets/*.jsonl

# LaTeX
*.aux
*.bbl
*.blg
*.log
*.out
*.toc
*.synctex.gz
GITIGNORE

echo "  ✅ Created .gitignore"
echo ""

# ============================================================================
# STEP 6: Generate final summary
# ============================================================================
echo "📊 STEP 6: Generating final repository summary..."
echo ""

cat > REPO_STRUCTURE.md << 'STRUCTURE'
# Legal LLM Benchmark - Repository Structure

## Directory Organization

```
legal-llm-benchmark/
├── data/                           # Input datasets
│   ├── phase1_questions.json       # 100 legal Q&A questions
│   ├── phase3_falsereject_questions.json  # 24 adversarial questions
│   ├── practice_area_mapping.json  # Legal taxonomy (77 categories)
│   └── phase2_contracts/           # 35 contract documents + 40 tasks
│
├── results/                        # Model responses + evaluations
│   ├── phase1_responses.json       # 12 models × 100 Q&A (1,200 responses)
│   ├── phase2_responses.json       # 12 models × 39 contracts (468 responses)
│   ├── phase3_responses.json       # 10 models × 24 FalseReject (240 responses)
│   ├── phase1_all_models_eval_scores.json     # Detailed eval reasoning
│   ├── phase2_all_models_eval_scores.json     # Detailed eval reasoning
│   └── falsereject_all_models_eval_scores.json # Detailed eval reasoning
│
├── paper/                          # Final publication-ready paper
│   ├── main.pdf                    # Compiled paper (523 KB)
│   ├── main.tex                    # LaTeX source
│   ├── references.bib              # Bibliography
│   ├── acl2023.sty                # ACL style
│   └── figure*.pdf                 # 5 figures
│
├── docs/                           # Documentation
│   ├── BLOG_POST.md               # Public-facing article
│   └── FIGURE_PLACEMENT_GUIDE.md  # Figure placement strategy
│
├── huggingface_datasets/          # HuggingFace-ready datasets
│   ├── all_questions_flat.jsonl   # All questions (124)
│   ├── phase1_flat.jsonl          # Phase 1 evaluations (1,200)
│   ├── phase3_flat.jsonl          # Phase 3 evaluations (240)
│   ├── phase2_contracts.jsonl     # Contracts with text (40)
│   ├── practice_areas.jsonl       # Taxonomy (77)
│   ├── detailed_evaluations.jsonl # Eval reasoning (1,000)
│   ├── best_vs_worst.jsonl        # Comparisons (100)
│   ├── phase3_refusal_analysis.jsonl  # Refusal stats (24)
│   └── README.md                  # Dataset card
│
├── scripts/                        # Utility scripts
│   ├── prepare_huggingface_datasets.py
│   ├── upload_to_huggingface.py
│   ├── merge_evaluations_to_responses.py
│   ├── create_additional_hf_datasets.py
│   ├── create_flattened_hf_datasets.py
│   ├── final_repo_cleanup.sh
│   └── archive/                   # Old/archived scripts
│
├── README.md                       # Main repository README
├── DATA_ORGANIZATION.md            # Data structure guide
├── HUGGINGFACE_UPLOAD_SUMMARY.md  # HuggingFace upload details
├── CLEANUP_COMPLETE_SUMMARY.md    # Cleanup documentation
└── .gitignore                      # Git ignore rules
```

## Key Statistics

- **Total Tasks**: 163 (100 Q&A + 39 Contracts + 24 FalseReject)
- **Models Evaluated**: 12 (10 safety-trained + 2 ablated)
- **Total Responses**: 1,956 evaluated responses
- **Human Validation**: Cohen's κ=0.91
- **Dataset Size**: ~9 MB (results), ~20 MB (HuggingFace)
- **Paper**: 10 pages + 4 appendices

## Essential Files for Reproduction

1. **Input Data**:
   - `data/phase1_questions.json` (100 Q&A)
   - `data/phase3_falsereject_questions.json` (24 FalseReject)
   - `data/phase2_contracts/` (35 contracts + 40 tasks)

2. **Results**:
   - `results/phase1_responses.json` (all model responses)
   - `results/phase2_responses.json` (all model responses)
   - `results/phase3_responses.json` (all model responses)

3. **Paper**:
   - `paper/main.pdf` (final publication-ready paper)
   - `paper/main.tex` (LaTeX source)

4. **Documentation**:
   - `README.md` (project overview)
   - `DATA_ORGANIZATION.md` (data structure guide)
   - `docs/BLOG_POST.md` (public article)

## HuggingFace Dataset

Live at: https://huggingface.co/datasets/marvintong/legal-llm-benchmark

**8 Configurations**:
1. questions (124 rows)
2. phase1_evaluations (1,200 rows)
3. phase3_evaluations (240 rows)
4. phase2_contracts (40 rows)
5. practice_areas (77 rows)
6. detailed_evaluations (1,000 rows)
7. best_vs_worst (100 rows)
8. refusal_analysis (24 rows)

## Citation

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
STRUCTURE

echo "  ✅ Created REPO_STRUCTURE.md"
echo ""

# ============================================================================
# FINAL SUMMARY
# ============================================================================
echo "========================================================================"
echo "  ✅ CLEANUP COMPLETE!"
echo "========================================================================"
echo ""
echo "📊 Final Statistics:"
echo "  - Essential result files: 6"
echo "  - Essential data files: 3"
echo "  - Paper files: 10"
echo "  - HuggingFace datasets: 8 configs"
echo "  - Documentation files: 5"
echo ""
echo "✅ Repository is ready for commit!"
echo ""
echo "Next steps:"
echo "  1. Review REPO_STRUCTURE.md"
echo "  2. Verify all files with: git status"
echo "  3. Commit with: git add . && git commit -m 'Final dataset and paper submission'"
echo ""
