#!/usr/bin/env python3
"""
Upload Legal LLM Benchmark Dataset to HuggingFace Hub

This script uploads all 3 tiers of datasets:
- TIER 1: Questions only (input data)
- TIER 2: Responses (questions + AI answers)
- TIER 3: Evaluations (questions + answers + scores)

Run after setting HF_TOKEN environment variable:
export HF_TOKEN=your_token_here
"""

import json
import os
from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_file

def main():
    # Setup
    repo_id = "marvintong/legal-llm-benchmark"
    dataset_dir = Path('/Users/marvin/legal-llm-benchmark/huggingface_datasets')

    # Get HF token from environment or parameter
    hf_token = os.environ.get('HF_TOKEN', 'YOUR_HF_TOKEN_HERE')

    print("=" * 70)
    print("  📦 LEGAL LLM BENCHMARK - HuggingFace Upload")
    print("=" * 70)
    print(f"\n📍 Repository: {repo_id}")
    print(f"📁 Source directory: {dataset_dir}\n")

    # Initialize HF API
    api = HfApi(token=hf_token)

    # Create or update repository
    print("🔧 Step 1: Creating/updating repository...")
    try:
        create_repo(
            repo_id=repo_id,
            repo_type="dataset",
            exist_ok=True,
            token=hf_token
        )
        print(f"  ✅ Repository {repo_id} ready\n")
    except Exception as e:
        print(f"  ⚠️  Repository may already exist: {e}\n")

    # Upload all dataset files
    print("📤 Step 2: Uploading dataset files...")

    files_to_upload = [
        # TIER 1: Questions
        ("1_questions_phase1.json", "TIER 1 - Phase 1 Questions"),
        ("1_questions_phase2.json", "TIER 1 - Phase 2 Questions"),
        ("1_questions_phase3.json", "TIER 1 - Phase 3 Questions"),

        # TIER 2: Responses
        ("2_responses_phase1.json", "TIER 2 - Phase 1 Responses"),
        ("2_responses_phase2.json", "TIER 2 - Phase 2 Responses"),
        ("2_responses_phase3.json", "TIER 2 - Phase 3 Responses"),

        # TIER 3: Evaluations
        ("3_evaluations_phase1.json", "TIER 3 - Phase 1 Evaluations"),
        ("3_evaluations_phase2.json", "TIER 3 - Phase 2 Evaluations"),
        ("3_evaluations_phase3.json", "TIER 3 - Phase 3 Evaluations"),
    ]

    uploaded_count = 0
    for filename, description in files_to_upload:
        file_path = dataset_dir / filename

        if not file_path.exists():
            print(f"  ⚠️  Skipping {filename} (file not found)")
            continue

        try:
            print(f"\n  📤 Uploading {filename}...")
            print(f"     {description}")

            api.upload_file(
                path_or_fileobj=str(file_path),
                path_in_repo=filename,
                repo_id=repo_id,
                repo_type="dataset",
                token=hf_token
            )

            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"     ✅ Uploaded ({size_mb:.2f} MB)")
            uploaded_count += 1

        except Exception as e:
            print(f"     ❌ Failed: {e}")

    # Upload README (dataset card)
    print("\n📄 Step 3: Uploading dataset card (README.md)...")
    readme_path = dataset_dir / "README.md"

    if readme_path.exists():
        try:
            api.upload_file(
                path_or_fileobj=str(readme_path),
                path_in_repo="README.md",
                repo_id=repo_id,
                repo_type="dataset",
                token=hf_token
            )
            print("  ✅ README.md uploaded\n")
        except Exception as e:
            print(f"  ❌ Failed to upload README: {e}\n")
    else:
        print("  ⚠️  README.md not found, skipping\n")

    # Summary
    print("=" * 70)
    print("  ✅ UPLOAD COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"  Files uploaded: {uploaded_count}/9 dataset files")
    print(f"  README: {'✅ Yes' if readme_path.exists() else '❌ No'}")
    print(f"\n🔗 View dataset at:")
    print(f"  https://huggingface.co/datasets/{repo_id}")
    print()
    print("📦 Dataset structure:")
    print("  🔹 TIER 1 - Questions Only:")
    print("      • 1_questions_phase1.json (100 Q&A)")
    print("      • 1_questions_phase2.json (39 contracts)")
    print("      • 1_questions_phase3.json (24 FalseReject)")
    print()
    print("  🔹 TIER 2 - Responses:")
    print("      • 2_responses_phase1.json (12 models × 100)")
    print("      • 2_responses_phase2.json (12 models × 39)")
    print("      • 2_responses_phase3.json (10 models × 24)")
    print()
    print("  🔹 TIER 3 - Evaluations (Full Dataset):")
    print("      • 3_evaluations_phase1.json (with scores)")
    print("      • 3_evaluations_phase2.json (with scores)")
    print("      • 3_evaluations_phase3.json (with scores + refusal labels)")
    print()

if __name__ == "__main__":
    main()
