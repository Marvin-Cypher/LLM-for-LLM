#!/usr/bin/env python3
"""
Prepare Legal LLM Benchmark datasets for HuggingFace upload

Creates 3 tiers of datasets:
1. Questions only (input data for researchers)
2. Responses (questions + AI answers, no evaluation)
3. Evaluations (questions + answers + scores - full dataset)
"""

import json
from pathlib import Path

def main():
    # Setup
    repo_root = Path('/Users/marvin/legal-llm-benchmark')
    output_dir = repo_root / 'huggingface_datasets'
    output_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("  📦 LEGAL LLM BENCHMARK - HuggingFace Dataset Preparation")
    print("=" * 70)

    # ============================================
    # TIER 1: QUESTIONS ONLY (Input Data)
    # ============================================
    print("\n📝 TIER 1: Creating Question-only datasets...\n")

    # Phase 1: Legal Q&A (already a clean questions file)
    with open(repo_root / 'data/phase1_questions.json', 'r') as f:
        phase1_questions_list = json.load(f)

    phase1_questions = {
        "metadata": {
            "phase": "phase1_legal_qa",
            "total_questions": len(phase1_questions_list),
            "description": "100 realistic legal Q&A questions covering 68+ practice areas",
            "task_type": "question_answering",
            "file_context": False
        },
        "questions": phase1_questions_list
    }

    with open(output_dir / '1_questions_phase1.json', 'w') as f:
        json.dump(phase1_questions, f, indent=2)
    print(f"  ✅ Phase 1: {len(phase1_questions_list)} questions → 1_questions_phase1.json")

    # Phase 2: Contract tasks (extract from results, uses 'tasks' key)
    with open(repo_root / 'results/phase2_responses.json', 'r') as f:
        phase2_data = json.load(f)

    phase2_questions_list = []
    for task in phase2_data['tasks']:  # Note: uses 'tasks' not 'questions'
        phase2_questions_list.append({
            "task_id": task['task_id'],
            "question": task['question'],
            "category": task.get('category', 'contract_analysis'),
            "task_type": task.get('task_type', 'unknown'),
            "contract_id": task.get('contract_id', 'unknown')
        })

    phase2_questions = {
        "metadata": {
            "phase": "phase2_contracts",
            "total_questions": len(phase2_questions_list),
            "description": "39 contract analysis tasks with document context",
            "task_type": "document_analysis",
            "file_context": True
        },
        "questions": phase2_questions_list
    }

    with open(output_dir / '1_questions_phase2.json', 'w') as f:
        json.dump(phase2_questions, f, indent=2)
    print(f"  ✅ Phase 2: {len(phase2_questions_list)} questions → 1_questions_phase2.json")

    # Phase 3: FalseReject (already extracted)
    with open(repo_root / 'data/phase3_falsereject_questions.json', 'r') as f:
        phase3_questions = json.load(f)

    with open(output_dir / '1_questions_phase3.json', 'w') as f:
        json.dump(phase3_questions, f, indent=2)
    print(f"  ✅ Phase 3: {len(phase3_questions['questions'])} questions → 1_questions_phase3.json")

    # ============================================
    # TIER 2: RESPONSES (Questions + AI Answers)
    # ============================================
    print("\n🤖 TIER 2: Creating Responses datasets (questions + AI answers)...\n")

    # Phase 1: Uses 'questions' key
    with open(repo_root / 'results/phase1_responses.json', 'r') as f:
        phase1_data = json.load(f)

    phase1_responses = {
        "metadata": phase1_data.get('metadata', {}),
        "questions": []
    }

    for q in phase1_data['questions']:
        q_data = {
            "question_id": q['question_id'],
            "question": q['question'],
            "category": q.get('category', 'unknown'),
            "model_responses": {}
        }

        for model, resp_data in q.get('model_responses', {}).items():
            q_data['model_responses'][model] = {
                "response": resp_data.get('response', ''),
                "timestamp": resp_data.get('timestamp', ''),
                "error": resp_data.get('error', None)
            }

        phase1_responses['questions'].append(q_data)

    with open(output_dir / '2_responses_phase1.json', 'w') as f:
        json.dump(phase1_responses, f, indent=2)

    model_count = len(phase1_data.get('metadata', {}).get('models', []))
    print(f"  ✅ Phase 1: {len(phase1_responses['questions'])} questions × {model_count} models → 2_responses_phase1.json")

    # Phase 2: Uses 'tasks' key
    phase2_responses = {
        "metadata": phase2_data.get('metadata', {}),
        "tasks": []
    }

    for task in phase2_data['tasks']:
        task_data = {
            "task_id": task['task_id'],
            "question": task['question'],
            "category": task.get('category', 'unknown'),
            "model_responses": {}
        }

        for model, resp_data in task.get('model_responses', {}).items():
            task_data['model_responses'][model] = {
                "response": resp_data.get('response', ''),
                "timestamp": resp_data.get('timestamp', ''),
                "error": resp_data.get('error', None)
            }

        phase2_responses['tasks'].append(task_data)

    with open(output_dir / '2_responses_phase2.json', 'w') as f:
        json.dump(phase2_responses, f, indent=2)

    model_count = len(phase2_data.get('metadata', {}).get('models', []))
    print(f"  ✅ Phase 2: {len(phase2_responses['tasks'])} tasks × {model_count} models → 2_responses_phase2.json")

    # Phase 3: Uses 'questions' key
    with open(repo_root / 'results/phase3_responses.json', 'r') as f:
        phase3_data = json.load(f)

    phase3_responses = {
        "metadata": phase3_data.get('metadata', {}),
        "questions": []
    }

    for q in phase3_data['questions']:
        q_data = {
            "question_id": q['question_id'],
            "question": q['question'],
            "category": q.get('category', 'unknown'),
            "model_responses": {}
        }

        for model, resp_data in q.get('model_responses', {}).items():
            q_data['model_responses'][model] = {
                "response": resp_data.get('response', ''),
                "timestamp": resp_data.get('timestamp', ''),
                "error": resp_data.get('error', None)
            }

        phase3_responses['questions'].append(q_data)

    with open(output_dir / '2_responses_phase3.json', 'w') as f:
        json.dump(phase3_responses, f, indent=2)

    model_count = len(phase3_data.get('metadata', {}).get('models', []))
    print(f"  ✅ Phase 3: {len(phase3_responses['questions'])} questions × {model_count} models → 2_responses_phase3.json")

    # ============================================
    # TIER 3: EVALUATIONS (Full Dataset)
    # ============================================
    print("\n📊 TIER 3: Creating Evaluation datasets (full data with scores)...\n")

    # Just copy the full response files (they already contain evaluations)
    for phase_num, phase_file in [
        (1, 'phase1_responses.json'),
        (2, 'phase2_responses.json'),
        (3, 'phase3_responses.json')
    ]:
        with open(repo_root / 'results' / phase_file, 'r') as f:
            eval_data = json.load(f)

        with open(output_dir / f'3_evaluations_phase{phase_num}.json', 'w') as f:
            json.dump(eval_data, f, indent=2)

        # Count questions/tasks
        if 'questions' in eval_data:
            count = len(eval_data['questions'])
        elif 'tasks' in eval_data:
            count = len(eval_data['tasks'])
        else:
            count = 0

        model_count = len(eval_data.get('metadata', {}).get('models', []))
        total_responses = count * model_count

        print(f"  ✅ Phase {phase_num}: {count} × {model_count} = {total_responses} evaluated responses → 3_evaluations_phase{phase_num}.json")

    # ============================================
    # SUMMARY
    # ============================================
    print("\n" + "=" * 70)
    print("  ✅ HuggingFace Dataset Structure Created Successfully!")
    print("=" * 70)
    print(f"\n📂 Output directory: {output_dir}\n")

    print("📦 Dataset Tiers:\n")
    print("  🔹 TIER 1 - Questions Only (Input Data):")
    print("      For researchers who want to evaluate their own models")
    print("      • 1_questions_phase1.json (100 legal Q&A)")
    print("      • 1_questions_phase2.json (39 contract tasks)")
    print("      • 1_questions_phase3.json (24 FalseReject)")
    print()
    print("  🔹 TIER 2 - Responses (Questions + AI Answers):")
    print("      Model outputs without evaluation scores")
    print("      • 2_responses_phase1.json (12 models × 100 questions)")
    print("      • 2_responses_phase2.json (12 models × 39 tasks)")
    print("      • 2_responses_phase3.json (12 models × 24 questions)")
    print()
    print("  🔹 TIER 3 - Evaluations (Full Dataset with Scores):")
    print("      Complete dataset with quality scores + refusal labels")
    print("      • 3_evaluations_phase1.json (scored responses)")
    print("      • 3_evaluations_phase2.json (scored responses)")
    print("      • 3_evaluations_phase3.json (scored + refusal labeled)")

    # Print file sizes
    print("\n📏 File Sizes:")
    total_size = 0
    for file in sorted(output_dir.glob('*.json')):
        size_kb = file.stat().st_size / 1024
        total_size += size_kb
        tier = file.name[0]
        tier_name = {"1": "Questions", "2": "Responses", "3": "Evaluations"}.get(tier, "Unknown")
        print(f"  • {file.name:<32} {size_kb:>8.1f} KB  ({tier_name})")

    print(f"\n  📊 Total: {total_size:>8.1f} KB ({total_size/1024:.2f} MB)")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
