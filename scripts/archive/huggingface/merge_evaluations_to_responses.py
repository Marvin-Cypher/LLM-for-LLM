#!/usr/bin/env python3
"""
Merge evaluation scores from *_eval_scores.json files into response files
to create complete TIER 3 evaluation datasets for HuggingFace upload.
"""

import json
from pathlib import Path

def merge_phase1_evaluations():
    """Merge Phase 1 evaluation scores into responses"""
    print("📊 Phase 1: Merging evaluations...")

    # Load responses
    with open('/Users/marvin/legal-llm-benchmark/results/phase1_responses.json', 'r') as f:
        responses = json.load(f)

    # Load evaluation scores
    with open('/Users/marvin/legal-llm-benchmark/results/phase1_all_models_eval_scores.json', 'r') as f:
        eval_data = json.load(f)

    scores_by_model = eval_data['scores_by_model']

    # Merge evaluations into responses
    for q_idx, question in enumerate(responses['questions']):
        for model_name, response_data in question.get('model_responses', {}).items():
            # Get scores for this model and question index
            if model_name in scores_by_model:
                model_scores = scores_by_model[model_name]
                q_idx_str = str(q_idx)

                if q_idx_str in model_scores:
                    scores = model_scores[q_idx_str]

                    # Calculate combined score (average of appropriateness and actionability)
                    appropriateness = scores.get('appropriateness', {})
                    actionability = scores.get('actionability', {})

                    app_score = appropriateness.get('appropriateness_score', 0)
                    act_score = actionability.get('actionability_score', 0)
                    combined_score = (app_score + act_score) / 2

                    # Detect refusal
                    refusal_type = appropriateness.get('refusal_type', 'direct_answer')
                    is_refusal = refusal_type in ['hard_refusal', 'soft_refusal']

                    # Add evaluation to response
                    response_data['evaluation'] = {
                        "score": round(combined_score, 1),
                        "appropriateness_score": app_score,
                        "actionability_score": act_score,
                        "is_refusal": is_refusal,
                        "refusal_type": refusal_type,
                        "contains_harmful": False,  # Phase 1 is all safety-trained
                        "appropriateness_reasoning": appropriateness.get('reasoning', ''),
                        "actionability_reasoning": actionability.get('reasoning', '')
                    }

    # Save merged data
    output_file = '/Users/marvin/legal-llm-benchmark/huggingface_datasets/3_evaluations_phase1.json'
    with open(output_file, 'w') as f:
        json.dump(responses, f, indent=2)

    print(f"  ✅ Merged {len(responses['questions'])} questions with evaluations")
    return len(responses['questions'])

def merge_phase3_evaluations():
    """Merge Phase 3 (FalseReject) evaluation scores into responses"""
    print("📊 Phase 3: Merging evaluations...")

    # Load responses
    with open('/Users/marvin/legal-llm-benchmark/results/phase3_responses.json', 'r') as f:
        responses = json.load(f)

    # Load evaluation scores
    with open('/Users/marvin/legal-llm-benchmark/results/falsereject_all_models_eval_scores.json', 'r') as f:
        eval_data = json.load(f)

    scores_by_model = eval_data['scores_by_model']

    # Merge evaluations into responses
    for q_idx, question in enumerate(responses['questions']):
        for model_name, response_data in question.get('model_responses', {}).items():
            # Get scores for this model and question index
            if model_name in scores_by_model:
                model_scores = scores_by_model[model_name]
                q_idx_str = str(q_idx)

                if q_idx_str in model_scores:
                    scores = model_scores[q_idx_str]

                    # Calculate combined score
                    appropriateness = scores.get('appropriateness', {})
                    actionability = scores.get('actionability', {})

                    app_score = appropriateness.get('appropriateness_score', 0)
                    act_score = actionability.get('actionability_score', 0)
                    combined_score = (app_score + act_score) / 2

                    # Detect refusal (critical for Phase 3!)
                    refusal_type = appropriateness.get('refusal_type', 'direct_answer')
                    is_refusal = refusal_type in ['hard_refusal', 'soft_refusal']

                    # Check for harmful content (ablated models)
                    contains_harmful = 'abliterated' in model_name.lower() and app_score <= 2

                    # Add evaluation to response
                    response_data['evaluation'] = {
                        "score": round(combined_score, 1),
                        "appropriateness_score": app_score,
                        "actionability_score": act_score,
                        "is_refusal": is_refusal,
                        "refusal_type": refusal_type,
                        "contains_harmful": contains_harmful,
                        "appropriateness_reasoning": appropriateness.get('reasoning', ''),
                        "actionability_reasoning": actionability.get('reasoning', '')
                    }

    # Save merged data
    output_file = '/Users/marvin/legal-llm-benchmark/huggingface_datasets/3_evaluations_phase3.json'
    with open(output_file, 'w') as f:
        json.dump(responses, f, indent=2)

    print(f"  ✅ Merged {len(responses['questions'])} questions with evaluations")
    return len(responses['questions'])

def merge_phase2_evaluations():
    """Merge Phase 2 evaluation scores into responses"""
    print("📊 Phase 2: Merging evaluations...")

    # Load responses (flattened structure)
    with open('/Users/marvin/legal-llm-benchmark/results/phase2_responses.json', 'r') as f:
        responses = json.load(f)

    # Load evaluation scores
    with open('/Users/marvin/legal-llm-benchmark/results/phase2_all_models_eval_scores.json', 'r') as f:
        eval_data = json.load(f)

    scores_by_model = eval_data['scores_by_model']

    # Phase 2 has flattened structure (each row is a model response)
    # Group by task_id to understand structure
    task_count = 0

    for task in responses['tasks']:
        model_name = task['model']
        task_id = task['task_id']

        # Find matching evaluation score
        if model_name in scores_by_model:
            # Phase 2 uses task_id as key
            model_scores = scores_by_model[model_name]

            if task_id in model_scores:
                scores = model_scores[task_id]

                # Calculate combined score
                appropriateness = scores.get('appropriateness', {})
                actionability = scores.get('actionability', {})

                app_score = appropriateness.get('appropriateness_score', 0)
                act_score = actionability.get('actionability_score', 0)
                combined_score = (app_score + act_score) / 2

                # Detect refusal
                refusal_type = appropriateness.get('refusal_type', 'direct_answer')
                is_refusal = refusal_type in ['hard_refusal', 'soft_refusal']

                # Add evaluation to task
                task['evaluation'] = {
                    "score": round(combined_score, 1),
                    "appropriateness_score": app_score,
                    "actionability_score": act_score,
                    "is_refusal": is_refusal,
                    "refusal_type": refusal_type,
                    "contains_harmful": False,
                    "appropriateness_reasoning": appropriateness.get('reasoning', ''),
                    "actionability_reasoning": actionability.get('reasoning', '')
                }
                task_count += 1

    # Save merged data
    output_file = '/Users/marvin/legal-llm-benchmark/huggingface_datasets/3_evaluations_phase2.json'
    with open(output_file, 'w') as f:
        json.dump(responses, f, indent=2)

    unique_tasks = len(set(task['task_id'] for task in responses['tasks']))
    print(f"  ✅ Merged {task_count} task responses ({unique_tasks} unique tasks)")
    return task_count

def main():
    print("=" * 70)
    print("  🔀 MERGING EVALUATION SCORES INTO RESPONSE FILES")
    print("=" * 70)
    print()

    # Merge all phases
    phase1_count = merge_phase1_evaluations()
    phase2_count = merge_phase2_evaluations()
    phase3_count = merge_phase3_evaluations()

    print()
    print("=" * 70)
    print("  ✅ EVALUATION MERGE COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"  Phase 1: {phase1_count} questions with merged evaluations")
    print(f"  Phase 2: {phase2_count} task responses with merged evaluations")
    print(f"  Phase 3: {phase3_count} questions with merged evaluations")
    print()
    print("📁 Output files:")
    print("  • huggingface_datasets/3_evaluations_phase1.json")
    print("  • huggingface_datasets/3_evaluations_phase2.json")
    print("  • huggingface_datasets/3_evaluations_phase3.json")
    print()
    print("✅ TIER 3 datasets now contain full evaluation data!")
    print("   - Quality scores (0-10)")
    print("   - Refusal labels (true/false)")
    print("   - Harmful content flags")
    print("   - Detailed evaluation reasoning")
    print()

if __name__ == "__main__":
    main()
