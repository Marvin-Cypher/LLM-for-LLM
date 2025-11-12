#!/usr/bin/env python3
"""
Merge Phase 2 quality evaluation scores from batch API results into the main Phase 2 dataset
"""

import json
from pathlib import Path
from typing import Dict

BASE_DIR = Path(__file__).parent.parent

def load_batch_scores(batch_file: Path) -> Dict[str, float]:
    """
    Load scores from a batch output file

    Returns dict mapping: {model___task_id: score}
    """
    scores = {}

    with open(batch_file, 'r') as f:
        for line in f:
            result = json.loads(line)

            try:
                if result['response']['status_code'] == 200:
                    custom_id = result['custom_id']
                    content = result['response']['body']['choices'][0]['message']['content']
                    eval_data = json.loads(content)
                    score = eval_data['score']

                    # Custom ID format for Phase 2: model___None or model___task_description
                    # We need to match by model and task index
                    scores[custom_id] = {
                        'score': score,
                        'justification': eval_data.get('justification', '')
                    }
            except Exception as e:
                print(f"Warning: Failed to parse result {result.get('custom_id', 'unknown')}: {e}")
                continue

    return scores

def main():
    # Load batch evaluation results
    results_dir = BASE_DIR / "results"

    batch_files = [
        ('batch_quality_qwen3_output.jsonl', 'qwen3-vl-abliterated:30b'),
        ('batch_quality_gemma3_output.jsonl', 'gemma3-abliterated:27b'),
    ]

    print("=" * 80)
    print("MERGING PHASE 2 QUALITY EVALUATION SCORES")
    print("=" * 80)

    # Load all scores
    all_scores = {}

    for filename, model in batch_files:
        batch_file = results_dir / filename
        print(f"\nLoading {filename}...")

        scores = load_batch_scores(batch_file)
        all_scores[model] = scores
        print(f"  Loaded {len(scores)} scores for {model}")

    # Load the merged Phase 2 dataset
    phase2_file = results_dir / "phase2_final_with_abliterated.json"
    print(f"\nLoading Phase 2 dataset: {phase2_file}")

    with open(phase2_file, 'r') as f:
        phase2_data = json.load(f)

    print(f"  Total tasks: {len(phase2_data['tasks'])}")

    # Merge scores into the dataset
    # Note: Phase 2 has a different structure with 'tasks' instead of 'questions'
    scores_added = 0
    models_updated = set()

    for task_idx, task in enumerate(phase2_data['tasks']):
        task_id = task.get('task_id', f'task_{task_idx}')

        # model_responses is a dict: {model: {response, metadata, ...}}
        for model, model_data in task['model_responses'].items():
            # Only update abliterated models
            if 'abliterated' not in model:
                continue

            if model not in all_scores:
                continue

            # Try to find matching score
            # The custom_id in batch might be model___None or model___description
            score_data = None
            for custom_id, data in all_scores[model].items():
                if custom_id.startswith(f"{model}___"):
                    # Match by position (batch results are in order)
                    score_data = data
                    break

            if score_data:
                # Initialize evaluation dict if needed
                if 'evaluation' not in model_data:
                    model_data['evaluation'] = {}

                model_data['evaluation']['quality_score'] = score_data['score']
                model_data['evaluation']['quality_justification'] = score_data['justification']

                models_updated.add(model)
                scores_added += 1

                # Remove used score to ensure we don't reuse it
                if score_data:
                    for k, v in list(all_scores[model].items()):
                        if v == score_data:
                            del all_scores[model][k]
                            break

    print(f"\n✅ Updated {scores_added} model responses")
    print(f"   Models updated: {', '.join(sorted(models_updated))}")

    # Calculate and display summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    for model in sorted(models_updated):
        quality_vals = []

        for task in phase2_data['tasks']:
            if model in task['model_responses']:
                model_response = task['model_responses'][model]
                if 'evaluation' in model_response:
                    if 'quality_score' in model_response['evaluation']:
                        quality_vals.append(model_response['evaluation']['quality_score'])

        print(f"\n{model}:")
        if quality_vals:
            avg_qual = sum(quality_vals) / len(quality_vals)
            print(f"  Quality Score:    {avg_qual:.2f}/10 (n={len(quality_vals)})")

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

    # Save updated dataset
    output_file = results_dir / "phase2_final_with_abliterated_scored.json"
    print(f"\n💾 Saving updated dataset to: {output_file}")

    with open(output_file, 'w') as f:
        json.dump(phase2_data, f, indent=2)

    print(f"✅ Saved! File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")

    print("\n" + "=" * 80)
    print("PHASE 2 EVALUATION MERGE COMPLETE")
    print("=" * 80)
    print("Next steps:")
    print("1. Generate comprehensive comparison analysis (Phase 1 + Phase 2 + FalseReject)")
    print("2. Create figures comparing abliterated vs standard models")
    print("3. Update paper with complete abliterated model findings")
    print("=" * 80)

if __name__ == "__main__":
    main()
