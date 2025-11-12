#!/bin/bash
# Quick progress monitor for abliterated models benchmarks

echo "================================================================================"
echo "ABLITERATED MODELS BENCHMARK - PROGRESS MONITOR"
echo "================================================================================"
echo ""

# Check if benchmark is running
if ps aux | grep -v grep | grep "run_all_abliterated_benchmarks.py" > /dev/null; then
    echo "✅ Benchmark is RUNNING"
else
    echo "❌ Benchmark is NOT running"
fi

echo ""
echo "--------------------------------------------------------------------------------"
echo "FILE SIZES"
echo "--------------------------------------------------------------------------------"
ls -lh results/abliterated*.json 2>/dev/null | awk '{print $9, "-", $5}'

echo ""
echo "--------------------------------------------------------------------------------"
echo "PROGRESS BY BENCHMARK"
echo "--------------------------------------------------------------------------------"

# Phase 1
if [ -f "results/abliterated_phase1_final.json" ]; then
    phase1_count=$(python3 -c "import json; f=open('results/abliterated_phase1_final.json'); d=json.load(f); print(len(d.get('questions', [])))" 2>/dev/null || echo "0")
    echo "Phase 1 (100 Q&A):        $phase1_count/100 questions completed"
fi

# FalseReject
if [ -f "results/abliterated_falsereject_final.json" ]; then
    fr_count=$(python3 -c "import json; f=open('results/abliterated_falsereject_final.json'); d=json.load(f); print(len(d.get('questions', [])))" 2>/dev/null || echo "0")
    echo "FalseReject (24 critical): $fr_count/24 questions completed"
fi

# Phase 2
if [ -f "results/abliterated_phase2_final.json" ]; then
    phase2_count=$(python3 -c "import json; f=open('results/abliterated_phase2_final.json'); d=json.load(f); print(len(d.get('questions', [])))" 2>/dev/null || echo "0")
    echo "Phase 2 (40 contracts):   $phase2_count/40 tasks completed"
fi

echo ""
echo "--------------------------------------------------------------------------------"
echo "LATEST LOG OUTPUT (last 20 lines)"
echo "--------------------------------------------------------------------------------"
tail -20 /tmp/abliterated_all_benchmarks.log 2>/dev/null || echo "No log file found"

echo ""
echo "================================================================================"
echo "To see full log: tail -f /tmp/abliterated_all_benchmarks.log"
echo "To check detailed progress: python3 -c \"import json; print(json.load(open('results/abliterated_falsereject_final.json'))['metadata'])\""
echo "================================================================================"
