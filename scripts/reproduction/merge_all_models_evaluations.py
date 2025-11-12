#!/usr/bin/env python3
"""
Merge ALL models evaluation scores (appropriateness, actionability, falsereject)
into the comprehensive dataset for figure generation.

This processes:
- 1,236 appropriateness evaluations (Phase 1, ALL models)
- 1,240 actionability evaluations (Phase 1, ALL models)
- 239 falsereject evaluations (FalseReject, ALL models)
"""

import json
from collections import defaultdict

def load_batch_evaluations(filepath):
    """Load batch evaluation JSONL file"""
    evaluations = []
    with open(filepath, 'r') as f:
        for line in f:
            evaluations.append(json.loads(line))
    return evaluations

def parse_custom_id(custom_id):
    """Parse custom_id to extract question_id and model

    Format examples:
    - approp_phase1_qa_0_anthropic/claude-sonnet-4.5_0
    - action_phase1_qa_0_openai/gpt-5_1
    - falsereject_0_anthropic/claude-sonnet-4.5_0
    """
    if custom_id.startswith('falsereject_'):
        # falsereject_0_anthropic/claude-sonnet-4.5_0
        # Remove 'falsereject_', then split on last '_' to get (question_model, idx)
        after_prefix = custom_id[len('falsereject_'):]
        parts = after_prefix.rsplit('_', 1)
        # parts[0] = '0_anthropic/claude-sonnet-4.5', parts[1] = '0'
        question_and_model = parts[0]
        # Split on first '_' to get question_idx and model
        question_idx_str, model = question_and_model.split('_', 1)
        return 'falsereject', int(question_idx_str), model
    elif custom_id.startswith('approp_falsereject_') or custom_id.startswith('action_falsereject_'):
        # approp_falsereject_0_anthropic/claude-sonnet-4.5_1000
        # This is appropriateness evaluation of falsereject responses
        if custom_id.startswith('approp_'):
            dimension = 'appropriateness'
            after_dim = custom_id[len('approp_falsereject_'):]
        else:
            dimension = 'actionability'
            after_dim = custom_id[len('action_falsereject_'):]

        # after_dim = '0_anthropic/claude-sonnet-4.5_1000'
        parts = after_dim.rsplit('_', 1)
        question_and_model = parts[0]
        question_idx_str, model = question_and_model.split('_', 1)
        return f'{dimension}_falsereject', int(question_idx_str), model
    else:
        # approp_phase1_qa_0_anthropic/claude-sonnet-4.5_0 or
        # action_phase1_qa_0_anthropic/claude-sonnet-4.5_0
        # Format: {dimension}_phase1_qa_{q_idx}_{model}_{idx}
        # Remove dimension prefix first
        if custom_id.startswith('approp_'):
            dimension = 'appropriateness'
            after_dim = custom_id[len('approp_'):]
        else:
            dimension = 'actionability'
            after_dim = custom_id[len('action_'):]

        # after_dim = 'phase1_qa_0_anthropic/claude-sonnet-4.5_0'
        # Remove 'phase1_qa_', then split on last '_'
        after_prefix = after_dim[len('phase1_qa_'):]
        parts = after_prefix.rsplit('_', 1)
        # parts[0] = '0_anthropic/claude-sonnet-4.5', parts[1] = '0'
        question_and_model = parts[0]
        # Split on first '_'
        question_idx_str, model = question_and_model.split('_', 1)
        return dimension, int(question_idx_str), model

def extract_evaluation_scores(eval_data):
    """Extract scores from evaluation response"""
    try:
        resp_body = eval_data['response']['body']
        content = resp_body['choices'][0]['message']['content']
        scores = json.loads(content)
        return scores
    except Exception as e:
        print(f"  Error parsing evaluation: {e}")
        return None

def main():
    print("="*80)
    print("MERGING ALL MODELS EVALUATION SCORES")
    print("="*80)

    # Load all batch evaluations
    print("\n📥 Loading batch evaluations...")
    approp_evals = load_batch_evaluations('results/batch_appropriateness_all_models_output.jsonl')
    action_evals = load_batch_evaluations('results/batch_actionability_all_models_output.jsonl')
    falsereject_evals = load_batch_evaluations('results/batch_falsereject_all_models_output.jsonl')

    print(f"   Appropriateness: {len(approp_evals)} evaluations")
    print(f"   Actionability: {len(action_evals)} evaluations")
    print(f"   FalseReject: {len(falsereject_evals)} evaluations")

    # Organize by model and question
    print("\n🔄 Organizing evaluations by model and question...")

    phase1_scores = defaultdict(lambda: defaultdict(dict))
    falsereject_scores = defaultdict(lambda: defaultdict(dict))

    # Process appropriateness
    for eval_data in approp_evals:
        custom_id = eval_data['custom_id']
        try:
            dim, q_idx, model = parse_custom_id(custom_id)
            scores = extract_evaluation_scores(eval_data)

            if scores and dim == 'appropriateness':
                phase1_scores[model][q_idx]['appropriateness'] = scores
        except Exception as e:
            print(f"  Error processing approp custom_id '{custom_id}': {e}")

    # Process actionability
    for eval_data in action_evals:
        custom_id = eval_data['custom_id']
        try:
            dim, q_idx, model = parse_custom_id(custom_id)
            scores = extract_evaluation_scores(eval_data)

            if scores and dim == 'actionability':
                phase1_scores[model][q_idx]['actionability'] = scores
        except Exception as e:
            print(f"  Error processing action custom_id '{custom_id}': {e}")

    # Process falsereject
    for eval_data in falsereject_evals:
        custom_id = eval_data['custom_id']
        try:
            dim, q_idx, model = parse_custom_id(custom_id)
            scores = extract_evaluation_scores(eval_data)

            if scores:
                falsereject_scores[model][q_idx] = scores
        except Exception as e:
            print(f"  Error processing falsereject custom_id '{custom_id}': {e}")

    print(f"\n✅ Organized evaluations:")
    print(f"   Phase 1 models: {len(phase1_scores)}")
    print(f"   FalseReject models: {len(falsereject_scores)}")

    # Print model coverage
    print("\n📊 Models in Phase 1 evaluations:")
    for model in sorted(phase1_scores.keys()):
        q_count = len(phase1_scores[model])
        print(f"   {model}: {q_count} questions")

    print("\n📊 Models in FalseReject evaluations:")
    for model in sorted(falsereject_scores.keys()):
        q_count = len(falsereject_scores[model])
        print(f"   {model}: {q_count} questions")

    # Save organized data
    print("\n💾 Saving organized evaluation data...")

    phase1_output = {
        'metadata': {
            'total_models': len(phase1_scores),
            'total_evaluations': len(approp_evals) + len(action_evals),
            'dimensions': ['appropriateness', 'actionability']
        },
        'scores_by_model': dict(phase1_scores)
    }

    with open('results/phase1_all_models_eval_scores.json', 'w') as f:
        json.dump(phase1_output, f, indent=2)
    print(f"   ✅ Saved: results/phase1_all_models_eval_scores.json")

    falsereject_output = {
        'metadata': {
            'total_models': len(falsereject_scores),
            'total_evaluations': len(falsereject_evals),
            'questions': 24
        },
        'scores_by_model': dict(falsereject_scores)
    }

    with open('results/falsereject_all_models_eval_scores.json', 'w') as f:
        json.dump(falsereject_output, f, indent=2)
    print(f"   ✅ Saved: results/falsereject_all_models_eval_scores.json")

    # Generate summary statistics
    print("\n" + "="*80)
    print("📈 SUMMARY STATISTICS")
    print("="*80)

    # Phase 1 average scores
    print("\nPhase 1 Average Scores by Model:")
    print("-"*80)

    for model in sorted(phase1_scores.keys()):
        approp_scores = []
        action_scores = []

        for q_idx, dims in phase1_scores[model].items():
            if 'appropriateness' in dims:
                score = dims['appropriateness'].get('appropriateness_score')
                if score is not None:
                    approp_scores.append(score)
            if 'actionability' in dims:
                score = dims['actionability'].get('actionability_score')
                if score is not None:
                    action_scores.append(score)

        if approp_scores and action_scores:
            avg_approp = sum(approp_scores) / len(approp_scores)
            avg_action = sum(action_scores) / len(action_scores)
            avg_overall = (avg_approp + avg_action) / 2

            print(f"{model:45} | Approp: {avg_approp:.2f} | Action: {avg_action:.2f} | Overall: {avg_overall:.2f}")

    # FalseReject stats
    print("\n\nFalseReject False Positive Rates:")
    print("-"*80)

    for model in sorted(falsereject_scores.keys()):
        false_positives = 0
        total = len(falsereject_scores[model])

        for q_idx, scores in falsereject_scores[model].items():
            if scores.get('is_false_positive', False):
                false_positives += 1

        fp_rate = (false_positives / total * 100) if total > 0 else 0
        print(f"{model:45} | {false_positives}/{total} false positives ({fp_rate:.1f}%)")

    print("\n" + "="*80)
    print("✅ MERGE COMPLETE!")
    print("="*80)
    print("\n📋 Next Steps:")
    print("1. Generate comprehensive figures with ALL models data")
    print("2. Compare standard models vs abliterated models")
    print("3. Update paper with complete analysis")

if __name__ == '__main__':
    main()
