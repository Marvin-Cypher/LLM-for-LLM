#!/usr/bin/env python3
"""
Run the 24 FalseReject legal questions through all 10 models.
Reuses the same API approach as Phase 1.
"""

import csv
import json
import os
import time
from pathlib import Path
from datetime import datetime
import requests
from openai import OpenAI

# API Configuration (load from environment variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENAI_API_KEY or not OPENROUTER_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY and OPENROUTER_API_KEY environment variables")

# Model Configuration (EXACT same as Phase 1 - ALL via OpenRouter)
ALL_MODELS = [
    "anthropic/claude-sonnet-4.5",
    "openai/gpt-5",
    "openai/gpt-oss-120b",
    "google/gemini-2.5-flash",
    "x-ai/grok-4",
    "deepseek/deepseek-chat-v3-0324",
    "z-ai/glm-4.6",
    "openai/o3-mini",
    "mistralai/mistral-large",
    "qwen/qwen-2.5-72b-instruct"
]

def load_falsereject_questions(csv_file: Path) -> list:
    """Load the 24 FalseReject questions from CSV."""
    questions = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            questions.append({
                'question_id': f'falsereject_{i:02d}',
                'question': row['legal_question'],
                'category': 'falsereject_legal',
                'source': 'FalseReject_HuggingFace',
                'expected_behavior': 'answer',  # These should be answered, not refused
                'reference_response': row.get('legal_advice', '')
            })

    return questions

def call_openai_api(model: str, question: str) -> dict:
    """Call OpenAI API (for gpt-4o, gpt-5, o3-mini)."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        start_time = time.time()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        latency = time.time() - start_time

        return {
            'response': response.choices[0].message.content,
            'latency': latency,
            'error': None
        }

    except Exception as e:
        return {
            'response': '',
            'latency': 0,
            'error': str(e)
        }

def call_openrouter_api(model: str, question: str) -> dict:
    """Call OpenRouter API (for Claude, Gemini, Llama, Qwen, DeepSeek, GLM, Grok)."""
    try:
        start_time = time.time()
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": question}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            },
            timeout=120
        )
        latency = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            return {
                'response': data['choices'][0]['message']['content'],
                'latency': latency,
                'error': None
            }
        else:
            return {
                'response': '',
                'latency': latency,
                'error': f"HTTP {response.status_code}: {response.text}"
            }

    except Exception as e:
        return {
            'response': '',
            'latency': 0,
            'error': str(e)
        }

def run_benchmark(questions: list) -> dict:
    """Run all questions through all models."""

    results = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'total_questions': len(questions),
            'models': ALL_MODELS,
            'source': 'FalseReject_HuggingFace_AmazonScience',
            'description': 'FalseReject legal questions - legitimate queries that appear adversarial'
        },
        'results': []
    }

    total_calls = len(questions) * len(ALL_MODELS)
    completed = 0

    print(f"🚀 FalseReject Benchmark")
    print("=" * 70)
    print(f"📋 Questions: {len(questions)}")
    print(f"🤖 Models: {len(ALL_MODELS)}")
    print(f"📊 Total API calls: {total_calls}")
    print(f"🔗 All models via OpenRouter API")
    print()

    for q_idx, question_data in enumerate(questions, 1):
        question_id = question_data['question_id']
        question = question_data['question']

        print(f"\n📄 Question {q_idx}/{len(questions)}: {question_id}")
        print(f"   {question[:100]}...")
        print()

        model_responses = {}

        # Test each model (ALL via OpenRouter)
        for model in ALL_MODELS:
            completed += 1
            model_short = model.split('/')[-1]

            print(f"   [{completed}/{total_calls}] 🟢 OpenRouter {model_short}...", end=" ", flush=True)
            result = call_openrouter_api(model, question)

            model_responses[model] = result

            # Print result
            if result['error']:
                print(f"❌ {result['error'][:50]}")
            else:
                response_len = len(result['response'])
                print(f"✅ ({result['latency']:.1f}s, {response_len} chars)")

            # Rate limiting
            time.sleep(1)

        # Add to results
        results['results'].append({
            **question_data,
            'model_responses': model_responses
        })

        # Save progress after each question
        output_file = Path('results/falsereject_benchmark.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        success_rate = sum(1 for m in model_responses.values() if not m['error']) / len(ALL_MODELS) * 100
        print(f"\n   📊 Progress: {completed}/{total_calls} ({success_rate:.1f}% success for this question)")

    return results

def main():
    # Load FalseReject questions
    csv_file = Path('/Users/marvin/Downloads/filtered-legal-consulting-advice.csv')

    if not csv_file.exists():
        print(f"❌ FalseReject CSV not found: {csv_file}")
        return

    print("📂 Loading FalseReject questions...")
    questions = load_falsereject_questions(csv_file)
    print(f"✅ Loaded {len(questions)} questions\n")

    # Run benchmark
    results = run_benchmark(questions)

    # Final save
    output_file = Path('results/falsereject_benchmark.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("✨ FalseReject benchmark complete!")
    print(f"📁 Results saved: {output_file}")
    print(f"\nNext step: Merge with Phase 1 results:")
    print(f"   python3 scripts/merge_phase1_with_falsereject.py")

if __name__ == "__main__":
    main()
