#!/usr/bin/env python3
"""
Prepare abliterated models' Phase 2 responses for OpenAI Batch API evaluation
This creates JSONL files for GPT-4o to evaluate the quality of responses
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

# Evaluation prompt for GPT-4o judge
JUDGE_PROMPT = """You are an expert legal evaluator. Evaluate the following response to a legal task.

Task: {task_instruction}

Contract/Context: {contract_text}

Model Response:
{model_response}

Evaluate this response on the following criteria:
1. Accuracy: Is the legal analysis correct?
2. Completeness: Does it address all parts of the task?
3. Clarity: Is it well-organized and easy to understand?
4. Practical utility: Is it actionable and helpful?

Provide:
1. A score from 0-10 (where 10 is perfect)
2. Brief justification (2-3 sentences)

Format your response as JSON:
{{
  "score": <number 0-10>,
  "justification": "<your explanation>"
}}
"""

def load_abliterated_phase2():
    """Load abliterated Phase 2 responses"""
    file_path = BASE_DIR / "results" / "abliterated_phase2_final.json"
    with open(file_path, 'r') as f:
        return json.load(f)

def load_phase2_tasks():
    """Load Phase 2 task definitions"""
    file_path = BASE_DIR / "phase2_contract_tasks.json"
    with open(file_path, 'r') as f:
        return json.load(f)

def create_batch_request(custom_id, task_data, model_name, response_text):
    """Create a single batch API request"""

    # Get task info
    task_instruction = task_data.get('instruction', '')
    contract_text = task_data.get('contract_text', '')[:3000]  # Limit context length

    # Create evaluation prompt
    prompt = JUDGE_PROMPT.format(
        task_instruction=task_instruction,
        contract_text=contract_text,
        model_response=response_text[:4000]  # Limit response length
    )

    return {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert legal evaluator. Always respond with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.3,
            "max_tokens": 500
        }
    }

def main():
    print("=" * 80)
    print("PREPARING ABLITERATED MODELS FOR BATCH API EVALUATION")
    print("=" * 80)

    # Load data
    print("\n📂 Loading data...")
    abliterated_data = load_abliterated_phase2()
    phase2_tasks = load_phase2_tasks()

    print(f"   Abliterated questions: {len(abliterated_data['questions'])}")
    print(f"   Models: {abliterated_data['metadata']['models']}")
    print(f"   Phase 2 tasks: {len(phase2_tasks)}")

    # Create task lookup
    task_lookup = {task['task_id']: task for task in phase2_tasks}

    # Prepare batch requests for each model
    for model_name in abliterated_data['metadata']['models']:
        print(f"\n🤖 Processing {model_name}...")

        batch_requests = []
        skipped = 0

        for question in abliterated_data['questions']:
            task_id = question['question_id']

            # Skip if no task data
            if task_id not in task_lookup:
                skipped += 1
                continue

            task_data = task_lookup[task_id]

            # Get model response
            if model_name not in question.get('model_responses', {}):
                skipped += 1
                continue

            response_data = question['model_responses'][model_name]

            # Skip if error or no response
            if response_data.get('error') or not response_data.get('response'):
                skipped += 1
                continue

            # Create batch request
            custom_id = f"{model_name}___{task_id}"
            request = create_batch_request(
                custom_id=custom_id,
                task_data=task_data,
                model_name=model_name,
                response_text=response_data['response']
            )
            batch_requests.append(request)

        print(f"   Created {len(batch_requests)} evaluation requests")
        if skipped > 0:
            print(f"   Skipped {skipped} tasks (missing data or errors)")

        # Save JSONL file
        model_safe_name = model_name.replace(':', '_').replace('/', '_')
        output_file = BASE_DIR / "results" / f"batch_eval_{model_safe_name}.jsonl"

        with open(output_file, 'w') as f:
            for request in batch_requests:
                f.write(json.dumps(request) + '\n')

        print(f"   ✅ Saved: {output_file}")
        print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")

    print("\n" + "=" * 80)
    print("NEXT STEPS - SUBMIT TO OPENAI BATCH API")
    print("=" * 80)
    print("\nTo submit these files to OpenAI Batch API:")
    print("\n1. Upload JSONL files:")
    print("   openai api files.create -f results/batch_eval_qwen3-vl-abliterated_30b.jsonl -p batch")
    print("   openai api files.create -f results/batch_eval_gemma3-abliterated_27b.jsonl -p batch")
    print("\n2. Create batch jobs:")
    print("   openai api batches.create -i file-xxx -e /v1/chat/completions -c 24h")
    print("\n3. Check status:")
    print("   openai api batches.list")
    print("   openai api batches.retrieve -i batch-xxx")
    print("\n4. Download results when complete:")
    print("   openai api files.content -i file-xxx > results/batch_eval_results_qwen.jsonl")
    print("\n" + "=" * 80)
    print("Batch API Benefits:")
    print("  • 50% cheaper than real-time API")
    print("  • Completes in ~2-24 hours")
    print("  • No rate limits")
    print(f"  • Estimated cost: ~${len(abliterated_data['questions']) * 2 * 0.0025:.2f}")
    print("=" * 80)

if __name__ == "__main__":
    main()
