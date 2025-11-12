#!/usr/bin/env python3
"""
Merge Phase 2 quality evaluation scores from batch API results into the main Phase 2 dataset
Version 2: Uses task_id matching from custom_id
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def load_batch_scores_by_task_id(batch_file: Path, model: str):
    """Load scores indexed by task_id extracted from custom_id"""
    scores = {}

    with open(batch_file, 'r') as f:
        for line in f:
            result = json.loads(line)

            try:
                if result['response']['status_code'] == 200:
                    custom_id = result['custom_id']
                    content = result['response']['body']['choices'][0]['message']['content']
                    eval_data = json.loads(content)

                    # Extract task_id from custom_id: "model___task_id"
                    parts = custom_id.split('___')
                    if len(parts) >= 2:
                        task_id = parts[1]  # e.g., "contract_001_add_clause_1" or "None"
                        scores[task_id] = {
                            'score': eval_data['score'],
                            'justification': eval_data.get('justification', '')
                        }
            except Exception as e:
                print(f"Warning: Failed to parse {result.get('custom_id', 'unknown')}: {e}")

    return scores

def main():
    results_dir = BASE_DIR / "results"

    batch_files = [
        ('batch_quality_qwen3_output.jsonl', 'qwen3-vl-abliterated:30b'),
        ('batch_quality_gemma3_output.jsonl', 'gemma3-abliterated:27b'),
    ]

    print("=" * 80)
    print("MERGING PHASE 2 QUALITY EVALUATION SCORES - V2")
    print("=" * 80)

    # Load batch scores by model
    model_scores = {}
    for filename, model in batch_files:
        batch_file = results_dir / filename
        print(f"\nLoading {filename}...")
        scores = load_batch_scores_by_task_id(batch_file, model)
        model_scores[model] = scores
        print(f"  Loaded {len(scores)} scores")
        print(f"  Sample task_ids: {list(scores.keys())[:3]}")

    # Load Phase 2 dataset
    phase2_file = results_dir / "phase2_final_with_abliterated.json"
    print(f"\nLoading Phase 2 dataset: {phase2_file}")

    with open(phase2_file, 'r') as f:
        phase2_data = json.load(f)

    print(f"  Total tasks: {len(phase2_data['tasks'])}")

    # Merge scores
    scores_added = 0
    models_updated = set()

    for task in phase2_data['tasks']:
        task_id = task.get('task_id', 'None')

        # Check if this task has model_responses dict
        if 'model_responses' not in task:
            continue

        for model, model_data in task['model_responses'].items():
            if 'abliterated' not in model:
                continue

            if model not in model_scores:
                continue

            # Look up score by task_id
            if task_id in model_scores[model]:
                score_info = model_scores[model][task_id]

                # Add evaluation
                if 'evaluation' not in model_data:
                    model_data['evaluation'] = {}

                model_data['evaluation']['quality_score'] = score_info['score']
                model_data['evaluation']['quality_justification'] = score_info['justification']

                scores_added += 1
                models_updated.add(model)

    print(f"\n✅ Updated {scores_added} model responses")
    print(f"   Models updated: {', '.join(sorted(models_updated))}")

    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    for model in sorted(models_updated):
        quality_vals = []

        for task in phase2_data['tasks']:
            if 'model_responses' in task and model in task['model_responses']:
                model_data = task['model_responses'][model]
                if 'evaluation' in model_data and 'quality_score' in model_data['evaluation']:
                    quality_vals.append(model_data['evaluation']['quality_score'])

        if quality_vals:
            avg = sum(quality_vals) / len(quality_vals)
            print(f"\n{model}:")
            print(f"  Quality Score: {avg:.2f}/10 (n={len(quality_vals)})")

            # Distribution
            bins = {'0-2': 0, '3-4': 0, '5-6': 0, '7-8': 0, '9-10': 0}
            for s in quality_vals:
                if s <= 2:
                    bins['0-2'] += 1
                elif s <= 4:
                    bins['3-4'] += 1
                elif s <= 6:
                    bins['5-6'] += 1
                elif s <= 8:
                    bins['7-8'] += 1
                else:
                    bins['9-10'] += 1

            print(f"  Distribution:")
            for range_label, count in bins.items():
                pct = count / len(quality_vals) * 100
                print(f"    {range_label}: {count:3d} ({pct:5.1f}%)")

    # Save
    output_file = results_dir / "phase2_final_with_abliterated_scored.json"
    print(f"\n💾 Saving to: {output_file}")

    with open(output_file, 'w') as f:
        json.dump(phase2_data, f, indent=2)

    print(f"✅ Saved! File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")

    print("\n" + "=" * 80)
    print("🎉 PHASE 2 EVALUATION MERGE COMPLETE")
    print("=" * 80)
    print("\n✅ ALL ABLITERATED MODEL EVALUATIONS COMPLETE!")
    print("\nNext steps:")
    print("1. Generate comprehensive comparison analysis")
    print("2. Create figures comparing abliterated vs standard models")
    print("3. Update paper with complete abliterated findings")
    print("=" * 80)

if __name__ == "__main__":
    main()
