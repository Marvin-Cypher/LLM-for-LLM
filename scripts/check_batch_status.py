#!/usr/bin/env python3
"""
Check OpenAI Batch Job Status

This script checks the status of uploaded batch jobs.

Usage:
    python3 scripts/check_batch_status.py
"""

import os
import json
from pathlib import Path
from openai import OpenAI
from datetime import datetime

# API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY environment variable")

def check_batch_status():
    """Check status of all batch jobs"""

    print("=" * 80)
    print("🔍 Check Batch Job Status")
    print("=" * 80)

    # Load batch IDs
    batch_ids_file = Path('batch_evaluation_jobs/batch_ids.json')
    if not batch_ids_file.exists():
        print(f"\n❌ Batch IDs file not found: {batch_ids_file}")
        print("   Run upload_batch_jobs.py first!")
        return

    with open(batch_ids_file, 'r') as f:
        batch_info = json.load(f)

    # Initialize OpenAI client
    client = OpenAI(api_key=OPENAI_API_KEY)

    print(f"\n📋 Checking {len(batch_info)} batch jobs...\n")

    updated_info = []
    all_completed = True

    for i, info in enumerate(batch_info, 1):
        batch_id = info['batch_id']
        filename = info['filename']

        print(f"[{i}/{len(batch_info)}] {filename}")
        print(f"   Batch ID: {batch_id}")

        try:
            # Get batch status
            batch = client.batches.retrieve(batch_id)

            status = batch.status
            request_counts = batch.request_counts

            # Update info
            info['status'] = status
            info['request_counts'] = {
                'total': request_counts.total,
                'completed': request_counts.completed,
                'failed': request_counts.failed
            }
            if batch.output_file_id:
                info['output_file_id'] = batch.output_file_id
            if batch.error_file_id:
                info['error_file_id'] = batch.error_file_id

            # Display status
            if status == 'completed':
                print(f"   ✅ Status: {status}")
                print(f"   📊 Completed: {request_counts.completed}/{request_counts.total}")
                if request_counts.failed > 0:
                    print(f"   ⚠️  Failed: {request_counts.failed}")
                print(f"   📄 Output file: {batch.output_file_id}")
            elif status == 'in_progress' or status == 'validating':
                print(f"   ⏳ Status: {status}")
                print(f"   📊 Progress: {request_counts.completed}/{request_counts.total}")
                all_completed = False
            elif status == 'failed':
                print(f"   ❌ Status: {status}")
                all_completed = False
            else:
                print(f"   📊 Status: {status}")
                all_completed = False

            updated_info.append(info)

        except Exception as e:
            print(f"   ❌ Error checking status: {str(e)}")
            updated_info.append(info)
            all_completed = False

        print()

    # Save updated info
    with open(batch_ids_file, 'w') as f:
        json.dump(updated_info, f, indent=2)

    print("=" * 80)
    if all_completed:
        print("✅ ALL BATCH JOBS COMPLETED!")
        print("\nNext step: Download results")
        print("   python3 scripts/download_batch_results.py")
    else:
        print("⏳ BATCH JOBS STILL PROCESSING")
        print("\nCheck again later. Most batches complete within 24 hours.")
        print("   python3 scripts/check_batch_status.py")
    print("=" * 80)


if __name__ == "__main__":
    check_batch_status()
