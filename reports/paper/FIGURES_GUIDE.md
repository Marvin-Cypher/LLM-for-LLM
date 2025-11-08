# Figures Guide for "LLMs for LLMs" Paper

## All Available Figures (9 Total)

Located in: `reports/paper/overleaf/figures/`

---

## Set 1: Original Phase 1 Analysis (4 Figures)
*From earlier benchmark with 100 Q&A questions*

### Figure 1: Model Performance Boxplot
**File**: `figure1_model_boxplot.png` (185 KB)
**Shows**: Distribution of scores across all models for Phase 1
**Use for**: Showing variance in model performance, median scores
**Data source**: Phase 1 (100 Q&A questions)

### Figure 2: Rejection Rates by Model
**File**: `figure2_rejection_rates.png` (199 KB)
**Shows**: How often models refuse to answer questions
**Use for**: Illustrating over-caution patterns in Phase 1
**Data source**: Phase 1 (100 Q&A questions)

### Figure 3: Category Performance Heatmap
**File**: `figure3_category_heatmap.png` (520 KB)
**Shows**: Model performance across different legal categories (corporate, contracts, employment, etc.)
**Use for**: Category-specific analysis, showing which models excel where
**Data source**: Phase 1 (100 Q&A questions, categorized)
**Key insight**: Different models excel in different legal domains

### Figure 4: Score Distribution
**File**: `figure4_score_distribution.png` (90 KB)
**Shows**: Overall distribution of quality scores across models
**Use for**: Statistical analysis section, showing score distributions
**Data source**: Phase 1 (100 Q&A questions)

---

## Set 2: New Comprehensive Analysis (5 Figures)
*From combined Phase 1 (100) + Phase 2 (39) + FalseReject (24) = 163 tasks*

### Figure 5: Overall Model Rankings
**File**: `model_rankings.png` (131 KB)
**Shows**: Bar chart of overall scores (weighted: 50% appropriateness + 50% actionability)
**Use for**: Main results - showing GPT-5 as winner
**Data source**: All 3 phases combined (Phase 1 + Phase 2 + FalseReject)
**Key finding**: GPT-5: 7.22/10 (best), O3-Mini: 4.50/10 (worst)

### Figure 6: File Context Impact
**File**: `file_context_impact.png` (146 KB)
**Shows**: Performance comparison Phase 1 (no files) vs Phase 2 (with files)
**Use for**: Demonstrating file-grounded reasoning capabilities
**Data source**: Phase 1 vs Phase 2 comparison
**Key finding**: GLM-4.6 improves +19.6% with file context

### Figure 7: Cross-Group Consistency
**File**: `consistency.png` (136 KB)
**Shows**: How consistently models perform across different task types
**Use for**: Reliability analysis - which models are predictable
**Data source**: Variance across Phase 1, Phase 2, FalseReject
**Key finding**: Claude & Gemini most consistent (0.99), GLM-4.6 least (0.76)

### Figure 8: False Positive Over-Refusal Rates
**File**: `falsereject_analysis.png` (156 KB)
**Shows**: Percentage of legitimate questions incorrectly refused
**Use for**: Safety calibration analysis - over-caution measurement
**Data source**: FalseReject benchmark (24 questions)
**Key finding**: GPT-5: 0% FP rate (perfect), O3-Mini: 45.8% (over-cautious)

### Figure 9: Provider Comparison
**File**: `provider_comparison.png` (107 KB)
**Shows**: Performance grouped by provider (OpenAI, Anthropic, Google, etc.)
**Use for**: Showing provider-level patterns and safety culture differences
**Data source**: All 3 phases, grouped by provider
**Key finding**: Provider safety culture influences over-refusal rates

---

## Recommended Figure Usage in Paper

### Main Results Section:
- **Figure 5** (model_rankings.png) - Primary result showing GPT-5 winner
- **Figure 3** (category_heatmap.png) - Category-specific winners
- **Figure 8** (falsereject_analysis.png) - Over-refusal analysis

### Analysis Section:
- **Figure 6** (file_context_impact.png) - File-grounded reasoning
- **Figure 7** (consistency.png) - Reliability/consistency
- **Figure 1** (model_boxplot.png) - Statistical distributions

### Additional Insights:
- **Figure 9** (provider_comparison.png) - Provider patterns
- **Figure 2** (rejection_rates.png) - General refusal patterns
- **Figure 4** (score_distribution.png) - Score distributions

---

## Data Lineage

### Phase 1 Only (Original 4 Figures)
- 100 legal Q&A questions
- 10 models tested
- 1,000 total responses
- Category-specific analysis

### Phase 1 + Phase 2 + FalseReject (New 5 Figures)
- **Phase 1**: 100 Q&A questions (no files)
- **Phase 2**: 39 contract tasks (with files)
- **FalseReject**: 24 over-refusal tests
- **Total**: 163 tasks, 1,630 responses
- **Plus**: 2,715 LLM-based evaluations (GPT-4o-mini as judge)

---

## Which Figures Show What?

**Best Overall Model**: Figure 5 (model_rankings.png)
**Category-Specific Champions**: Figure 3 (category_heatmap.png)
**File Context Impact**: Figure 6 (file_context_impact.png)
**Consistency/Reliability**: Figure 7 (consistency.png)
**Over-Refusal/Safety**: Figure 8 (falsereject_analysis.png)
**Provider Patterns**: Figure 9 (provider_comparison.png)
**Score Distributions**: Figure 1 (boxplot), Figure 4 (distribution)
**Refusal Patterns**: Figure 2 (rejection_rates.png)

---

## Figure Quality

All figures are publication-ready:
- **Resolution**: 300 DPI minimum
- **Format**: PNG (lossless)
- **File sizes**: 90 KB - 520 KB
- **Suitable for**: Academic papers, presentations, reports

---

## LaTeX Usage

In your `main.tex` file, reference figures like this:

```latex
\begin{figure}[t]
\centering
\includegraphics[width=0.9\columnwidth]{figures/model_rankings.png}
\caption{Overall Model Performance Rankings. GPT-5 achieves the highest score (7.22/10), significantly outperforming other models.}
\label{fig:rankings}
\end{figure}
```

Then reference in text: `As shown in Figure~\ref{fig:rankings}, GPT-5...`

---

## Summary

You have a comprehensive set of 9 publication-quality figures covering:
- ✅ Phase 1 original analysis (4 figures)
- ✅ New comprehensive analysis with all 3 phases (5 figures)
- ✅ All statistical analyses (rankings, consistency, distributions)
- ✅ All key findings (file context, over-refusal, categories)
- ✅ Ready for academic publication (300 DPI, proper formatting)

**No figures were deleted** - everything is preserved and available in the paper package!
