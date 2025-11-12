#!/usr/bin/env python3
"""
FIXED VERSION: Generate comprehensive figures with ALL 12 models merged together
Fixes:
1. Heatmap logic issues
2. Figure5 readability (text too long)
3. Add Phase 2 contracts data
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

OUTPUT_DIR = Path('reports/paper/overleaf/figures')

def load_all_data():
    """Load all evaluation data including Phase 2"""
    # Phase 1 scores (ALL 10 standard models)
    with open('results/phase1_all_models_eval_scores.json', 'r') as f:
        phase1_standard = json.load(f)

    # Phase 1 abliterated scores
    gemma_action = []
    gemma_approp = []
    qwen_action = []
    qwen_approp = []

    with open('results/batch_actionability_gemma3_output.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            resp = json.loads(data['response']['body']['choices'][0]['message']['content'])
            gemma_action.append(resp.get('score', 0))

    with open('results/batch_appropriateness_gemma3_output.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            resp = json.loads(data['response']['body']['choices'][0]['message']['content'])
            gemma_approp.append(resp.get('score', 0))

    with open('results/batch_actionability_qwen3_output.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            resp = json.loads(data['response']['body']['choices'][0]['message']['content'])
            qwen_action.append(resp.get('score', 0))

    with open('results/batch_appropriateness_qwen3_output.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            resp = json.loads(data['response']['body']['choices'][0]['message']['content'])
            qwen_approp.append(resp.get('score', 0))

    # FalseReject
    with open('results/falsereject_all_models_eval_scores.json', 'r') as f:
        falsereject_standard = json.load(f)

    with open('results/falsereject_analysis_with_abliterated.json', 'r') as f:
        falsereject_refusal = json.load(f)

    # Phase 2 (Contracts)
    with open('results/phase2_final_with_abliterated_scored.json', 'r') as f:
        phase2_data = json.load(f)

    # Phase 2 abliterated quality scores
    gemma_phase2 = []
    qwen_phase2 = []

    with open('results/batch_quality_gemma3_output.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            resp = json.loads(data['response']['body']['choices'][0]['message']['content'])
            gemma_phase2.append(resp.get('score', 0))

    with open('results/batch_quality_qwen3_output.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            resp = json.loads(data['response']['body']['choices'][0]['message']['content'])
            qwen_phase2.append(resp.get('score', 0))

    return {
        'phase1_standard': phase1_standard,
        'gemma_action': gemma_action,
        'gemma_approp': gemma_approp,
        'qwen_action': qwen_action,
        'qwen_approp': qwen_approp,
        'falsereject_standard': falsereject_standard,
        'falsereject_refusal': falsereject_refusal,
        'phase2_data': phase2_data,
        'gemma_phase2': gemma_phase2,
        'qwen_phase2': qwen_phase2
    }

def calculate_all_scores(data):
    """Calculate comprehensive scores for ALL 12 models across all 3 benchmarks"""

    scores = {}

    # Phase 1: Standard models
    for model, questions in data['phase1_standard']['scores_by_model'].items():
        approp_scores = []
        action_scores = []

        for q_idx, dims in questions.items():
            if 'appropriateness' in dims and dims['appropriateness'].get('appropriateness_score'):
                approp_scores.append(dims['appropriateness']['appropriateness_score'])
            if 'actionability' in dims and dims['actionability'].get('actionability_score'):
                action_scores.append(dims['actionability']['actionability_score'])

        if approp_scores and action_scores:
            scores[model] = {
                'phase1_appropriateness': np.mean(approp_scores),
                'phase1_actionability': np.mean(action_scores),
                'phase1_overall': (np.mean(approp_scores) + np.mean(action_scores)) / 2,
                'type': 'standard'
            }

    # Phase 1: Abliterated models
    scores['gemma3-abliterated:27b'] = {
        'phase1_appropriateness': np.mean(data['gemma_approp']),
        'phase1_actionability': np.mean(data['gemma_action']),
        'phase1_overall': (np.mean(data['gemma_approp']) + np.mean(data['gemma_action'])) / 2,
        'type': 'abliterated'
    }

    scores['qwen3-vl-abliterated:30b'] = {
        'phase1_appropriateness': np.mean(data['qwen_approp']),
        'phase1_actionability': np.mean(data['qwen_action']),
        'phase1_overall': (np.mean(data['qwen_approp']) + np.mean(data['qwen_action'])) / 2,
        'type': 'abliterated'
    }

    # FalseReject: ALL models
    for model, model_data in data['falsereject_refusal']['model_analysis'].items():
        if model not in scores:
            scores[model] = {'type': 'standard' if 'abliterated' not in model else 'abliterated'}

        scores[model]['falsereject_refusal_rate'] = model_data['false_positive_rate']
        scores[model]['falsereject_utility'] = 100 - model_data['false_positive_rate']

    # Phase 2: Abliterated only (standard models don't have quality scores)
    scores['gemma3-abliterated:27b']['phase2_quality'] = np.mean(data['gemma_phase2'])
    scores['qwen3-vl-abliterated:30b']['phase2_quality'] = np.mean(data['qwen_phase2'])

    return scores

def figure4_comprehensive_heatmap_FIXED(scores):
    """FIXED: Heatmap showing performance across all benchmarks"""

    fig, ax = plt.subplots(figsize=(12, 10))

    # Prepare data - sort by Phase1 overall score
    sorted_models = sorted(
        [m for m in scores.keys() if 'phase1_overall' in scores[m]],
        key=lambda x: scores[x]['phase1_overall'],
        reverse=True
    )

    # Metrics to display
    metrics = [
        'Phase1\nAppropriateness',
        'Phase1\nActionability',
        'Phase1\nOverall',
        'FalseReject\nUtility (%)',
        'Phase2\nQuality'
    ]

    # Build data matrix
    data_matrix = []
    for model in sorted_models:
        row = [
            scores[model].get('phase1_appropriateness', 0),
            scores[model].get('phase1_actionability', 0),
            scores[model].get('phase1_overall', 0),
            scores[model].get('falsereject_utility', 0),
            scores[model].get('phase2_quality', 0)  # Will be 0 for standard models
        ]
        data_matrix.append(row)

    data_array = np.array(data_matrix)

    # Normalize for visualization
    normalized = data_array.copy()
    normalized[:, :3] = data_array[:, :3] / 10  # Quality scores 0-10
    normalized[:, 3] = data_array[:, 3] / 100  # Utility percentage 0-100
    normalized[:, 4] = data_array[:, 4] / 10  # Phase2 quality 0-10

    # Create heatmap
    im = ax.imshow(normalized, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)

    # Set ticks
    ax.set_xticks(np.arange(len(metrics)))
    ax.set_yticks(np.arange(len(sorted_models)))
    ax.set_xticklabels(metrics, fontsize=10, fontweight='bold')

    # Shorten model names for y-axis
    short_names = []
    for m in sorted_models:
        if '/' in m:
            short_names.append(m.split('/')[-1])
        elif ':' in m:
            short_names.append(m.split(':')[0])
        else:
            short_names.append(m)

    ax.set_yticklabels(short_names, fontsize=9)

    # Rotate x labels
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

    # Add values in cells
    for i in range(len(sorted_models)):
        for j in range(len(metrics)):
            value = data_array[i, j]
            if j == 3:  # Utility percentage
                text_str = f'{value:.0f}%' if value > 0 else '-'
            elif j == 4 and value == 0:  # Phase2 (only abliterated have scores)
                text_str = 'N/A'
            elif value > 0:
                text_str = f'{value:.1f}'
            else:
                text_str = '-'

            # Color: white text on dark cells, black on light cells
            text_color = 'white' if normalized[i, j] < 0.5 else 'black'
            ax.text(j, i, text_str, ha="center", va="center", color=text_color, fontsize=8, fontweight='bold')

    ax.set_title('Comprehensive Performance: ALL 12 Models Across 3 Benchmarks\n' +
                 'Phase1 (n=100) | FalseReject (n=24) | Phase2 (n=40)',
                 fontweight='bold', fontsize=12, pad=15)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Normalized Score\n(0=worst, 1=best)', rotation=270, labelpad=20, fontweight='bold')

    # Add note about Phase2
    fig.text(0.5, 0.02, 'Note: Phase2 quality scores available only for abliterated models',
             ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(OUTPUT_DIR / 'figure4_comprehensive_heatmap.png', bbox_inches='tight', dpi=300)
    plt.savefig(OUTPUT_DIR / 'figure4_comprehensive_heatmap.pdf', bbox_inches='tight')
    plt.close()

    print("✅ Figure 4: Comprehensive Heatmap (FIXED)")

def figure5_ranking_comparison_FIXED(scores):
    """FIXED: Readable rankings without long text"""

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Get models with complete data
    complete_models = [m for m in scores.keys() if 'phase1_overall' in scores[m]]

    # 1. Phase1 Quality Rankings
    sorted_phase1 = sorted(complete_models, key=lambda x: scores[x]['phase1_overall'], reverse=True)
    short_names_p1 = [m.split('/')[-1] if '/' in m else m.split(':')[0] if ':' in m else m for m in sorted_phase1]
    scores_p1 = [scores[m]['phase1_overall'] for m in sorted_phase1]
    types_p1 = [scores[m]['type'] for m in sorted_phase1]
    colors_p1 = ['#4CAF50' if t == 'abliterated' else '#2196F3' for t in types_p1]

    axes[0, 0].barh(short_names_p1, scores_p1, color=colors_p1, alpha=0.8, edgecolor='black', linewidth=0.5)
    axes[0, 0].set_xlabel('Quality Score (0-10)', fontweight='bold')
    axes[0, 0].set_title('Phase1 Q&A Quality Rankings (n=100)', fontweight='bold', fontsize=11)
    axes[0, 0].axvline(x=8, color='gray', linestyle='--', alpha=0.5, label='High quality (8.0)')
    axes[0, 0].grid(axis='x', alpha=0.3)
    axes[0, 0].legend(fontsize=8)
    axes[0, 0].set_xlim(6, 10)

    # 2. FalseReject Utility Rankings
    models_with_fr = [m for m in complete_models if 'falsereject_utility' in scores[m]]
    sorted_fr = sorted(models_with_fr, key=lambda x: scores[x]['falsereject_utility'], reverse=True)
    short_names_fr = [m.split('/')[-1] if '/' in m else m.split(':')[0] if ':' in m else m for m in sorted_fr]
    utility_fr = [scores[m]['falsereject_utility'] for m in sorted_fr]
    types_fr = [scores[m]['type'] for m in sorted_fr]
    colors_fr = ['#4CAF50' if t == 'abliterated' else '#2196F3' for t in types_fr]

    axes[0, 1].barh(short_names_fr, utility_fr, color=colors_fr, alpha=0.8, edgecolor='black', linewidth=0.5)
    axes[0, 1].set_xlabel('Utility: % Answered (0-100%)', fontweight='bold')
    axes[0, 1].set_title('FalseReject Utility Rankings (n=24)', fontweight='bold', fontsize=11)
    axes[0, 1].axvline(x=50, color='gray', linestyle='--', alpha=0.5, label='50% threshold')
    axes[0, 1].grid(axis='x', alpha=0.3)
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].set_xlim(0, 105)

    # 3. Combined Score (Quality × Utility)
    combined_scores = {}
    for model in models_with_fr:
        quality = scores[model]['phase1_overall'] / 10  # Normalize
        utility = scores[model]['falsereject_utility'] / 100  # Normalize
        combined = quality * utility * 100  # Scale to 0-100
        combined_scores[model] = combined

    sorted_combined = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    short_names_comb = [m[0].split('/')[-1] if '/' in m[0] else m[0].split(':')[0] if ':' in m[0] else m[0] for m in sorted_combined]
    scores_comb = [m[1] for m in sorted_combined]
    types_comb = [scores[m[0]]['type'] for m in sorted_combined]
    colors_comb = ['#4CAF50' if t == 'abliterated' else '#2196F3' for t in types_comb]

    axes[1, 0].barh(short_names_comb, scores_comb, color=colors_comb, alpha=0.8, edgecolor='black', linewidth=0.5)
    axes[1, 0].set_xlabel('Combined Score (Quality × Utility)', fontweight='bold')
    axes[1, 0].set_title('Overall Performance Rankings', fontweight='bold', fontsize=11)
    axes[1, 0].grid(axis='x', alpha=0.3)
    axes[1, 0].set_xlim(0, 100)

    # 4. Compact Statistics Table
    axes[1, 1].axis('off')

    # Create compact table
    stats_data = [
        ['Metric', 'Best', 'Score', 'Worst', 'Score'],
        ['', '', '', '', ''],
        ['Phase1', short_names_p1[0], f'{scores_p1[0]:.2f}', short_names_p1[-1], f'{scores_p1[-1]:.2f}'],
        ['FalseReject', short_names_fr[0], f'{utility_fr[0]:.0f}%', short_names_fr[-1], f'{utility_fr[-1]:.0f}%'],
        ['Combined', short_names_comb[0], f'{scores_comb[0]:.1f}', short_names_comb[-1], f'{scores_comb[-1]:.1f}'],
        ['', '', '', '', ''],
        ['Stats', 'Value', '', '', ''],
        ['Models', '12', '', '', ''],
        ['Phase1 Qs', '100', '', '', ''],
        ['FalseReject', '24', '', '', ''],
        ['Phase2 Tasks', '40', '', '', ''],
    ]

    table = axes[1, 1].table(cellText=stats_data, cellLoc='left', loc='center',
                             colWidths=[0.15, 0.2, 0.15, 0.2, 0.15],
                             bbox=[0.05, 0.1, 0.9, 0.8])

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # Style header row
    for i in range(5):
        table[(0, i)].set_facecolor('#E8EAF6')
        table[(0, i)].set_text_props(weight='bold')

    # Add legend
    abliterated_patch = mpatches.Patch(color='#4CAF50', label='Abliterated (n=2)', alpha=0.8)
    standard_patch = mpatches.Patch(color='#2196F3', label='Standard (n=10)', alpha=0.8)
    axes[1, 1].legend(handles=[abliterated_patch, standard_patch], loc='lower center',
                     fontsize=10, frameon=True, ncol=2)

    plt.suptitle('Performance Rankings: ALL 12 Models', fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    plt.savefig(OUTPUT_DIR / 'figure5_ranking_comparison.png', bbox_inches='tight', dpi=300)
    plt.savefig(OUTPUT_DIR / 'figure5_ranking_comparison.pdf', bbox_inches='tight')
    plt.close()

    print("✅ Figure 5: Ranking Comparison (FIXED - Readable)")

def main():
    print("="*80)
    print("GENERATING FIXED COMPREHENSIVE FIGURES")
    print("="*80)
    print("\nFixes:")
    print("  1. Figure4: Fixed heatmap logic")
    print("  2. Figure5: Made text readable (shortened names)")
    print("  3. Added Phase2 contracts data (40 tasks, 2 abliterated models)")
    print()

    # Load data
    print("📥 Loading ALL data (Phase1 + FalseReject + Phase2)...")
    data = load_all_data()

    # Calculate scores
    print("🔄 Calculating comprehensive scores...")
    scores = calculate_all_scores(data)

    print(f"\n✅ Scores calculated for {len(scores)} models")
    print(f"   Phase1: {sum(1 for s in scores.values() if 'phase1_overall' in s)} models")
    print(f"   FalseReject: {sum(1 for s in scores.values() if 'falsereject_utility' in s)} models")
    print(f"   Phase2: {sum(1 for s in scores.values() if 'phase2_quality' in s and s['phase2_quality'] > 0)} models")

    # Generate FIXED figures
    print("\n📊 Generating FIXED figures...")
    figure4_comprehensive_heatmap_FIXED(scores)
    figure5_ranking_comparison_FIXED(scores)

    print("\n" + "="*80)
    print("✅ FIXED FIGURES GENERATED!")
    print("="*80)
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    print("\nFixed figures:")
    print("  • figure4_comprehensive_heatmap.png/pdf (FIXED logic)")
    print("  • figure5_ranking_comparison.png/pdf (FIXED readability)")

if __name__ == '__main__':
    main()
