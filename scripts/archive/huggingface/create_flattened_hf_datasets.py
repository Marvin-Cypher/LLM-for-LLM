#!/usr/bin/env python3
"""
Create flattened versions of datasets for HuggingFace viewer compatibility.

The HuggingFace viewer requires consistent column types. We'll create flattened
versions where each row is a single model response to a question.
"""

import json
from pathlib import Path

def flatten_phase1_evaluations():
    """Flatten Phase 1: Each row = one model response to one question"""
    print("📊 Flattening Phase 1 evaluations...")

    with open('/Users/marvin/legal-llm-benchmark/huggingface_datasets/3_evaluations_phase1.json', 'r') as f:
        data = json.load(f)

    flattened = []

    for question in data['questions']:
        for model_name, response_data in question['model_responses'].items():
            evaluation = response_data.get('evaluation', {})

            row = {
                'question_id': question['question_id'],
                'question': question['question'],
                'category': question.get('category', ''),
                'model': model_name,
                'response': response_data.get('response', ''),
                'score': evaluation.get('score', 0.0),
                'appropriateness_score': evaluation.get('appropriateness_score', 0),
                'actionability_score': evaluation.get('actionability_score', 0),
                'is_refusal': evaluation.get('is_refusal', False),
                'refusal_type': evaluation.get('refusal_type', ''),
                'contains_harmful': evaluation.get('contains_harmful', False),
            }

            flattened.append(row)

    # Save as JSONL (one JSON object per line - HuggingFace prefers this)
    output_file = '/Users/marvin/legal-llm-benchmark/huggingface_datasets/phase1_flat.jsonl'
    with open(output_file, 'w') as f:
        for row in flattened:
            f.write(json.dumps(row) + '\n')

    print(f"  ✅ Created {len(flattened)} rows → phase1_flat.jsonl")
    return len(flattened)

def flatten_phase3_evaluations():
    """Flatten Phase 3: Each row = one model response to one FalseReject question"""
    print("📊 Flattening Phase 3 evaluations...")

    with open('/Users/marvin/legal-llm-benchmark/huggingface_datasets/3_evaluations_phase3.json', 'r') as f:
        data = json.load(f)

    flattened = []

    for question in data['questions']:
        for model_name, response_data in question['model_responses'].items():
            evaluation = response_data.get('evaluation', {})

            row = {
                'question_id': question['question_id'],
                'question': question['question'],
                'category': question.get('category', ''),
                'model': model_name,
                'response': response_data.get('response', ''),
                'score': evaluation.get('score', 0.0),
                'appropriateness_score': evaluation.get('appropriateness_score', 0),
                'actionability_score': evaluation.get('actionability_score', 0),
                'is_refusal': evaluation.get('is_refusal', False),
                'refusal_type': evaluation.get('refusal_type', ''),
                'contains_harmful': evaluation.get('contains_harmful', False),
            }

            flattened.append(row)

    # Save as JSONL
    output_file = '/Users/marvin/legal-llm-benchmark/huggingface_datasets/phase3_flat.jsonl'
    with open(output_file, 'w') as f:
        for row in flattened:
            f.write(json.dumps(row) + '\n')

    print(f"  ✅ Created {len(flattened)} rows → phase3_flat.jsonl")
    return len(flattened)

def flatten_questions():
    """Flatten questions files"""
    print("📊 Flattening questions...")

    # Phase 1 questions
    with open('/Users/marvin/legal-llm-benchmark/huggingface_datasets/1_questions_phase1.json', 'r') as f:
        phase1_data = json.load(f)

    questions_flat = []
    for q in phase1_data['questions']:
        questions_flat.append({
            'id': q.get('id', ''),
            'question': q.get('question', ''),
            'category': q.get('category', ''),
            'difficulty': q.get('difficulty', ''),
            'expected_behavior': q.get('expected_behavior', ''),
            'phase': 'phase1'
        })

    # Phase 3 questions
    with open('/Users/marvin/legal-llm-benchmark/huggingface_datasets/1_questions_phase3.json', 'r') as f:
        phase3_data = json.load(f)

    for q in phase3_data['questions']:
        questions_flat.append({
            'id': str(q.get('id', '')),
            'question': q.get('question', ''),
            'category': q.get('category', ''),
            'difficulty': q.get('difficulty', ''),
            'expected_behavior': q.get('expected_behavior', ''),
            'phase': 'phase3'
        })

    # Save as JSONL
    output_file = '/Users/marvin/legal-llm-benchmark/huggingface_datasets/all_questions_flat.jsonl'
    with open(output_file, 'w') as f:
        for row in questions_flat:
            f.write(json.dumps(row) + '\n')

    print(f"  ✅ Created {len(questions_flat)} rows → all_questions_flat.jsonl")
    return len(questions_flat)

def main():
    print("=" * 70)
    print("  🔄 CREATING FLATTENED DATASETS FOR HUGGINGFACE VIEWER")
    print("=" * 70)
    print()

    phase1_count = flatten_phase1_evaluations()
    phase3_count = flatten_phase3_evaluations()
    questions_count = flatten_questions()

    print()
    print("=" * 70)
    print("  ✅ FLATTENED DATASETS CREATED!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"  Phase 1 evaluations: {phase1_count} rows (12 models × 100 questions)")
    print(f"  Phase 3 evaluations: {phase3_count} rows (10 models × 24 questions)")
    print(f"  All questions: {questions_count} rows (100 + 24 questions)")
    print()
    print("📁 Files created:")
    print("  • phase1_flat.jsonl (easy for HuggingFace viewer)")
    print("  • phase3_flat.jsonl (easy for HuggingFace viewer)")
    print("  • all_questions_flat.jsonl (all questions combined)")
    print()
    print("🔧 These flattened files will work better with the HuggingFace viewer!")
    print()

if __name__ == "__main__":
    main()
