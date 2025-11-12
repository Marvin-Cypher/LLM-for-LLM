#!/usr/bin/env python3
"""
Create additional helpful datasets for HuggingFace:
1. Phase 2 contracts with embedded contract text
2. Practice area taxonomy
3. Detailed evaluation reasoning
4. Best vs Worst responses comparison
"""

import json
from pathlib import Path
from collections import defaultdict

def create_phase2_contracts_dataset():
    """Create Phase 2 contracts dataset with embedded contract text"""
    print("📄 Creating Phase 2 contracts dataset...")

    contracts_dir = Path('/Users/marvin/legal-llm-benchmark/data/phase2_contracts/contracts')
    tasks_dir = Path('/Users/marvin/legal-llm-benchmark/data/phase2_contracts/tasks')

    # Load all contract texts
    contracts = {}
    for contract_file in contracts_dir.glob('*.txt'):
        contract_id = contract_file.stem
        with open(contract_file, 'r') as f:
            contracts[contract_id] = f.read()

    # Load all tasks
    tasks_with_contracts = []
    for task_file in sorted(tasks_dir.glob('*.json')):
        with open(task_file, 'r') as f:
            task = json.load(f)

        # Get contract text
        contract_id = task.get('contract_id', '')
        contract_text = contracts.get(contract_id, '')

        # Flatten for JSONL
        row = {
            'task_id': task.get('task_id', ''),
            'contract_id': contract_id,
            'task_type': task.get('task_type', ''),
            'task_title': task.get('title', ''),
            'instruction': task.get('instruction', ''),
            'contract_text': contract_text,
            'contract_length': len(contract_text),
            'evaluation_criteria': ', '.join(task.get('evaluation_criteria', [])),
        }

        tasks_with_contracts.append(row)

    # Save as JSONL
    output_file = Path('/Users/marvin/legal-llm-benchmark/huggingface_datasets/phase2_contracts.jsonl')
    with open(output_file, 'w') as f:
        for row in tasks_with_contracts:
            f.write(json.dumps(row) + '\n')

    print(f"  ✅ Created {len(tasks_with_contracts)} contract tasks → phase2_contracts.jsonl")
    return len(tasks_with_contracts)

def create_practice_areas_dataset():
    """Create practice area taxonomy dataset"""
    print("📚 Creating practice area taxonomy...")

    with open('/Users/marvin/legal-llm-benchmark/data/practice_area_mapping.json', 'r') as f:
        data = json.load(f)

    # Flatten into rows
    taxonomy = []
    for major_category, subcategories in data['practice_area_categories'].items():
        for subcategory in subcategories:
            taxonomy.append({
                'major_category': major_category,
                'subcategory': subcategory,
                'category_id': subcategory,
            })

    # Save as JSONL
    output_file = Path('/Users/marvin/legal-llm-benchmark/huggingface_datasets/practice_areas.jsonl')
    with open(output_file, 'w') as f:
        for row in taxonomy:
            f.write(json.dumps(row) + '\n')

    print(f"  ✅ Created {len(taxonomy)} practice areas → practice_areas.jsonl")
    return len(taxonomy)

def create_detailed_evaluations_dataset():
    """Create detailed evaluation reasoning dataset"""
    print("📊 Creating detailed evaluation reasoning...")

    # Load Phase 1 eval scores
    with open('/Users/marvin/legal-llm-benchmark/results/phase1_all_models_eval_scores.json', 'r') as f:
        phase1_eval = json.load(f)

    detailed_evals = []

    for model_name, model_data in phase1_eval['scores_by_model'].items():
        for question_idx, scores in model_data.items():
            if question_idx in ['scores', 'count', 'mean', 'std', 'min', 'max']:
                continue  # Skip aggregated stats

            appropriateness = scores.get('appropriateness', {})
            actionability = scores.get('actionability', {})

            row = {
                'question_index': int(question_idx),
                'model': model_name,
                'appropriateness_score': appropriateness.get('appropriateness_score', 0),
                'appropriateness_reasoning': appropriateness.get('reasoning', ''),
                'refusal_type': appropriateness.get('refusal_type', ''),
                'actionability_score': actionability.get('actionability_score', 0),
                'actionability_reasoning': actionability.get('reasoning', ''),
                'has_specific_steps': actionability.get('has_specific_steps', False),
                'has_concrete_examples': actionability.get('has_concrete_examples', False),
            }

            detailed_evals.append(row)

    # Save as JSONL
    output_file = Path('/Users/marvin/legal-llm-benchmark/huggingface_datasets/detailed_evaluations.jsonl')
    with open(output_file, 'w') as f:
        for row in detailed_evals:
            f.write(json.dumps(row) + '\n')

    print(f"  ✅ Created {len(detailed_evals)} detailed evaluations → detailed_evaluations.jsonl")
    return len(detailed_evals)

def create_best_vs_worst_dataset():
    """Create best vs worst responses comparison dataset"""
    print("🏆 Creating best vs worst responses comparison...")

    # Load Phase 1 evaluations
    with open('/Users/marvin/legal-llm-benchmark/huggingface_datasets/3_evaluations_phase1.json', 'r') as f:
        phase1_data = json.load(f)

    comparisons = []

    for question in phase1_data['questions']:
        # Find best and worst responses
        responses_with_scores = []

        for model_name, response_data in question.get('model_responses', {}).items():
            evaluation = response_data.get('evaluation', {})
            score = evaluation.get('score', 0)
            is_refusal = evaluation.get('is_refusal', False)

            # Only consider non-refusals for "best"
            if not is_refusal:
                responses_with_scores.append({
                    'model': model_name,
                    'score': score,
                    'response': response_data.get('response', ''),
                    'refusal_type': evaluation.get('refusal_type', ''),
                })

        if len(responses_with_scores) >= 2:
            # Sort by score
            sorted_responses = sorted(responses_with_scores, key=lambda x: x['score'], reverse=True)

            best = sorted_responses[0]
            worst = sorted_responses[-1]

            # Find a refusal example if exists
            refusal_example = None
            for model_name, response_data in question.get('model_responses', {}).items():
                evaluation = response_data.get('evaluation', {})
                if evaluation.get('is_refusal', False):
                    refusal_example = {
                        'model': model_name,
                        'response': response_data.get('response', ''),
                        'refusal_type': evaluation.get('refusal_type', ''),
                    }
                    break

            row = {
                'question_id': question['question_id'],
                'question': question['question'],
                'category': question.get('category', ''),

                'best_model': best['model'],
                'best_score': best['score'],
                'best_response': best['response'][:500],  # Truncate for readability

                'worst_model': worst['model'],
                'worst_score': worst['score'],
                'worst_response': worst['response'][:500],

                'has_refusal_example': refusal_example is not None,
                'refusal_model': refusal_example['model'] if refusal_example else '',
                'refusal_response': refusal_example['response'][:200] if refusal_example else '',

                'score_gap': best['score'] - worst['score'],
            }

            comparisons.append(row)

    # Save as JSONL
    output_file = Path('/Users/marvin/legal-llm-benchmark/huggingface_datasets/best_vs_worst.jsonl')
    with open(output_file, 'w') as f:
        for row in comparisons:
            f.write(json.dumps(row) + '\n')

    print(f"  ✅ Created {len(comparisons)} comparisons → best_vs_worst.jsonl")
    return len(comparisons)

def create_phase3_detailed_analysis():
    """Create Phase 3 detailed refusal analysis"""
    print("🚨 Creating Phase 3 refusal analysis...")

    # Load Phase 3 evaluations
    with open('/Users/marvin/legal-llm-benchmark/huggingface_datasets/3_evaluations_phase3.json', 'r') as f:
        phase3_data = json.load(f)

    refusal_analysis = []

    for question in phase3_data['questions']:
        question_text = question['question']

        # Count refusals for this question
        refusals_count = 0
        answers_count = 0

        responses_list = []

        for model_name, response_data in question.get('model_responses', {}).items():
            evaluation = response_data.get('evaluation', {})
            is_refusal = evaluation.get('is_refusal', False)

            if is_refusal:
                refusals_count += 1
            else:
                answers_count += 1

            responses_list.append({
                'model': model_name,
                'is_refusal': is_refusal,
                'score': evaluation.get('score', 0),
                'refusal_type': evaluation.get('refusal_type', ''),
            })

        total = refusals_count + answers_count
        refusal_rate = (refusals_count / total * 100) if total > 0 else 0

        row = {
            'question_id': question['question_id'],
            'question': question_text,
            'total_models': total,
            'refusals_count': refusals_count,
            'answers_count': answers_count,
            'refusal_rate': round(refusal_rate, 1),
            'models_refusing': ', '.join([r['model'] for r in responses_list if r['is_refusal']]),
            'models_answering': ', '.join([r['model'] for r in responses_list if not r['is_refusal']]),
        }

        refusal_analysis.append(row)

    # Save as JSONL
    output_file = Path('/Users/marvin/legal-llm-benchmark/huggingface_datasets/phase3_refusal_analysis.jsonl')
    with open(output_file, 'w') as f:
        for row in refusal_analysis:
            f.write(json.dumps(row) + '\n')

    print(f"  ✅ Created {len(refusal_analysis)} refusal analyses → phase3_refusal_analysis.jsonl")
    return len(refusal_analysis)

def main():
    print("=" * 70)
    print("  📦 CREATING ADDITIONAL HELPFUL DATASETS FOR HUGGINGFACE")
    print("=" * 70)
    print()

    # Create all datasets
    contracts_count = create_phase2_contracts_dataset()
    areas_count = create_practice_areas_dataset()
    detailed_count = create_detailed_evaluations_dataset()
    comparison_count = create_best_vs_worst_dataset()
    refusal_count = create_phase3_detailed_analysis()

    print()
    print("=" * 70)
    print("  ✅ ALL ADDITIONAL DATASETS CREATED!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"  1. Phase 2 Contracts: {contracts_count} tasks with contract text")
    print(f"  2. Practice Areas: {areas_count} legal categories")
    print(f"  3. Detailed Evaluations: {detailed_count} evaluation reasonings")
    print(f"  4. Best vs Worst: {comparison_count} response comparisons")
    print(f"  5. Refusal Analysis: {refusal_count} question-level refusal stats")
    print()
    print("📁 Files created:")
    print("  • phase2_contracts.jsonl")
    print("  • practice_areas.jsonl")
    print("  • detailed_evaluations.jsonl")
    print("  • best_vs_worst.jsonl")
    print("  • phase3_refusal_analysis.jsonl")
    print()

if __name__ == "__main__":
    main()
