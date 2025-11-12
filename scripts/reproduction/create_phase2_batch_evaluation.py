#!/usr/bin/env python3
"""
Create Phase 2 (Contracts) batch evaluation request for ALL 12 models
This will create a JSONL file to submit to OpenAI Batch API
"""

import json
from pathlib import Path

# Load Phase 2 data
with open('results/phase2_final_with_abliterated_scored.json', 'r') as f:
    phase2_data = json.load(f)

print("="*80)
print("CREATING PHASE 2 BATCH EVALUATION REQUEST")
print("="*80)

# Group tasks by task_id and model
tasks_by_id = {}
for task in phase2_data['tasks']:
    task_id = task['task_id']
    model = task['model']

    if task_id not in tasks_by_id:
        tasks_by_id[task_id] = {}

    tasks_by_id[task_id][model] = task

print(f"\n📊 Data Summary:")
print(f"   Unique tasks: {len(tasks_by_id)}")
print(f"   Models: {len(set(t['model'] for t in phase2_data['tasks']))}")

# Get all models (normalize names for consistency with Phase 1)
model_mapping = {
    'claude-sonnet-4.5': 'anthropic/claude-sonnet-4.5',
    'deepseek-chat-v3': 'deepseek/deepseek-chat-v3-0324',
    'gemini-2.5-flash': 'google/gemini-2.5-flash',
    'glm-4.6': 'z-ai/glm-4.6',
    'gpt-5': 'openai/gpt-5',
    'gpt-oss-120b': 'openai/gpt-oss-120b',
    'grok-4': 'x-ai/grok-4',
    'mistral-large': 'mistralai/mistral-large',
    'o3-mini': 'openai/o3-mini',
    'qwen-2.5-72b': 'qwen/qwen-2.5-72b-instruct'
}

# Also add abliterated models (though they already have evaluations)
all_models = list(model_mapping.values()) + [
    'gemma3-abliterated:27b',
    'qwen3-vl-abliterated:30b'
]

print(f"\n📋 ALL 12 models to evaluate:")
for i, model in enumerate(all_models, 1):
    print(f"   {i}. {model}")

# Evaluation prompt template
EVALUATION_PROMPT = """You are evaluating the quality of a contract drafting response.

Task: {task_title}

Response to evaluate:
{response}

Please evaluate this response on the following criteria:

1. **Completeness**: Does the response fully address the task requirements?
2. **Accuracy**: Is the legal content correct and appropriate?
3. **Professionalism**: Is it well-formatted and professional?
4. **Actionability**: Can this be used directly or with minimal modifications?

Provide your evaluation in JSON format:
{{
  "score": <integer 0-10>,
  "justification": "<detailed explanation of the score>"
}}

Score guidelines:
- 9-10: Excellent, ready to use with minimal edits
- 7-8: Good quality, needs minor improvements
- 5-6: Acceptable but needs significant work
- 3-4: Poor quality, major issues
- 0-2: Unacceptable, fails to meet requirements
"""

# Create batch requests
batch_requests = []
request_id = 0

for task_id in sorted(tasks_by_id.keys()):
    for model_short, model_full in model_mapping.items():
        if model_short in tasks_by_id[task_id]:
            task_data = tasks_by_id[task_id][model_short]
            response = task_data.get('response', '')

            # Skip if no response or error
            if not response or task_data.get('error'):
                continue

            # Create evaluation request
            custom_id = f"phase2_contract_{task_id}_{model_full}_{request_id}"

            batch_request = {
                "custom_id": custom_id,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o-2024-08-06",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert legal evaluator assessing the quality of contract drafting responses."
                        },
                        {
                            "role": "user",
                            "content": EVALUATION_PROMPT.format(
                                task_title=task_data.get('task_title', 'Contract task'),
                                response=response[:8000]  # Truncate if too long
                            )
                        }
                    ],
                    "max_tokens": 500,
                    "temperature": 0.3,
                    "response_format": {"type": "json_object"}
                }
            }

            batch_requests.append(batch_request)
            request_id += 1

# Note: Abliterated models already have Phase 2 evaluations, so we skip them
print(f"\n📝 Note: Abliterated models already evaluated (skipping)")

print(f"\n✅ Created {len(batch_requests)} evaluation requests")
print(f"   Expected: ~{len(tasks_by_id)} tasks × 12 models = {len(tasks_by_id) * 12}")

# Count by model
from collections import Counter
model_counts = Counter()
for req in batch_requests:
    custom_id = req['custom_id']
    # Extract model from custom_id
    parts = custom_id.split('_')
    model_part = '_'.join(parts[3:-1])  # Everything between task_id and request_id
    model_counts[model_part] += 1

print(f"\n📊 Requests by model:")
for model, count in sorted(model_counts.items()):
    print(f"   {model}: {count} evaluations")

# Save to JSONL file
output_file = Path('batch_evaluation_jobs/phase2_quality_evaluation_ALL_MODELS.jsonl')
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w') as f:
    for req in batch_requests:
        f.write(json.dumps(req) + '\n')

print(f"\n💾 Saved batch file to: {output_file}")
print(f"   Total size: {output_file.stat().st_size / 1024:.1f} KB")
print(f"   Total requests: {len(batch_requests)}")

print("\n" + "="*80)
print("✅ BATCH FILE CREATED!")
print("="*80)
print("\nNext steps:")
print("1. Upload this file to OpenAI")
print("2. Submit batch job")
print("3. Wait for completion (~24 hours)")
print("4. Download results and merge into comprehensive analysis")

print(f"\n📋 Estimated cost:")
print(f"   {len(batch_requests)} requests × ~500 tokens × $0.0025/1K = ~${len(batch_requests) * 0.5 * 0.0025:.2f}")
print(f"   (50% batch discount already applied)")
