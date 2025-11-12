#!/usr/bin/env python3
"""
Download batch evaluation results for ALL models from OpenAI
These batches contain quality scores (actionability, appropriateness) for all 12 models
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Batch IDs for ALL models evaluations
BATCH_CONFIGS = {
    "batch_690da40b344481909717c2216e38edad": {
        "name": "appropriateness_all_models",
        "dimension": "appropriateness",
        "output_file": "results/batch_appropriateness_all_models_output.jsonl",
        "error_file": "results/batch_appropriateness_all_models_error.jsonl"
    },
    "batch_690da41208cc8190b95a6fd9c3ffd5e0": {
        "name": "actionability_all_models",
        "dimension": "actionability",
        "output_file": "results/batch_actionability_all_models_output.jsonl",
        "error_file": "results/batch_actionability_all_models_error.jsonl"
    },
    "batch_690da414dfd88190b917d9d5f7cf5a43": {
        "name": "falsereject_all_models",
        "dimension": "falsereject_evaluation",
        "output_file": "results/batch_falsereject_all_models_output.jsonl",
        "error_file": "results/batch_falsereject_all_models_error.jsonl"
    }
}

def download_batch_results(batch_id, config):
    """Download batch results from OpenAI"""
    print(f"\n{'='*80}")
    print(f"Processing: {config['name']}")
    print(f"Batch ID: {batch_id}")
    print(f"{'='*80}")

    try:
        # Get batch info
        batch = client.batches.retrieve(batch_id)
        print(f"Status: {batch.status}")
        print(f"Created: {batch.created_at}")
        print(f"Request counts: {batch.request_counts}")

        if batch.status != "completed":
            print(f"⚠️  Batch not completed yet. Status: {batch.status}")
            return False

        # Download output file
        if batch.output_file_id:
            print(f"\n📥 Downloading output file: {batch.output_file_id}")
            output_content = client.files.content(batch.output_file_id)

            with open(config['output_file'], 'wb') as f:
                f.write(output_content.read())

            print(f"✅ Saved to: {config['output_file']}")

            # Count lines
            with open(config['output_file'], 'r') as f:
                line_count = sum(1 for _ in f)
            print(f"   Total evaluations: {line_count}")

        # Download error file if exists
        if batch.error_file_id:
            print(f"\n⚠️  Downloading error file: {batch.error_file_id}")
            error_content = client.files.content(batch.error_file_id)

            with open(config['error_file'], 'wb') as f:
                f.write(error_content.read())

            print(f"   Saved to: {config['error_file']}")

            # Count errors
            with open(config['error_file'], 'r') as f:
                error_count = sum(1 for _ in f)
            print(f"   Total errors: {error_count}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def analyze_downloaded_data(config):
    """Quick analysis of downloaded data"""
    print(f"\n📊 Analyzing {config['name']}...")

    try:
        with open(config['output_file'], 'r') as f:
            lines = f.readlines()

        # Sample first evaluation
        first_eval = json.loads(lines[0])
        print(f"\nSample evaluation structure:")
        print(f"  Keys: {list(first_eval.keys())}")

        if 'response' in first_eval:
            resp = first_eval['response']
            if 'body' in resp:
                body = resp['body']
                if 'choices' in body:
                    content = body['choices'][0]['message']['content']
                    print(f"  Sample content (first 200 chars):")
                    print(f"  {content[:200]}...")

        # Count by model (if custom_id contains model name)
        models_found = set()
        for line in lines:
            data = json.loads(line)
            custom_id = data.get('custom_id', '')
            # Extract model from custom_id (format may vary)
            if '_model_' in custom_id:
                model = custom_id.split('_model_')[1].split('_')[0]
                models_found.add(model)

        print(f"\n  Models found in evaluations: {len(models_found)}")
        if models_found:
            print(f"  Models: {sorted(models_found)}")

    except Exception as e:
        print(f"  Error analyzing: {e}")

def main():
    print("="*80)
    print("DOWNLOADING ALL MODELS BATCH EVALUATIONS")
    print("="*80)
    print("\nThese batches contain GPT-4o evaluation scores for ALL 12 models")
    print("on Phase 1 (actionability, appropriateness) and FalseReject benchmarks.\n")

    # Download all batches
    success_count = 0
    for batch_id, config in BATCH_CONFIGS.items():
        if download_batch_results(batch_id, config):
            success_count += 1
            analyze_downloaded_data(config)

    print(f"\n{'='*80}")
    print(f"✅ Successfully downloaded {success_count}/{len(BATCH_CONFIGS)} batches")
    print(f"{'='*80}")

    print("\n📋 Next Steps:")
    print("1. Merge these evaluations into phase1_final_with_abliterated_scored.json")
    print("2. Update falsereject_analysis_with_abliterated.json with evaluation scores")
    print("3. Generate comprehensive figures with ALL models quality data")
    print("4. Update paper figures to show complete analysis")

if __name__ == '__main__':
    main()
