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
