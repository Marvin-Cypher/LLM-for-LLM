# LLMs for LLMs: Academic Paper - LaTeX Package

This package contains the complete LaTeX source for the paper "LLMs for LLMs: Large Language Models Performance for Real Legal Practice."

## Files Included

- `main.tex` - Main paper file
- `references.bib` - Bibliography (to be populated)
- `acl2023.sty` - ACL 2023 style file (download from ACL website)
- `figures/` - Directory for figure files

## Instructions for Overleaf

1. Create a new project in Overleaf
2. Upload all files from this package
3. Download ACL 2023 style files from: https://github.com/acl-org/acl-style-files
4. Place your figures in the `figures/` directory
5. Populate `references.bib` with your citations
6. Compile using pdfLaTeX

## Figures to Include

Copy these files from `reports/academic/batch_analysis/` to `figures/`:
- model_rankings.png
- file_context_impact.png
- consistency.png
- falsereject_analysis.png
- provider_comparison.png

## Customization

- Update author names and affiliations in `main.tex`
- Add actual citations to `references.bib`
- Customize abstract and introduction as needed
- Add appendix sections with full details

## Building Locally

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Notes

- Paper formatted for ACL 2023 conference style
- Can be adapted for other venues (IEEE, AAAI, etc.)
- Total page count: ~10-12 pages (including appendix)
- Figures should be high resolution (300 DPI minimum)
