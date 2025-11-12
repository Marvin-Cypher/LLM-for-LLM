#!/bin/bash
# Restore all essential reproduction scripts from backup

echo "🔄 Restoring Reproduction Scripts"
echo ""

cd /Users/marvin/legal-llm-benchmark

# Create scripts/reproduction directory
mkdir -p scripts/reproduction

echo "📋 Copying essential benchmark scripts..."

# Stage 2: Benchmarking
cp scripts_backup/benchmark_async.py scripts/reproduction/ 2>/dev/null && echo "  ✅ benchmark_async.py"
cp scripts_backup/phase2_benchmark_hybrid.py scripts/reproduction/ 2>/dev/null && echo "  ✅ phase2_benchmark_hybrid.py"
cp scripts_backup/run_falsereject_benchmark.py scripts/reproduction/ 2>/dev/null && echo "  ✅ run_falsereject_benchmark.py"
cp scripts_backup/run_all_abliterated_benchmarks.py scripts/reproduction/ 2>/dev/null && echo "  ✅ run_all_abliterated_benchmarks.py"

# Retry scripts
cp scripts_backup/retry_failed_requests.py scripts/reproduction/ 2>/dev/null && echo "  ✅ retry_failed_requests.py"
cp scripts_backup/retry_openai_official.py scripts/reproduction/ 2>/dev/null && echo "  ✅ retry_openai_official.py"
cp scripts_backup/retry_missing_phase1.py scripts/reproduction/ 2>/dev/null && echo "  ✅ retry_missing_phase1.py"

echo ""
echo "🔍 Looking for evaluation scripts..."

# Stage 3: Evaluation
find scripts_backup -name "*eval*.py" -exec cp {} scripts/reproduction/ \; 2>/dev/null
ls scripts/reproduction/*eval*.py 2>/dev/null && echo "  ✅ Found evaluation scripts" || echo "  ⚠️  No evaluation scripts found"

echo ""
echo "📊 Looking for figure generation scripts..."

# Stage 5: Figures
find scripts_backup -name "*figure*.py" -exec cp {} scripts/reproduction/ \; 2>/dev/null
find scripts_backup -name "*plot*.py" -exec cp {} scripts/reproduction/ \; 2>/dev/null
ls scripts/reproduction/*figure*.py scripts/reproduction/*plot*.py 2>/dev/null && echo "  ✅ Found figure scripts" || echo "  ⚠️  No figure scripts found"

echo ""
echo "📁 Scripts restored to: scripts/reproduction/"
ls -lh scripts/reproduction/ | wc -l
echo "files"

