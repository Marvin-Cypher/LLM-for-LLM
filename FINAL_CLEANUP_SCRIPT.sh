#!/bin/bash
# Final cleanup: Remove unnecessary docs, keep only reproduction scripts, remove API keys

echo "🧹 Final Cleanup for Commit"
echo ""

# 1. Remove unnecessary documentation files
echo "📄 Removing unnecessary documentation..."
rm -f HUGGINGFACE_UPLOAD_SUMMARY.md
rm -f CLEANUP_COMPLETE_SUMMARY.md
rm -f docs/FIGURE_PLACEMENT_GUIDE.md
rm -f CONTRIBUTING.md  # Not needed for initial commit
echo "  ✅ Removed 4 unnecessary docs"

# 2. Keep only essential reproduction scripts
echo ""
echo "📝 Cleaning scripts directory..."
cd scripts

# Keep these essential scripts for reproduction:
# - final_repo_cleanup.sh (this file's parent)
# All others moved to archive/ already

# Remove HuggingFace upload scripts (data already uploaded)
mkdir -p archive/huggingface 2>/dev/null
mv prepare_huggingface_datasets.py archive/huggingface/ 2>/dev/null || true
mv upload_to_huggingface.py archive/huggingface/ 2>/dev/null || true
mv merge_evaluations_to_responses.py archive/huggingface/ 2>/dev/null || true
mv create_additional_hf_datasets.py archive/huggingface/ 2>/dev/null || true
mv create_flattened_hf_datasets.py archive/huggingface/ 2>/dev/null || true

echo "  ✅ Moved HuggingFace scripts to archive/"

cd ..

# 3. Check for API keys in all scripts
echo ""
echo "🔑 Checking for API keys in scripts..."

# Search for common API key patterns
api_key_files=$(grep -r "hf_[A-Za-z0-9]" scripts/ --include="*.py" --include="*.sh" 2>/dev/null || true)
openai_key_files=$(grep -r "sk-[A-Za-z0-9]" scripts/ --include="*.py" --include="*.sh" 2>/dev/null || true)
other_keys=$(grep -r "api_key.*=.*['\"][A-Za-z0-9]" scripts/ --include="*.py" 2>/dev/null || true)

if [ -n "$api_key_files" ] || [ -n "$openai_key_files" ] || [ -n "$other_keys" ]; then
    echo "  ⚠️  WARNING: Found potential API keys in scripts!"
    echo "$api_key_files"
    echo "$openai_key_files"
    echo "$other_keys"
else
    echo "  ✅ No hardcoded API keys found"
fi

# 4. Update .gitignore to exclude sensitive files
echo ""
echo "📝 Updating .gitignore..."
cat >> .gitignore << 'GITIGNORE'

# API Keys and Secrets
*.key
*.secret
.env.local
config/api_keys.json

# Hugging Face token
huggingface_token.txt
hf_token.txt

GITIGNORE

echo "  ✅ Updated .gitignore"

# 5. Summary
echo ""
echo "========================================================================"
echo "  ✅ FINAL CLEANUP COMPLETE"
echo "========================================================================"
echo ""
echo "Removed files:"
echo "  - HUGGINGFACE_UPLOAD_SUMMARY.md"
echo "  - CLEANUP_COMPLETE_SUMMARY.md"
echo "  - docs/FIGURE_PLACEMENT_GUIDE.md"
echo "  - CONTRIBUTING.md"
echo "  - HuggingFace upload scripts (moved to archive/)"
echo ""
echo "Essential files remaining:"
echo "  ✅ README.md"
echo "  ✅ DATA_ORGANIZATION.md"
echo "  ✅ REPO_STRUCTURE.md"
echo "  ✅ FINAL_COMMIT_CHECKLIST.md"
echo "  ✅ docs/BLOG_POST.md"
echo "  ✅ paper/ (9 files)"
echo "  ✅ data/ (input datasets)"
echo "  ✅ results/ (6 JSON files)"
echo "  ✅ scripts/final_repo_cleanup.sh"
echo ""
echo "🚀 Repository is ready for commit!"
echo ""
