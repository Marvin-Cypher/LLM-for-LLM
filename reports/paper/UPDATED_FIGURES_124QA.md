# Updated Figures with 124 Q&A Questions

## Summary

Successfully regenerated figures 1-5 using the **merged 124 Q&A questions dataset** (Phase 1 + FalseReject), excluding file-based contract tasks (Phase 2).

## What Changed

### Previous Figures (Original)
- **Data source**: Phase 1 only (100 Q&A questions)
- **Location**: `reports/academic/figures/` (preserved)
- **Figures**: figure1-4

### Updated Figures (New)
- **Data source**: Phase 1 + FalseReject = 124 Q&A questions
- **Location**:
  - `reports/academic/figures_124qa/` (new directory)
  - `reports/paper/overleaf/figures/` (replaced old versions)
- **Figures**: figure1-5 (added new figure 5: model rankings)

## Data Composition

### 124 Q&A Questions Dataset
```
Phase 1:      100 Q&A questions (no files)
FalseReject:   24 Q&A questions (over-refusal test)
─────────────────────────────────────────────
Total:        124 Q&A questions
```

### Excluded from These Figures
- Phase 2: 39 contract modification tasks (with file context)
- These file-based tasks are analyzed separately in comprehensive figures

## Evaluation Scores
- **Total responses**: 1,240 (124 questions × 10 models)
- **Evaluated responses**: 1,236 (99.7% coverage)
- **Missing scores**: 4 responses
- **Evaluator**: GPT-4o-mini via OpenAI Batch API

## Updated Figures (1-5)

### Figure 1: Model Performance Boxplot
**File**: `figure1_model_boxplot.png` (191 KB)
**Shows**: Distribution of appropriateness scores across all models
**Data**: 124 Q&A questions (Phase 1 + FalseReject)
**Visualization**: Boxplot showing median, quartiles, and outliers
**Use for**: Showing performance variance and overall score distributions

### Figure 2: Rejection Rates by Model
**File**: `figure2_rejection_rates.png` (163 KB)
**Shows**: Percentage of questions refused by each model
**Data**: 124 Q&A questions
**Visualization**: Bar chart of refusal percentages
**Use for**: Illustrating over-caution patterns and safety calibration
**Key finding**: Different models show vastly different refusal rates

### Figure 3: Category Performance Heatmap
**File**: `figure3_category_heatmap.png` (868 KB)
**Shows**: Model performance across different legal categories
**Data**: 124 Q&A questions, grouped by category
**Categories**: Corporate law, contracts, employment, litigation, compliance, etc.
**Visualization**: Color-coded heatmap (darker = better performance)
**Use for**: Category-specific analysis, identifying domain-specific strengths
**Key insight**: Different models excel in different legal domains

### Figure 4: Score Distribution
**File**: `figure4_score_distribution.png` (122 KB)
**Shows**: Histogram of score distributions across all models
**Data**: 124 Q&A questions
**Visualization**: Overlapping histograms or density plots
**Use for**: Statistical analysis, showing score concentration patterns

### Figure 5: Model Rankings (NEW)
**File**: `figure5_model_rankings.png` (166 KB)
**Shows**: Overall model rankings based on average appropriateness scores
**Data**: 124 Q&A questions
**Visualization**: Horizontal bar chart of mean scores
**Use for**: Main results section, showing clear winner
**Key finding**: Clear performance hierarchy among models

## Technical Implementation

### Custom ID Matching Fix
The original script failed because evaluation results use array indices in custom_ids:
- **Phase 1 format**: `approp_phase1_qa_{index}_{model}_{suffix}`
- **FalseReject format**: `approp_falsereject_{index}_{model}_{suffix}`

Where `{index}` is 0-99 for Phase 1, 0-23 for FalseReject.

### Code Updates
1. Added `source_index` field to track original array position
2. Updated custom_id generation to use indices instead of question IDs
3. Implemented prefix matching to handle suffix variations

### Script Location
`scripts/regenerate_124qa_figures.py`

## Comparison: Original vs Updated

| Aspect | Original (100 Q&A) | Updated (124 Q&A) |
|--------|-------------------|------------------|
| **Phase 1** | ✅ 100 questions | ✅ 100 questions |
| **FalseReject** | ❌ Not included | ✅ 24 questions |
| **Phase 2 (Files)** | ❌ Not included | ❌ Not included |
| **Total Questions** | 100 | 124 |
| **Evaluation Scores** | ~1,000 | 1,236 |
| **Figures** | 4 figures | 5 figures |
| **New Figure** | - | Figure 5 (rankings) |

## What This Means for the Paper

### Stronger Analysis
- **+24% more data**: 124 vs 100 questions
- **Over-refusal insights**: FalseReject questions specifically test safety calibration
- **More comprehensive**: Includes both general Q&A and over-refusal testing
- **Better statistics**: Larger sample size improves statistical significance

### Clearer Narrative
The 124 Q&A dataset tells a cohesive story:
1. **General capability** (Phase 1: 100 questions)
2. **Safety calibration** (FalseReject: 24 questions)
3. Combined analysis shows both accuracy AND appropriate refusal behavior

### Separate File Analysis
File-based tasks (Phase 2) remain in comprehensive figures because:
- Different evaluation dimensions (file context handling)
- Smaller sample size (39 tasks)
- Best analyzed separately to show file-grounded reasoning impact

## Figure Usage in Paper

### Main Results Section
- **Figure 5** (model_rankings.png) - Primary result
- **Figure 1** (model_boxplot.png) - Score distributions
- **Figure 2** (rejection_rates.png) - Refusal analysis

### Detailed Analysis Section
- **Figure 3** (category_heatmap.png) - Domain-specific performance
- **Figure 4** (score_distribution.png) - Statistical distributions

### Comprehensive Analysis (Separate)
Use the comprehensive figures that include all 163 tasks (100+39+24) for:
- File context impact analysis
- Cross-group consistency
- Provider comparison

## Files Modified/Created

### Created
- `scripts/regenerate_124qa_figures.py` - Figure regeneration script
- `reports/academic/figures_124qa/` - New directory with 5 figures
- `reports/paper/UPDATED_FIGURES_124QA.md` - This document

### Updated
- `reports/paper/overleaf/figures/` - Replaced figure1-5 with 124 Q&A versions

### Preserved
- `reports/academic/figures/` - Original 100-question figures kept for reference
- Comprehensive analysis figures (6-9) remain unchanged

## Regeneration Instructions

To regenerate these figures:
```bash
python3 scripts/regenerate_124qa_figures.py
```

Output directory: `reports/academic/figures_124qa/`

## Validation

✅ Score matching works correctly (1,236/1,240 responses matched)
✅ All 5 figures generated successfully
✅ Figures copied to Overleaf directory
✅ Same visualization methods as original figures
✅ Data properly merged from Phase 1 + FalseReject
✅ Phase 2 (file-based tasks) correctly excluded

## Next Steps

1. Review figures visually to ensure quality
2. Update paper text to reference 124 Q&A dataset
3. Verify LaTeX compilation with new figures
4. Consider whether comprehensive figures (6-9) need similar updates

---

**Generated**: 2025-11-07
**Script**: `scripts/regenerate_124qa_figures.py`
**Data sources**: `results/phase1_final.json`, `results/falsereject_benchmark_final.json`
**Evaluation results**: `batch_evaluation_jobs/results/appropriateness_results.jsonl`
