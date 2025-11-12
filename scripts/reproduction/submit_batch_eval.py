#!/usr/bin/env python3
"""
Submit abliterated models to OpenAI Batch API for evaluation
"""

import os
from pathlib import Path
from openai import OpenAI

BASE_DIR = Path(__file__).parent.parent

def main():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print("=" * 80)
    print("SUBMITTING ABLITERATED MODELS TO OPENAI BATCH API")
    print("=" * 80)

    batch_files = [
        "batch_eval_qwen3-vl-abliterated_30b.jsonl",
        "batch_eval_gemma3-abliterated_27b.jsonl"
    ]

    batch_ids = []

    for batch_file in batch_files:
        file_path = BASE_DIR / "results" / batch_file

        print(f"\n📤 Uploading {batch_file}...")

        # Upload file
        with open(file_path, "rb") as f:
            batch_input_file = client.files.create(
                file=f,
                purpose="batch"
            )

        print(f"   ✅ File uploaded: {batch_input_file.id}")

        # Create batch job
        print(f"   🚀 Creating batch job...")
        batch_job = client.batches.create(
            input_file_id=batch_input_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
                "description": f"Evaluate {batch_file.replace('batch_eval_', '').replace('.jsonl', '')} Phase 2 responses"
            }
        )

        print(f"   ✅ Batch created: {batch_job.id}")
        print(f"   Status: {batch_job.status}")
        print(f"   Total requests: {batch_job.request_counts.total if hasattr(batch_job, 'request_counts') else 'unknown'}")

        batch_ids.append({
            'model': batch_file.replace('batch_eval_', '').replace('.jsonl', ''),
            'file_id': batch_input_file.id,
            'batch_id': batch_job.id
        })

    print("\n" + "=" * 80)
    print("✅ ALL BATCHES SUBMITTED!")
    print("=" * 80)

    print("\nBatch Job IDs:")
    for info in batch_ids:
        print(f"  • {info['model']}: {info['batch_id']}")

    print("\nTo check status:")
    for info in batch_ids:
        print(f"  openai api batches.retrieve -i {info['batch_id']}")

    print("\nTo list all batches:")
    print("  openai api batches.list")

    print("\nBatches typically complete in 2-24 hours.")
    print("You'll receive an email when complete, or check status with the commands above.")
    print("=" * 80)

if __name__ == "__main__":
    main()
