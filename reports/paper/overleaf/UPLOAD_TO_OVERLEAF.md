# How to Upload Files to Overleaf

## The Error You're Seeing

```
LaTeX Error: File `acl2023.sty' not found.
```

This means Overleaf doesn't have the ACL 2023 style file. You need to upload it!

---

## Solution: Upload These Files to Overleaf

### Files to Upload (in this directory):

1. **acl2023.sty** (11 KB) - ACL 2023 LaTeX style file ✅ Ready
2. **acl_natbib.bst** (44 KB) - ACL bibliography style ✅ Ready
3. **main.tex** - Your updated paper ✅ Ready
4. **references.bib** - Bibliography (if you have citations)
5. **figures/** folder - All 5 PNG figures ✅ Ready

---

## Step-by-Step Upload Instructions

### 1. Open Your Overleaf Project
- Go to https://www.overleaf.com
- Open your project (or create a new one)

### 2. Upload the Style Files (CRITICAL)

Click the **"Upload"** button in Overleaf, then upload these files from your computer:

**From: `/Users/marvin/legal-llm-benchmark/reports/paper/overleaf/`**

- ✅ `acl2023.sty` (11 KB)
- ✅ `acl_natbib.bst` (44 KB)

These files are **required** for compilation!

### 3. Upload the Main Paper

- ✅ `main.tex` (updated with 124 Q&A insights)

### 4. Create a "figures" Folder in Overleaf

In Overleaf:
- Click **"New Folder"**
- Name it: `figures`

### 5. Upload All 5 Figures to the "figures" Folder

Click on the `figures` folder, then upload these PNG files:

**From: `/Users/marvin/legal-llm-benchmark/reports/paper/overleaf/figures/`**

- ✅ `figure1_model_boxplot.png` (191 KB)
- ✅ `figure2_rejection_rates.png` (163 KB)
- ✅ `figure3_category_heatmap.png` (442 KB)
- ✅ `figure4_score_distribution.png` (122 KB)
- ✅ `figure5_model_rankings.png` (166 KB)

### 6. (Optional) Upload Bibliography

If you have references:
- ✅ `references.bib`

---

## After Uploading

### Click "Recompile" in Overleaf

The paper should now compile successfully! ✅

### Expected Output

A PDF with:
- Title: "LLMs for LLMs: Large Language Models Performance for Real Legal Practice"
- Updated abstract (GPT-5: 9.17/10)
- 2 tables with 124 Q&A data
- 5 figures (all rendered)
- ~12 pages

---

## Quick Checklist

Before compiling, make sure you have uploaded:

- [ ] acl2023.sty (in root directory)
- [ ] acl_natbib.bst (in root directory)
- [ ] main.tex (in root directory)
- [ ] figures/figure1_model_boxplot.png
- [ ] figures/figure2_rejection_rates.png
- [ ] figures/figure3_category_heatmap.png
- [ ] figures/figure4_score_distribution.png
- [ ] figures/figure5_model_rankings.png

---

## Alternative: Zip Package

I can create a single ZIP file with everything you need. Would you like me to do that?

---

## If You Still Get Errors

### Error: "File 'acl2023.sty' not found"
**Solution**: Make sure `acl2023.sty` is uploaded to the ROOT directory (not in a subfolder)

### Error: "Cannot find figure file"
**Solution**: Make sure all PNG files are in a folder named `figures` (lowercase)

### Error: "Undefined control sequence"
**Solution**: The ACL style might need updates. You can switch to standard article class:
- Change line 2 from `\usepackage[hyperref]{acl2023}` to just remove that line
- Change line 1 to `\documentclass[11pt,a4paper]{article}`

---

## File Locations on Your Computer

All files ready for upload are here:

```
/Users/marvin/legal-llm-benchmark/reports/paper/overleaf/
├── acl2023.sty              ← Upload this!
├── acl_natbib.bst           ← Upload this!
├── main.tex                 ← Upload this!
├── references.bib           ← Upload this (if you have it)
└── figures/
    ├── figure1_model_boxplot.png       ← Upload this!
    ├── figure2_rejection_rates.png     ← Upload this!
    ├── figure3_category_heatmap.png    ← Upload this!
    ├── figure4_score_distribution.png  ← Upload this!
    └── figure5_model_rankings.png      ← Upload this!
```

---

## Need Help?

If you're still having issues, I can:
1. Create a ZIP file with everything
2. Create an alternative version without ACL style (standard article class)
3. Help debug specific Overleaf errors

Let me know what you need!
