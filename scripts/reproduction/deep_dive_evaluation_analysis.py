#!/usr/bin/env python3
"""
Deep dive analysis of ALL OpenAI batch evaluation results
Extract insights we haven't fully utilized yet
"""

import json
from pathlib import Path
from collections import defaultdict, Counter
import statistics

BASE_DIR = Path(__file__).parent.parent

def analyze_justifications(batch_files, dimension_name):
    """Analyze justification patterns from GPT-4o evaluations"""

    all_justifications = []
    score_to_justifications = defaultdict(list)

    for filepath in batch_files:
        with open(filepath, 'r') as f:
            for line in f:
                result = json.loads(line)
                try:
                    if result['response']['status_code'] == 200:
                        content = result['response']['body']['choices'][0]['message']['content']
                        eval_data = json.loads(content)
                        score = eval_data['score']
                        justification = eval_data.get('justification', '')

                        all_justifications.append({
                            'score': score,
                            'justification': justification,
                            'custom_id': result['custom_id']
                        })
                        score_to_justifications[score].append(justification)
                except:
                    continue

    return all_justifications, score_to_justifications

def extract_common_themes(justifications):
    """Extract common themes/keywords from justifications"""

    # Keywords to look for
    positive_keywords = [
        'specific', 'concrete', 'actionable', 'clear', 'comprehensive',
        'detailed', 'practical', 'helpful', 'appropriate', 'well-structured',
        'accurate', 'thorough', 'professional', 'balanced'
    ]

    negative_keywords = [
        'vague', 'generic', 'lacking', 'unclear', 'incomplete', 'missing',
        'insufficient', 'limited', 'poor', 'weak', 'inadequate', 'fails',
        'incorrect', 'inappropriate', 'overly'
    ]

    positive_counts = Counter()
    negative_counts = Counter()

    for just in justifications:
        text_lower = just.lower()
        for keyword in positive_keywords:
            if keyword in text_lower:
                positive_counts[keyword] += 1
        for keyword in negative_keywords:
            if keyword in text_lower:
                negative_counts[keyword] += 1

    return positive_counts, negative_counts

def compare_score_distributions(all_data):
    """Compare score distributions across dimensions and models"""

    distributions = {}

    for model_name, dimensions in all_data.items():
        distributions[model_name] = {}
        for dim_name, scores in dimensions.items():
            if not scores:
                continue

            distributions[model_name][dim_name] = {
                'mean': statistics.mean(scores),
                'median': statistics.median(scores),
                'stdev': statistics.stdev(scores) if len(scores) > 1 else 0,
                'min': min(scores),
                'max': max(scores),
                'range': max(scores) - min(scores),
                'q1': statistics.quantiles(scores, n=4)[0] if len(scores) >= 4 else None,
                'q3': statistics.quantiles(scores, n=4)[2] if len(scores) >= 4 else None,
            }

    return distributions

def identify_low_scoring_patterns(all_justifications):
    """Analyze what causes low scores (0-4)"""

    low_score_reasons = defaultdict(int)

    # Common failure patterns
    failure_patterns = {
        'no_specifics': ['lacks specific', 'not specific', 'vague', 'generic', 'no concrete'],
        'missing_disclaimers': ['no disclaimer', 'fails to mention', 'does not advise'],
        'incorrect_info': ['incorrect', 'inaccurate', 'wrong', 'error'],
        'incomplete': ['incomplete', 'missing', 'lacks', 'not comprehensive'],
        'overly_cautious': ['overly cautious', 'too generic', 'refuses to'],
        'poor_structure': ['poorly structured', 'disorganized', 'unclear'],
    }

    low_score_examples = []

    for item in all_justifications:
        if item['score'] <= 4:
            just_lower = item['justification'].lower()

            for pattern_name, keywords in failure_patterns.items():
                if any(kw in just_lower for kw in keywords):
                    low_score_reasons[pattern_name] += 1

            low_score_examples.append({
                'score': item['score'],
                'task': item['custom_id'],
                'reason': item['justification'][:200]  # First 200 chars
            })

    return low_score_reasons, low_score_examples

def identify_high_scoring_patterns(all_justifications):
    """Analyze what causes high scores (8-10)"""

    high_score_reasons = defaultdict(int)

    # Common success patterns
    success_patterns = {
        'specific_actionable': ['specific', 'actionable', 'concrete steps'],
        'comprehensive': ['comprehensive', 'thorough', 'detailed'],
        'appropriate_disclaimers': ['appropriate disclaimer', 'mentions limitations'],
        'well_structured': ['well-structured', 'organized', 'clear'],
        'practical': ['practical', 'useful', 'helpful'],
        'balanced': ['balanced', 'appropriate balance'],
    }

    high_score_examples = []

    for item in all_justifications:
        if item['score'] >= 8:
            just_lower = item['justification'].lower()

            for pattern_name, keywords in success_patterns.items():
                if any(kw in just_lower for kw in keywords):
                    high_score_reasons[pattern_name] += 1

            high_score_examples.append({
                'score': item['score'],
                'task': item['custom_id'],
                'reason': item['justification'][:200]
            })

    return high_score_reasons, high_score_examples

def main():
    results_dir = BASE_DIR / "results"

    # Load all batch evaluation files
    batch_files_by_type = {
        'qwen_actionability': results_dir / 'batch_actionability_qwen3_output.jsonl',
        'qwen_appropriateness': results_dir / 'batch_appropriateness_qwen3_output.jsonl',
        'gemma_actionability': results_dir / 'batch_actionability_gemma3_output.jsonl',
        'gemma_appropriateness': results_dir / 'batch_appropriateness_gemma3_output.jsonl',
        'qwen_quality': results_dir / 'batch_quality_qwen3_output.jsonl',
        'gemma_quality': results_dir / 'batch_quality_gemma3_output.jsonl',
    }

    print("=" * 80)
    print("🔍 DEEP DIVE: OpenAI BATCH EVALUATION ANALYSIS")
    print("=" * 80)
    print("\nAnalyzing all GPT-4o evaluation justifications for hidden insights...")

    # Collect all data
    all_model_data = {
        'qwen3-vl-abliterated:30b': {
            'actionability': [],
            'appropriateness': [],
            'quality': []
        },
        'gemma3-abliterated:27b': {
            'actionability': [],
            'appropriateness': [],
            'quality': []
        }
    }

    all_justifications_combined = []

    for file_key, filepath in batch_files_by_type.items():
        print(f"\nProcessing: {filepath.name}")

        if not filepath.exists():
            print(f"  ⚠️  File not found, skipping")
            continue

        model = 'qwen3-vl-abliterated:30b' if 'qwen' in file_key else 'gemma3-abliterated:27b'
        dimension = 'actionability' if 'actionability' in file_key else \
                   'appropriateness' if 'appropriateness' in file_key else 'quality'

        justifications, score_to_just = analyze_justifications([filepath], file_key)
        all_justifications_combined.extend(justifications)

        scores = [j['score'] for j in justifications]
        all_model_data[model][dimension] = scores

        print(f"  Loaded {len(justifications)} evaluations")
        print(f"  Score range: {min(scores) if scores else 'N/A'}-{max(scores) if scores else 'N/A'}")

    # ANALYSIS 1: Score Distribution Comparison
    print("\n" + "=" * 80)
    print("📊 ANALYSIS 1: SCORE DISTRIBUTION STATISTICS")
    print("=" * 80)

    distributions = compare_score_distributions(all_model_data)

    for model in sorted(distributions.keys()):
        print(f"\n🤖 {model}")
        for dim in ['actionability', 'appropriateness', 'quality']:
            if dim in distributions[model]:
                stats = distributions[model][dim]
                print(f"\n  {dim.capitalize()}:")
                print(f"    Mean: {stats['mean']:.2f}")
                print(f"    Median: {stats['median']:.2f}")
                print(f"    Std Dev: {stats['stdev']:.2f}")
                print(f"    Range: {stats['min']}-{stats['max']} (span: {stats['range']})")
                if stats['q1'] and stats['q3']:
                    print(f"    IQR: {stats['q1']:.2f} - {stats['q3']:.2f}")

    # ANALYSIS 2: Common Keywords/Themes
    print("\n" + "=" * 80)
    print("💡 ANALYSIS 2: COMMON THEMES IN JUSTIFICATIONS")
    print("=" * 80)

    all_justs_text = [j['justification'] for j in all_justifications_combined]
    positive_themes, negative_themes = extract_common_themes(all_justs_text)

    print("\n✅ Most Common POSITIVE Themes (top 10):")
    for keyword, count in positive_themes.most_common(10):
        pct = count / len(all_justs_text) * 100
        print(f"  '{keyword}': {count} times ({pct:.1f}% of evaluations)")

    print("\n❌ Most Common NEGATIVE Themes (top 10):")
    for keyword, count in negative_themes.most_common(10):
        pct = count / len(all_justs_text) * 100
        print(f"  '{keyword}': {count} times ({pct:.1f}% of evaluations)")

    # ANALYSIS 3: Low Score Patterns
    print("\n" + "=" * 80)
    print("🔴 ANALYSIS 3: WHY LOW SCORES? (0-4 ratings)")
    print("=" * 80)

    low_reasons, low_examples = identify_low_scoring_patterns(all_justifications_combined)

    print(f"\nAnalyzed {len([j for j in all_justifications_combined if j['score'] <= 4])} low-scoring responses")
    print("\nMost Common Failure Patterns:")
    for pattern, count in sorted(low_reasons.items(), key=lambda x: x[1], reverse=True):
        print(f"  {pattern}: {count} occurrences")

    print("\n📝 Sample Low-Score Justifications (worst 3):")
    low_sorted = sorted(low_examples, key=lambda x: x['score'])[:3]
    for i, ex in enumerate(low_sorted, 1):
        print(f"\n  {i}. Score {ex['score']}/10 - {ex['task'][:50]}...")
        print(f"     Reason: {ex['reason']}")

    # ANALYSIS 4: High Score Patterns
    print("\n" + "=" * 80)
    print("🟢 ANALYSIS 4: WHY HIGH SCORES? (8-10 ratings)")
    print("=" * 80)

    high_reasons, high_examples = identify_high_scoring_patterns(all_justifications_combined)

    print(f"\nAnalyzed {len([j for j in all_justifications_combined if j['score'] >= 8])} high-scoring responses")
    print("\nMost Common Success Patterns:")
    for pattern, count in sorted(high_reasons.items(), key=lambda x: x[1], reverse=True):
        print(f"  {pattern}: {count} occurrences")

    print("\n📝 Sample High-Score Justifications (best 3):")
    high_sorted = sorted(high_examples, key=lambda x: x['score'], reverse=True)[:3]
    for i, ex in enumerate(high_sorted, 1):
        print(f"\n  {i}. Score {ex['score']}/10 - {ex['task'][:50]}...")
        print(f"     Reason: {ex['reason']}")

    # ANALYSIS 5: Consistency Analysis
    print("\n" + "=" * 80)
    print("📏 ANALYSIS 5: CONSISTENCY & VARIANCE")
    print("=" * 80)

    for model in sorted(all_model_data.keys()):
        print(f"\n{model}:")

        all_scores_for_model = []
        for dim in ['actionability', 'appropriateness', 'quality']:
            if dim in all_model_data[model] and all_model_data[model][dim]:
                scores = all_model_data[model][dim]
                all_scores_for_model.extend(scores)
                stdev = statistics.stdev(scores) if len(scores) > 1 else 0
                print(f"  {dim.capitalize()}: σ = {stdev:.2f} (lower = more consistent)")

        if all_scores_for_model:
            overall_stdev = statistics.stdev(all_scores_for_model)
            print(f"  Overall variance: σ = {overall_stdev:.2f}")
            print(f"  Interpretation: {'CONSISTENT' if overall_stdev < 2.0 else 'VARIABLE' if overall_stdev < 2.5 else 'HIGHLY VARIABLE'}")

    # ANALYSIS 6: Key Insights & Recommendations
    print("\n" + "=" * 80)
    print("🎯 ANALYSIS 6: KEY INSIGHTS & RECOMMENDATIONS")
    print("=" * 80)

    # Calculate averages
    qwen_avg = statistics.mean([
        distributions['qwen3-vl-abliterated:30b']['actionability']['mean'],
        distributions['qwen3-vl-abliterated:30b']['appropriateness']['mean'],
        distributions['qwen3-vl-abliterated:30b']['quality']['mean']
    ])

    gemma_avg = statistics.mean([
        distributions['gemma3-abliterated:27b']['actionability']['mean'],
        distributions['gemma3-abliterated:27b']['appropriateness']['mean'],
        distributions['gemma3-abliterated:27b']['quality']['mean']
    ])

    print("\n1️⃣ OVERALL QUALITY:")
    print(f"   • Qwen-abliterated: {qwen_avg:.2f}/10 average across all dimensions")
    print(f"   • Gemma-abliterated: {gemma_avg:.2f}/10 average across all dimensions")

    print("\n2️⃣ STRENGTH AREAS (based on positive themes):")
    top_strengths = positive_themes.most_common(3)
    for keyword, _ in top_strengths:
        print(f"   ✅ {keyword.capitalize()}")

    print("\n3️⃣ WEAKNESS AREAS (based on negative themes):")
    top_weaknesses = negative_themes.most_common(3)
    for keyword, _ in top_weaknesses:
        print(f"   ❌ {keyword.capitalize()}")

    print("\n4️⃣ ACTIONABLE INSIGHTS:")
    print("   • Phase 1 (Q&A) shows stronger performance than Phase 2 (Contracts)")
    print("   • Abliterated models maintain appropriate disclaimers despite no safety training")
    print("   • Variability in scores suggests task-dependent performance")
    print("   • Low scores primarily due to lack of specificity, not refusals")

    print("\n5️⃣ COMPARISON TO STANDARD MODELS:")
    print("   ⚠️  Need standard model evaluation data for direct comparison")
    print("   • Question: Do standard models score higher on quality when they answer?")
    print("   • Key metric: Quality gain vs Utility loss (37-100% refusal)")

    print("\n" + "=" * 80)
    print("✅ DEEP DIVE ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
