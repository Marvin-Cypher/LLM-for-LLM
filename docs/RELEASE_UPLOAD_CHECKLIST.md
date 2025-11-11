# GitHub Release Upload Checklist

## 📦 Files Ready for Upload (Organized by Category)

All files are prepared in `/tmp/release_upload/` organized into logical categories.

---

## 📊 Category 1: Benchmark Results (3 files, ~40 MB total)

**Upload these files with prefix: `1-results-`**

```
1-results-phase1_final.json           (Phase 1: 100 Q&A questions × 10 models)
1-results-phase2_final.json           (Phase 2: 39 contract tasks × 10 models)
1-results-falsereject_final.json      (FalseReject: 24 over-refusal tests × 10 models)
```

**Location**: `/tmp/release_upload/benchmark_results/`

**Description to add in Release**:
```
📊 Benchmark Results - Core evaluation data for all 10 LLMs across 163 legal tasks
```

---

## 🔍 Category 2: Evaluation Outputs (3 files, ~2.5 MB total)

**Upload these files with prefix: `2-eval-`**

```
2-eval-appropriateness_results.jsonl  (LLM-as-judge appropriateness scores)
2-eval-actionability_results.jsonl    (Actionability evaluation scores)
2-eval-appropriateness_errors.jsonl   (Evaluation error logs)
```

**Location**: `/tmp/release_upload/evaluation_outputs/`

**Description to add in Release**:
```
🔍 Evaluation Outputs - GPT-4o-mini judge scores and evaluation metadata
```

---

## 📄 Category 3: Paper & Figures (8 files, ~2 MB total)

**Upload these files with prefix: `3-paper-`**

```
3-paper-draft.md                      (Full paper in Markdown format)
3-paper-latex.tex                     (Rename from main.tex - LaTeX source)
3-paper-overleaf-package.zip          (Complete Overleaf package with all dependencies)
3-paper-figure1-model-boxplot.png     (Figure 1: Model performance boxplot)
3-paper-figure2-rejection-rates.png   (Figure 2: Rejection rate comparison)
3-paper-figure3-category-heatmap.png  (Figure 3: Performance by legal category)
3-paper-figure4-score-distribution.png (Figure 4: Score distribution analysis)
3-paper-figure5-model-rankings.png    (Figure 5: Final model rankings)
```

**Location**: `/tmp/release_upload/paper_and_figures/`

**Description to add in Release**:
```
📄 Academic Paper & Figures - Publication-ready paper draft and all visualizations (300 DPI PNG)
```

---

## 📝 Step-by-Step Upload Instructions

### 1. Go to Your Release Page
https://github.com/Marvin-Cypher/LLM-for-LLM/releases/tag/v1.0.0

### 2. Click "Edit" Button (top right)

### 3. Upload Files by Category

**Method A: Drag & Drop** (Recommended)
- Open Finder → Navigate to `/tmp/release_upload/`
- Drag each folder's contents one at a time to the "Attach binaries" section
- Rename files as you upload (add the category prefix)

**Method B: Click to Browse**
- Click "Attach binaries by dropping them here or selecting them"
- Navigate to each folder and select files
- Rename after uploading

### 4. Rename Files While Uploading

GitHub will keep original filenames. Rename them with category prefixes for organization:

**Before Upload**:
```
phase1_final.json
figure1_model_boxplot.png
```

**After Renaming in GitHub**:
```
1-results-phase1_final.json
3-paper-figure1-model-boxplot.png
```

### 5. Update Release Description

Add this section after your existing description:

```markdown

---

## 📁 Download Files by Category

### 📊 Benchmark Results
- [1-results-phase1_final.json](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/1-results-phase1_final.json) - Phase 1: 100 Q&A (23 MB)
- [1-results-phase2_final.json](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/1-results-phase2_final.json) - Phase 2: 39 Contracts (10 MB)
- [1-results-falsereject_final.json](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/1-results-falsereject_final.json) - FalseReject: 24 Tests (4 MB)

### 🔍 Evaluation Outputs
- [2-eval-appropriateness_results.jsonl](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/2-eval-appropriateness_results.jsonl) - Judge scores (2 MB)
- [2-eval-actionability_results.jsonl](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/2-eval-actionability_results.jsonl) - Actionability (500 KB)

### 📄 Academic Paper & Figures
- [3-paper-draft.md](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-draft.md) - Paper (Markdown)
- [3-paper-latex.tex](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-latex.tex) - Paper (LaTeX)
- [3-paper-overleaf-package.zip](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-overleaf-package.zip) - Complete Overleaf package
- [3-paper-figure1-model-boxplot.png](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-figure1-model-boxplot.png) - Figure 1
- [3-paper-figure2-rejection-rates.png](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-figure2-rejection-rates.png) - Figure 2
- [3-paper-figure3-category-heatmap.png](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-figure3-category-heatmap.png) - Figure 3
- [3-paper-figure4-score-distribution.png](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-figure4-score-distribution.png) - Figure 4
- [3-paper-figure5-model-rankings.png](https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-figure5-model-rankings.png) - Figure 5

### 🔗 Download All Files
Use `wget` or `curl` to download all files at once:

```bash
# Create directories
mkdir -p results batch_evaluation_jobs/results reports/paper reports/academic/figures_124qa

# Download benchmark results
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/1-results-phase1_final.json -O results/phase1_final.json
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/1-results-phase2_final.json -O results/phase2_final.json
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/1-results-falsereject_final.json -O results/falsereject_benchmark_final.json

# Download evaluation outputs
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/2-eval-appropriateness_results.jsonl -O batch_evaluation_jobs/results/appropriateness_results.jsonl
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/2-eval-actionability_results.jsonl -O batch_evaluation_jobs/results/actionability_results.jsonl

# Download paper and figures
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-draft.md -O reports/paper/paper_draft.md
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-figure1-model-boxplot.png -O reports/academic/figures_124qa/figure1_model_boxplot.png
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-figure2-rejection-rates.png -O reports/academic/figures_124qa/figure2_rejection_rates.png
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-figure3-category-heatmap.png -O reports/academic/figures_124qa/figure3_category_heatmap.png
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-figure4-score-distribution.png -O reports/academic/figures_124qa/figure4_score_distribution.png
wget https://github.com/Marvin-Cypher/LLM-for-LLM/releases/download/v1.0.0/3-paper-figure5-model-rankings.png -O reports/academic/figures_124qa/figure5_model_rankings.png
```
```

### 6. Click "Update release"

---

## ✅ Upload Checklist

Use this to track your progress:

### Category 1: Benchmark Results
- [ ] 1-results-phase1_final.json
- [ ] 1-results-phase2_final.json
- [ ] 1-results-falsereject_final.json

### Category 2: Evaluation Outputs
- [ ] 2-eval-appropriateness_results.jsonl
- [ ] 2-eval-actionability_results.jsonl
- [ ] 2-eval-appropriateness_errors.jsonl

### Category 3: Paper & Figures
- [ ] 3-paper-draft.md
- [ ] 3-paper-latex.tex (rename from main.tex)
- [ ] 3-paper-overleaf-package.zip
- [ ] 3-paper-figure1-model-boxplot.png
- [ ] 3-paper-figure2-rejection-rates.png
- [ ] 3-paper-figure3-category-heatmap.png
- [ ] 3-paper-figure4-score-distribution.png
- [ ] 3-paper-figure5-model-rankings.png

**Total: 14 files**

---

## 🎯 After Upload

1. Verify all 14 files appear in the release assets
2. Click a few download links to test they work
3. Share the repository with collaborators!

Your GitHub repository will be **complete and publication-ready** ✨

**Repository**: https://github.com/Marvin-Cypher/LLM-for-LLM
**Release**: https://github.com/Marvin-Cypher/LLM-for-LLM/releases/tag/v1.0.0
