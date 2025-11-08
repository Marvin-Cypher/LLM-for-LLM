# LaTeX Paper Update Instructions

## Status: Partially Updated

### ✅ Completed Updates

1. **Abstract** - UPDATED in `main.tex` lines 22-26
   - Changed GPT-5 score from 7.22/10 to 9.17/10
   - Added "across 124 Q&A legal questions" specification
   - Added specific over-refusal rates: GPT-OSS-120B (95.8%), O3-Mini (87.5%)
   - Updated overall refusal rate range from "0% to 45.8%" to "0% to 21%"

2. **Figures** - ALL 5 FIGURES UPDATED in `figures/` directory
   - figure1_model_boxplot.png - 124 Q&A dataset
   - figure2_rejection_rates.png - 124 Q&A dataset
   - figure3_category_heatmap.png - 124 Q&A dataset (visual issues fixed)
   - figure4_score_distribution.png - 124 Q&A dataset
   - figure5_model_rankings.png - NEW figure added

---

## ⏳ Manual Updates Needed

### Table 1: Model Performance Rankings (Section 4.1)

**Current table** shows old mixed-dataset results. **Replace with**:

```latex
\begin{table}[h]
\centering
\small
\begin{tabular}{clccc}
\toprule
\textbf{Rank} & \textbf{Model} & \textbf{Score} & \textbf{Refusal} & \textbf{Quality} \\
\midrule
1 & GPT-5 & \textbf{9.17} & 0.0\% & Excellent \\
2 & DeepSeek v3 & 8.93 & 3.3\% & Excellent \\
3 & Mistral Large & 8.90 & 0.8\% & Excellent \\
4 & Qwen 2.5 72B & 8.89 & 0.0\% & Excellent \\
5 & Gemini 2.5 Flash & 8.71 & 4.9\% & Very Good \\
6 & Claude Sonnet 4.5 & 8.61 & 0.8\% & Very Good \\
7 & Grok-4 & 8.34 & 3.2\% & Good \\
8 & GLM-4.6 & 8.13 & 1.6\% & Good \\
9 & GPT-OSS-120B & 7.02 & 21.0\% & Moderate \\
10 & O3-Mini & 6.36 & 17.7\% & Poor \\
\bottomrule
\end{tabular}
\caption{Model Performance on 124 Q\&A Legal Questions. Score = Appropriateness (0-10). Refusal = Percentage of questions refused.}
\label{tab:model-performance-124qa}
\end{table}
```

**Key findings to update below the table**:
- GPT-5 achieves top performance (9.17/10) with perfect safety calibration
- Top 6 models cluster above 8.6/10, showing consistently high quality
- DeepSeek v3, Mistral Large, and Qwen 2.5 72B perform nearly identically (8.89-8.93)
- Sharp performance drop for GPT-OSS-120B and O3-Mini due to aggressive safety training
- Over-refusal significantly impacts usability: O3-Mini refuses 17.7% of all questions

---

### Table 3: False Positive Rates (Section 4.4)

**Section title**: Change "Over-Refusal Analysis" to **"Safety Calibration: Over-Refusal Analysis"**

**Replace current table with**:

```latex
\begin{table}[h]
\centering
\small
\begin{tabular}{clccc}
\toprule
\textbf{Rank} & \textbf{Model} & \textbf{Overall} & \textbf{FP Rate} & \textbf{FP Count} \\
 & & \textbf{Refusal} & \textbf{(FalseReject)} & \textbf{/ 24} \\
\midrule
1 & GPT-5 & 0.0\% & \textbf{0.0\%} & 0/24 \\
2 & Qwen 2.5 72B & 0.0\% & 0.0\% & 0/24 \\
3 & Claude Sonnet 4.5 & 0.8\% & 4.2\% & 1/24 \\
4 & Mistral Large & 0.8\% & 4.2\% & 1/24 \\
5 & GLM-4.6 & 1.6\% & 4.2\% & 1/24 \\
6 & Grok-4 & 3.2\% & 16.7\% & 4/24 \\
7 & DeepSeek v3 & 3.3\% & 17.4\% & 4/23 \\
8 & Gemini 2.5 Flash & 4.9\% & 25.0\% & 6/24 \\
9 & O3-Mini & 17.7\% & \textbf{87.5\%} & 21/24 \\
10 & GPT-OSS-120B & 21.0\% & \textbf{95.8\%} & 23/24 \\
\bottomrule
\end{tabular}
\caption{Safety Calibration on Legitimate Legal Questions. Overall Refusal = \% of all 124 questions refused. FP Rate = False positive rate on 24 FalseReject questions. Lower is better.}
\label{tab:false-positives-124qa}
\end{table}
```

**Key findings to add**:
- GPT-5 and Qwen 2.5 72B demonstrate perfect safety calibration (0\% false positives)
- GPT-OSS-120B and O3-Mini are practically unusable (95.8\% and 87.5\% false positives)
- Clear trade-off between safety training intensity and usability

---

### Section 4: Results - Analysis Focus Statement

**Add after `\section{Results}` heading**:

```latex
\section{Results}

\textbf{Analysis Focus}: This results section focuses on the \textbf{124 Q\&A questions} (Phase 1: 100 questions + FalseReject: 24 questions), which provide the most comprehensive assessment of legal reasoning and safety calibration without the confounding factor of file context. Phase 2 contract analysis (39 tasks with files) is discussed separately to isolate file-grounded reasoning capabilities.
```

---

### Figure Captions to Update

**Figure 1** - Model Boxplot:
```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.9\linewidth]{figures/figure1_model_boxplot.png}
\caption{Model Performance Distribution on 124 Q\&A Questions. Boxplots show median, quartiles, and outliers for appropriateness scores (0-10 scale).}
\label{fig:model-boxplot-124qa}
\end{figure}
```

**Figure 2** - Rejection Rates:
```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.9\linewidth]{figures/figure2_rejection_rates.png}
\caption{Model Refusal Rates on 124 Q\&A Questions. Color-coded: green (<15\%), orange (15-30\%), red (>30\%). GPT-OSS-120B and O3-Mini show severe over-refusal.}
\label{fig:rejection-rates-124qa}
\end{figure}
```

**Figure 3** - Category Heatmap:
```latex
\begin{figure}[h]
\centering
\includegraphics[width=\linewidth]{figures/figure3_category_heatmap.png}
\caption{Model Performance by Legal Category (124 Q\&A Questions). Heatmap shows mean appropriateness scores across 68 legal categories. Green = high performance, yellow = moderate, red = poor.}
\label{fig:category-heatmap-124qa}
\end{figure}
```

**Figure 4** - Score Distribution:
```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.9\linewidth]{figures/figure4_score_distribution.png}
\caption{Score Distribution Across Models (124 Q\&A Questions). Histogram shows concentration of appropriateness scores for each model.}
\label{fig:score-distribution-124qa}
\end{figure}
```

**Figure 5** - Model Rankings (NEW):
```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.9\linewidth]{figures/figure5_model_rankings.png}
\caption{Overall Model Rankings on 124 Q\&A Questions. Horizontal bar chart of mean appropriateness scores. GPT-5 leads at 9.17/10.}
\label{fig:model-rankings-124qa}
\end{figure}
```

---

## Data Summary for Reference

### 124 Q&A Dataset Composition
- Phase 1: 100 legal Q&A questions (no files)
- FalseReject: 24 over-refusal test questions
- **Total: 124 Q&A questions**
- Excludes: Phase 2 (39 contract tasks with files)

### Top 5 Model Scores (124 Q&A)
1. GPT-5: 9.17
2. DeepSeek v3: 8.93
3. Mistral Large: 8.90
4. Qwen 2.5 72B: 8.89
5. Gemini 2.5 Flash: 8.71

### Perfect Safety Calibration (0% False Positives)
- GPT-5: 0/24
- Qwen 2.5 72B: 0/24

### Severe Over-Refusal Issues
- GPT-OSS-120B: 95.8% false positives (23/24)
- O3-Mini: 87.5% false positives (21/24)

### Overall Statistics
- Mean score: 8.30/10
- Median score: 9.00/10
- Std dev: 1.83
- Total responses evaluated: 1,236/1,240 (99.7% coverage)

---

## Quick Checklist

- [x] Abstract updated with 124 Q&A insights
- [x] All 5 figures regenerated and copied to figures/ directory
- [ ] Table 1 (Model Performance) updated with 124 Q&A data
- [ ] Table 3 (False Positives) updated with new over-refusal data
- [ ] Analysis focus statement added to Results section
- [ ] Figure captions updated to reference 124 Q&A dataset
- [ ] Section 4.1 text updated with new key findings
- [ ] Section 4.4 title changed to "Safety Calibration"
- [ ] Reference to Figure 5 (new rankings figure) added

---

## Files Ready for Overleaf

All files in `reports/paper/overleaf/` are ready:

- ✅ `main.tex` - Abstract updated, needs table/figure caption updates
- ✅ `figures/figure1_model_boxplot.png` - 124 Q&A data
- ✅ `figures/figure2_rejection_rates.png` - 124 Q&A data
- ✅ `figures/figure3_category_heatmap.png` - 124 Q&A data (fixed)
- ✅ `figures/figure4_score_distribution.png` - 124 Q&A data
- ✅ `figures/figure5_model_rankings.png` - NEW figure
- ✅ `references.bib` - No changes needed
- ✅ `README.md` - Instructions for Overleaf upload

---

## Compilation Test

Before submitting, test LaTeX compilation:

```bash
cd reports/paper/overleaf/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Expected output: `main.pdf` with updated content and all 5 figures.

---

**Last Updated**: November 8, 2025
**Markdown Version**: reports/paper/paper_draft.md (fully updated)
**LaTeX Version**: reports/paper/overleaf/main.tex (partially updated - needs manual table/caption updates)
