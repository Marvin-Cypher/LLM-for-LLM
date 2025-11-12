#!/bin/bash
# Repository Cleanup Script
# Reduces 348 files to ~50 essential files for researchers

set -e  # Exit on error

echo "🧹 Starting repository cleanup..."
echo "Current files: $(find . -type f | grep -v '.git' | wc -l)"

# Step 1: Delete status/temporary files in root
echo ""
echo "Step 1: Removing status/temporary files..."
rm -f ABLITERATED_*.md \
      BUG_FIX_SUMMARY.md \
      COMPREHENSIVE_*.md \
      CORRECTED_RESULTS_SUMMARY.md \
      EVALUATION_INSIGHTS.md \
      FALSEREJECT_DATA_ISSUE.md \
      FIGURES_REGENERATED.md \
      FIGURE_AUDIT_REPORT.md \
      FINAL_*.md \
      HUGGINGFACE_QUICK_START.md \
      NEW_INSIGHTS_SUMMARY.md \
      PAPER_*.md \
      SESSION_COMPLETE_SUMMARY.md \
      UPDATE_ALL_ARTIFACTS.md \
      phase2_contract_tasks.json \
      huggingface_readme.md \
      huggingface_readme_complete.md \
      REPO_CLEANUP_PLAN.md

echo "✅ Removed $(ls -1 *.md 2>/dev/null | grep -E '(ABLITERATED|BUG|COMPREHENSIVE|CORRECTED|EVALUATION|FALSEREJECT|FIGURES|FIGURE_AUDIT|FINAL|HUGGINGFACE|NEW_INSIGHTS|PAPER|SESSION|UPDATE)' | wc -l) status files"

# Step 2: Clean up intermediate results
echo ""
echo "Step 2: Cleaning intermediate results..."
cd results
rm -f abliterated_falsereject_final.json \
      abliterated_phase1.json \
      abliterated_phase1_final.json \
      abliterated_phase2_final.json \
      falsereject_analysis.json \
      falsereject_analysis_with_abliterated.json \
      falsereject_raw_responses.csv \
      phase1_final.json \
      phase2_final.json \
      phase2_final_with_abliterated.json

echo "✅ Removed intermediate result files"
cd ..

# Step 3: Rename final results for clarity
echo ""
echo "Step 3: Renaming final results..."
cd results
[ -f phase1_final_with_abliterated_scored.json ] && mv phase1_final_with_abliterated_scored.json phase1_responses.json
[ -f phase2_final_with_abliterated_scored.json ] && mv phase2_final_with_abliterated_scored.json phase2_responses.json
[ -f falsereject_benchmark_final.json ] && mv falsereject_benchmark_final.json phase3_responses.json

echo "✅ Renamed results files"
cd ..

# Step 4: Reorganize data directory
echo ""
echo "Step 4: Reorganizing data directory..."
cd data
[ -f 100_realistic_legal_questions.json ] && mv 100_realistic_legal_questions.json phase1_questions.json
echo "✅ Renamed questions file"
cd ..

# Rename phase2_documents to data/phase2_contracts
if [ -d "phase2_documents" ]; then
    mv phase2_documents data/phase2_contracts
    echo "✅ Moved phase2_documents -> data/phase2_contracts"
fi

# Step 5: Clean up scripts directory (keep only essential)
echo ""
echo "Step 5: Cleaning scripts directory..."
cd scripts

# Keep only essential scripts
mkdir -p ../scripts_backup
mv *.py ../scripts_backup/ 2>/dev/null || true

# Restore only the essential upload script
[ -f ../scripts_backup/upload_to_huggingface.py ] && mv ../scripts_backup/upload_to_huggingface.py .

echo "✅ Cleaned scripts (backed up to scripts_backup/)"
cd ..

# Step 6: Clean up reports directory
echo ""
echo "Step 6: Cleaning reports directory..."
rm -rf reports/benchmark_data_*.csv \
       reports/benchmark_report_*.md \
       reports/COMPREHENSIVE_FINDINGS_BLOG.md \
       reports/paper/ACADEMIC_INSIGHTS_FRAMEWORK.md \
       reports/paper/COMPREHENSIVE_FIXES_TO_APPLY.md \
       reports/paper/FIGURES_GUIDE.md \
       reports/paper/FINAL_FIGURES_SUMMARY.md \
       reports/paper/PAPER_STRUCTURE_ANALYSIS.md \
       reports/paper/PAPER_UPDATE_124QA.md \
       reports/paper/SUBMISSION_READY_CHECKLIST.md \
       reports/paper/UPDATED_FIGURES_124QA.md \
       reports/paper/paper_draft.md

# Move overleaf to top-level paper/
if [ -d "reports/paper/overleaf" ]; then
    mkdir -p paper
    cp /tmp/overleaf_submission_ready/main.tex paper/
    cp /tmp/overleaf_submission_ready/references.bib paper/
    cp /tmp/overleaf_submission_ready/acl2023.sty paper/
    cp /tmp/overleaf_submission_ready/*.pdf paper/ 2>/dev/null || true
    echo "✅ Copied paper files from submission package"
fi

# Remove reports directory entirely
rm -rf reports

echo "✅ Cleaned reports directory"

# Step 7: Remove batch_evaluation_jobs
echo ""
echo "Step 7: Removing batch job artifacts..."
rm -rf batch_evaluation_jobs
echo "✅ Removed batch_evaluation_jobs/"

# Final count
echo ""
echo "================================================"
echo "✅ Cleanup complete!"
echo "Files before: 348"
echo "Files after: $(find . -type f | grep -v '.git' | grep -v 'scripts_backup' | wc -l)"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Review the cleaned structure"
echo "2. Create reproduce_paper.py script"
echo "3. Update README.md"
echo "4. Test that essential files are present"
echo ""
echo "Backup of all scripts saved in: scripts_backup/"
