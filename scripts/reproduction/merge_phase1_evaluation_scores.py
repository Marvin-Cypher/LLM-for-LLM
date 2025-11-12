#!/usr/bin/env python3
"""
Merge Phase 1 evaluation scores from batch API results into the main Phase 1 dataset
"""

import json
from pathlib import Path
from typing import Dict

BASE_DIR = Path(__file__).parent.parent

def load_batch_scores(batch_file: Path, dimension: str) -> Dict[str, float]:
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

                    # Parse custom_id: model___task_id___dimension
                    parts = custom_id.split('___')
                    if len(parts) >= 2:
                        model = parts[0]
                        task_id = parts[1]
                        key = f"{model}___{task_id}"
                        scores[key] = score
            except Exception as e:
                print(f"Warning: Failed to parse result {result.get('custom_id', 'unknown')}: {e}")
                continue

    return scores

def main():
    # Load batch evaluation results
    results_dir = BASE_DIR / "results"

    batch_files = [
        ('batch_actionability_qwen3_output.jsonl', 'qwen3-vl-abliterated:30b', 'actionability'),
        ('batch_appropriateness_qwen3_output.jsonl', 'qwen3-vl-abliterated:30b', 'appropriateness'),
        ('batch_actionability_gemma3_output.jsonl', 'gemma3-abliterated:27b', 'actionability'),
        ('batch_appropriateness_gemma3_output.jsonl', 'gemma3-abliterated:27b', 'appropriateness'),
    ]

    print("=" * 80)
    print("MERGING PHASE 1 EVALUATION SCORES")
    print("=" * 80)

    # Load all scores by dimension
    actionability_scores = {}
    appropriateness_scores = {}

    for filename, model, dimension in batch_files:
        batch_file = results_dir / filename
        print(f"\nLoading {filename}...")

        scores = load_batch_scores(batch_file, dimension)
        print(f"  Loaded {len(scores)} scores")

        if dimension == 'actionability':
            actionability_scores.update(scores)
        else:
            appropriateness_scores.update(scores)

    print(f"\nTotal actionability scores: {len(actionability_scores)}")
    print(f"Total appropriateness scores: {len(appropriateness_scores)}")

    # Load the merged Phase 1 dataset
    phase1_file = results_dir / "phase1_final_with_abliterated.json"
    print(f"\nLoading Phase 1 dataset: {phase1_file}")

    with open(phase1_file, 'r') as f:
        phase1_data = json.load(f)

    print(f"  Total questions: {len(phase1_data['questions'])}")

    # Merge scores into the dataset
    models_updated = set()
    scores_added = 0

    for question in phase1_data['questions']:
        question_id = question['question_id']

        # model_responses is a dict, not a list
        for model, model_response in question['model_responses'].items():
            # Only update abliterated models
            if 'abliterated' not in model:
                continue

            key = f"{model}___{question_id}"

            # Add scores if available
            if key in actionability_scores and key in appropriateness_scores:
                # Initialize evaluation dict if needed
                if 'evaluation' not in model_response:
                    model_response['evaluation'] = {}

                model_response['evaluation']['actionability_score'] = actionability_scores[key]
                model_response['evaluation']['appropriateness_score'] = appropriateness_scores[key]

                models_updated.add(model)
                scores_added += 1
            elif key in actionability_scores or key in appropriateness_scores:
                print(f"  Warning: Partial scores for {key}")

    print(f"\n✅ Updated {scores_added} model responses")
    print(f"   Models updated: {', '.join(sorted(models_updated))}")

    # Calculate and display summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    for model in sorted(models_updated):
        actionability_vals = []
        appropriateness_vals = []

        for question in phase1_data['questions']:
            if model in question['model_responses']:
                model_response = question['model_responses'][model]
                if 'evaluation' in model_response:
                    if 'actionability_score' in model_response['evaluation']:
                        actionability_vals.append(model_response['evaluation']['actionability_score'])
                    if 'appropriateness_score' in model_response['evaluation']:
                        appropriateness_vals.append(model_response['evaluation']['appropriateness_score'])

        print(f"\n{model}:")
        if actionability_vals:
            avg_act = sum(actionability_vals) / len(actionability_vals)
            print(f"  Actionability:    {avg_act:.2f}/10 (n={len(actionability_vals)})")
        if appropriateness_vals:
            avg_app = sum(appropriateness_vals) / len(appropriateness_vals)
            print(f"  Appropriateness:  {avg_app:.2f}/10 (n={len(appropriateness_vals)})")

        if actionability_vals and appropriateness_vals:
            overall = (sum(actionability_vals) + sum(appropriateness_vals)) / (len(actionability_vals) + len(appropriateness_vals))
            print(f"  Overall Average:  {overall:.2f}/10")

    # Save updated dataset
    output_file = results_dir / "phase1_final_with_abliterated_scored.json"
    print(f"\n💾 Saving updated dataset to: {output_file}")

    with open(output_file, 'w') as f:
        json.dump(phase1_data, f, indent=2)

    print(f"✅ Saved! File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")

    print("\n" + "=" * 80)
    print("PHASE 1 EVALUATION MERGE COMPLETE")
    print("=" * 80)
    print("Next steps:")
    print("1. Wait for Phase 2 evaluation batches to complete")
    print("2. Run similar merge script for Phase 2 scores")
    print("3. Generate comparative analysis figures")
    print("=" * 80)

if __name__ == "__main__":
    main()
