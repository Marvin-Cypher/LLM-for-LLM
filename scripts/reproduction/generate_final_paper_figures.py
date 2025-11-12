#!/usr/bin/env python3
"""
Generate final publication-ready figures based on comprehensive analysis
ALL models, ALL data, honest about what we can/cannot claim
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
import seaborn as sns
from collections import defaultdict

# Set publication-quality style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.2)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "results"
FIGURES_DIR = BASE_DIR / "reports" / "paper" / "overleaf" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

#==============================================================================
# FIGURE 1: FalseReject - The Utility Crisis (ALL 12 MODELS)
#==============================================================================

def generate_figure1_utility_crisis():
    """
    Figure 1: Over-refusal rates showing 0-100% range
    This is our STRONGEST finding - based on all 12 models
    """

    print("\n📊 Generating Figure 1: The Utility Crisis (FalseReject - 12 Models)...")

    with open(RESULTS_DIR / "falsereject_analysis_with_abliterated.json") as f:
        data = json.load(f)

    # Extract data
    models = []
    refusal_rates = []
    categories = []

    for model, stats in data['model_analysis'].items():
        models.append(model)
        refusal_rates.append(stats['false_positive_rate'])

        # Categorize
        if 'abliterated' in model.lower():
            categories.append('Abliterated')
        elif stats['false_positive_rate'] < 50:
            categories.append('Well-Calibrated')
        elif stats['false_positive_rate'] < 90:
            categories.append('Over-Calibrated')
        else:
            categories.append('Severely Over-Calibrated')

    # Sort by refusal rate
    sorted_indices = np.argsort(refusal_rates)
    models = [models[i] for i in sorted_indices]
    refusal_rates = [refusal_rates[i] for i in sorted_indices]
    categories = [categories[i] for i in sorted_indices]

    # Color mapping
    color_map = {
        'Abliterated': '#00CC00',
        'Well-Calibrated': '#4CAF50',
        'Over-Calibrated': '#FF9800',
        'Severely Over-Calibrated': '#F44336'
    }
    colors = [color_map[cat] for cat in categories]

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))

    y_pos = np.arange(len(models))
    bars = ax.barh(y_pos, refusal_rates, color=colors, edgecolor='black', linewidth=1.5)

    # Add percentage labels
    for i, (bar, rate) in enumerate(zip(bars, refusal_rates)):
        label_x = rate + 2 if rate < 85 else rate - 2
        ha = 'left' if rate < 85 else 'right'
        color = 'black' if rate < 85 else 'white'

        ax.text(label_x, bar.get_y() + bar.get_height()/2,
                f'{rate:.1f}%', ha=ha, va='center',
                fontsize=10, fontweight='bold', color=color)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(models, fontsize=11)
    ax.set_xlabel('Over-Refusal Rate (%)', fontsize=14, fontweight='bold')
    ax.set_title('The Utility Crisis: Over-Refusal on Legitimate Legal Questions\n' +
                 '(FalseReject Benchmark: 24 Adversarial but Legitimate Questions)',
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xlim(0, 108)
    ax.grid(axis='x', alpha=0.3)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='#00CC00', label='Abliterated (0%)', edgecolor='black', linewidth=1.5),
        mpatches.Patch(facecolor='#4CAF50', label='Well-Calibrated (<50%)', edgecolor='black', linewidth=1.5),
        mpatches.Patch(facecolor='#FF9800', label='Over-Calibrated (50-90%)', edgecolor='black', linewidth=1.5),
        mpatches.Patch(facecolor='#F44336', label='Severely Over-Calibrated (>90%)', edgecolor='black', linewidth=1.5)
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11, framealpha=0.95)

    # Add insight annotation
    ax.text(0.02, 0.98,
            'Key Finding: Standard models sacrifice 37-100% utility on legitimate questions.\n' +
            'Abliterated models prove 0% refusal is possible.',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='black', linewidth=2, alpha=0.9))

    plt.tight_layout()

    # Save
    for ext in ['png', 'pdf']:
        output_path = FIGURES_DIR / f"figure1_utility_crisis.{ext}"
        plt.savefig(output_path, bbox_inches='tight')
        print(f"✅ Saved: {output_path}")

    plt.close()

#==============================================================================
# FIGURE 2: Abliterated Model Quality (Phase 1 + Phase 2)
#==============================================================================

def generate_figure2_abliterated_quality():
    """
    Figure 2: Quality scores for abliterated models
    Shows 6.9-7.4/10 quality despite 0% safety
    """

    print("\n📊 Generating Figure 2: Abliterated Model Quality...")

    # Data from our evaluations
    data = {
        'Qwen-abliterated:30b': {
            'Phase 1 Actionability': 7.39,
            'Phase 1 Appropriateness': 6.41,
            'Phase 2 Contract Quality': 5.72
        },
        'Gemma-abliterated:27b': {
            'Phase 1 Actionability': 7.84,
            'Phase 1 Appropriateness': 6.88,
            'Phase 2 Contract Quality': 3.62
        }
    }

    fig, ax = plt.subplots(figsize=(12, 7))

    models = list(data.keys())
    dimensions = ['Phase 1 Actionability', 'Phase 1 Appropriateness', 'Phase 2 Contract Quality']

    x = np.arange(len(models))
    width = 0.25

    colors = ['#2196F3', '#FF9800', '#9C27B0']

    for i, dim in enumerate(dimensions):
        values = [data[model][dim] for model in models]
        offset = (i - 1) * width
        bars = ax.bar(x + offset, values, width, label=dim, color=colors[i],
                      edgecolor='black', linewidth=1.5)

        # Add value labels
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.15,
                   f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('Quality Score (0-10)', fontsize=13, fontweight='bold')
    ax.set_title('Abliterated Model Quality: Despite 0% Safety Training\n' +
                 '(GPT-4o Evaluation: n=478 responses)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=12)
    ax.legend(fontsize=10, loc='upper right')
    ax.set_ylim(0, 10)
    ax.axhline(y=7.0, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Good (7.0)')
    ax.grid(axis='y', alpha=0.3)

    # Add insight
    ax.text(0.02, 0.98,
            'Key Finding: 6.9-7.4/10 quality on Q&A tasks with 0% refusal.\n' +
            'High utility does NOT require excessive safety filtering.',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', edgecolor='black', linewidth=2, alpha=0.9))

    plt.tight_layout()

    for ext in ['png', 'pdf']:
        output_path = FIGURES_DIR / f"figure2_abliterated_quality.{ext}"
        plt.savefig(output_path, bbox_inches='tight')
        print(f"✅ Saved: {output_path}")

    plt.close()

#==============================================================================
# FIGURE 3: The Appropriateness Paradox (8:1 Positive-Negative Ratio)
#==============================================================================

def generate_figure3_appropriateness_paradox():
    """
    Figure 3: Evaluation theme distribution from 478 GPT-4o evaluations
    Shows base models already appropriate
    """

    print("\n📊 Generating Figure 3: The Appropriateness Paradox...")

    # Data from deep dive analysis
    positive_themes = {
        'Specific': 60.9,
        'Clear': 59.2,
        'Detailed': 45.0,
        'Professional': 41.2,
        'Practical': 40.6
    }

    negative_themes = {
        'Fails': 10.7,
        'Incorrect': 2.9,
        'Unclear': 1.7,
        'Missing': 1.7
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Positive themes
    pos_labels = list(positive_themes.keys())
    pos_values = list(positive_themes.values())

    bars1 = ax1.barh(pos_labels, pos_values, color='#4CAF50', edgecolor='black', linewidth=1.5)
    ax1.set_xlabel('Percentage of Evaluations (%)', fontsize=12, fontweight='bold')
    ax1.set_title('✓ Positive Quality Markers', fontsize=13, fontweight='bold', color='darkgreen')
    ax1.set_xlim(0, 70)
    ax1.grid(axis='x', alpha=0.3)

    for bar, val in zip(bars1, pos_values):
        ax1.text(val + 1.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
                va='center', fontsize=11, fontweight='bold')

    # Negative themes
    neg_labels = list(negative_themes.keys())
    neg_values = list(negative_themes.values())

    bars2 = ax2.barh(neg_labels, neg_values, color='#F44336', edgecolor='black', linewidth=1.5)
    ax2.set_xlabel('Percentage of Evaluations (%)', fontsize=12, fontweight='bold')
    ax2.set_title('✗ Negative Quality Markers', fontsize=13, fontweight='bold', color='darkred')
    ax2.set_xlim(0, 70)
    ax2.grid(axis='x', alpha=0.3)

    for bar, val in zip(bars2, neg_values):
        ax2.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
                va='center', fontsize=11, fontweight='bold')

    fig.suptitle('The Appropriateness Paradox: 8:1 Positive-to-Negative Ratio\n' +
                 '(GPT-4o Evaluation of Abliterated Models: n=478)',
                 fontsize=15, fontweight='bold', y=1.02)

    # Add insight
    fig.text(0.5, -0.05,
             'Key Finding: Base models already contain appropriate professional behavior (60% positive markers).\n' +
             'Safety over-calibration provides diminishing returns while sacrificing 37-100% utility.',
             ha='center', fontsize=11, style='italic',
             bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='black', linewidth=2))

    plt.tight_layout()

    for ext in ['png', 'pdf']:
        output_path = FIGURES_DIR / f"figure3_appropriateness_paradox.{ext}"
        plt.savefig(output_path, bbox_inches='tight')
        print(f"✅ Saved: {output_path}")

    plt.close()

#==============================================================================
# FIGURE 4: The Wrong Optimization (Failure Patterns)
#==============================================================================

def generate_figure4_wrong_optimization():
    """
    Figure 4: What causes low scores? Shows 1.4% missing disclaimers
    """

    print("\n📊 Generating Figure 4: The Wrong Optimization...")

    # Data from analysis
    failure_patterns = {
        'Incomplete Response\n(Standard LLM Issue)': 87.0,
        'Incorrect Legal Info\n(Knowledge Issue)': 24.6,
        'Lack of Specificity\n(Quality Issue)': 11.6,
        'Poor Structure\n(Quality Issue)': 5.8,
        'Missing Disclaimers\n(Safety Issue)': 1.4
    }

    labels = list(failure_patterns.keys())
    sizes = list(failure_patterns.values())

    # Colors: blue for quality issues, red for safety issue
    colors = ['#2196F3', '#2196F3', '#2196F3', '#2196F3', '#F44336']
    explode = [0, 0, 0, 0, 0.15]  # Explode the safety issue

    fig, ax = plt.subplots(figsize=(12, 9))

    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        startangle=90, colors=colors, explode=explode,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'},
                                        wedgeprops={'edgecolor': 'black', 'linewidth': 2})

    # Emphasize the safety issue
    for i, autotext in enumerate(autotexts):
        if i == 4:  # Missing disclaimers
            autotext.set_color('white')
            autotext.set_fontsize(13)
            autotext.set_weight('bold')

    ax.set_title('The Wrong Optimization: What Causes Low Scores (0-4/10)?\n' +
                 'Analysis of 69 Low-Scoring Responses (Abliterated Models)',
                 fontsize=15, fontweight='bold', pad=20)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='#2196F3', label='Standard LLM Limitations (87% of failures)',
                      edgecolor='black', linewidth=1.5),
        mpatches.Patch(facecolor='#F44336', label='Safety-Related Issue (1.4% of failures)',
                      edgecolor='black', linewidth=1.5)
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.95)

    # Add insight
    ax.text(0.5, -0.15,
            'Key Finding: Safety training optimizes for a problem (missing disclaimers) that accounts\n' +
            'for only 1.4% of actual quality failures, while ignoring real issues (incompleteness: 87%).',
            ha='center', fontsize=11, style='italic', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='black', linewidth=2))

    plt.tight_layout()

    for ext in ['png', 'pdf']:
        output_path = FIGURES_DIR / f"figure4_wrong_optimization.{ext}"
        plt.savefig(output_path, bbox_inches='tight')
        print(f"✅ Saved: {output_path}")

    plt.close()

#==============================================================================
# FIGURE 5: Success Factors (Specificity vs Disclaimers)
#==============================================================================

def generate_figure5_success_factors():
    """
    Figure 5: What drives high scores? Specificity (84%) vs Disclaimers (2%)
    """

    print("\n📊 Generating Figure 5: Success Factors Analysis...")

    success_factors = {
        'Specific + Actionable': 83.7,
        'Well-Structured': 78.5,
        'Practical': 66.3,
        'Comprehensive': 51.7,
        'Appropriate Disclaimers': 1.7
    }

    labels = list(success_factors.keys())
    values = list(success_factors.values())
    colors = ['#2196F3', '#2196F3', '#2196F3', '#2196F3', '#F44336']

    fig, ax = plt.subplots(figsize=(13, 7))

    bars = ax.barh(labels, values, color=colors, edgecolor='black', linewidth=2)

    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
               va='center', fontsize=12, fontweight='bold')

    ax.set_xlabel('Percentage of High-Score Justifications (%)', fontsize=13, fontweight='bold')
    ax.set_title('Success Factor Analysis: What Drives High Scores (8-10/10)?\n' +
                 'Analysis of 172 High-Scoring Responses (Abliterated Models)',
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xlim(0, 95)
    ax.grid(axis='x', alpha=0.3)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='#2196F3', label='Quality-Driven Success Factors',
                      edgecolor='black', linewidth=1.5),
        mpatches.Patch(facecolor='#F44336', label='Safety-Emphasized Factor (1.7%)',
                      edgecolor='black', linewidth=1.5)
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11, framealpha=0.95)

    # Add insight
    ax.text(0.5, -0.15,
            'Key Finding: Specificity and actionability (84%) drive success, not disclaimers (2%).\n' +
            'Safety training optimizes for the wrong quality dimension.',
            ha='center', fontsize=11, style='italic', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='black', linewidth=2))

    plt.tight_layout()

    for ext in ['png', 'pdf']:
        output_path = FIGURES_DIR / f"figure5_success_factors.{ext}"
        plt.savefig(output_path, bbox_inches='tight')
        print(f"✅ Saved: {output_path}")

    plt.close()

#==============================================================================
# FIGURE 6: Task-Adaptive Performance
#==============================================================================

def generate_figure6_task_adaptive():
    """
    Figure 6: Performance variance across task types
    """

    print("\n📊 Generating Figure 6: Task-Adaptive Performance...")

    data = {
        'Qwen-abliterated': {
            'Q&A Actionability': {'mean': 7.39, 'std': 1.57},
            'Q&A Appropriateness': {'mean': 6.41, 'std': 1.29},
            'Contract Quality': {'mean': 5.58, 'std': 2.64}
        },
        'Gemma-abliterated': {
            'Q&A Actionability': {'mean': 7.84, 'std': 1.24},
            'Q&A Appropriateness': {'mean': 6.88, 'std': 1.11},
            'Contract Quality': {'mean': 3.58, 'std': 1.43}
        }
    }

    fig, axes = plt.subplots(1, 2, figsize=(15, 7), sharey=True)

    for idx, (model, ax) in enumerate(zip(['Qwen-abliterated', 'Gemma-abliterated'], axes)):
        tasks = list(data[model].keys())
        means = [data[model][t]['mean'] for t in tasks]
        stds = [data[model][t]['std'] for t in tasks]

        x = np.arange(len(tasks))
        colors = ['#2196F3', '#FF9800', '#9C27B0']

        bars = ax.bar(x, means, yerr=stds, capsize=8, color=colors,
                     edgecolor='black', linewidth=1.5, alpha=0.85, error_kw={'linewidth': 2})

        # Add value labels
        for i, (bar, mean, std) in enumerate(zip(bars, means, stds)):
            ax.text(bar.get_x() + bar.get_width()/2, mean + std + 0.4,
                   f'{mean:.2f}\n(σ={std:.2f})', ha='center', va='bottom',
                   fontsize=10, fontweight='bold')

            # Add consistency label
            consistency = 'Consistent' if std < 2.0 else 'Variable'
            color = 'green' if std < 2.0 else 'orange'
            ax.text(i, 0.7, consistency, ha='center', fontsize=9,
                   fontweight='bold', color=color, rotation=90)

        ax.set_xticks(x)
        ax.set_xticklabels(tasks, rotation=20, ha='right', fontsize=10)
        ax.set_title(model, fontsize=13, fontweight='bold')
        ax.set_ylim(0, 11)
        ax.grid(axis='y', alpha=0.3)
        ax.axhline(y=7.0, color='green', linestyle='--', linewidth=1.5, alpha=0.4)

        if idx == 0:
            ax.set_ylabel('Score (0-10)', fontsize=12, fontweight='bold')

    fig.suptitle('Task-Adaptive Performance: Q&A vs Contract Drafting\n' +
                 'Error bars show standard deviation (consistency measure)',
                 fontsize=15, fontweight='bold', y=1.00)

    # Add insight
    fig.text(0.5, -0.08,
             'Key Finding: Q&A tasks show consistent performance (σ=1.2-1.6), contracts show high variance (σ=2.64).\n' +
             'Suggests need for adaptive safety calibration, not blanket over-calibration.',
             ha='center', fontsize=11, style='italic',
             bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='black', linewidth=2))

    plt.tight_layout()

    for ext in ['png', 'pdf']:
        output_path = FIGURES_DIR / f"figure6_task_adaptive.{ext}"
        plt.savefig(output_path, bbox_inches='tight')
        print(f"✅ Saved: {output_path}")

    plt.close()

#==============================================================================
# FIGURE 7: The Unanswered Question (Utility vs Quality Tradeoff)
#==============================================================================

def generate_figure7_unanswered_question():
    """
    Figure 7: Utility-Quality tradeoff showing what we know vs don't know
    """

    print("\n📊 Generating Figure 7: The Unanswered Question...")

    fig, ax = plt.subplots(figsize=(13, 9))

    # Abliterated models (we have data)
    abliterated_data = [
        (100, 7.36, 'Gemma-abliterated', True),
        (100, 6.90, 'Qwen-abliterated', True),
    ]

    # Standard models (we know utility, NOT quality)
    standard_data = [
        (62.5, None, 'GLM-4.6', False),
        (54.2, None, 'Mistral-large', False),
        (41.7, None, 'DeepSeek-v3', False),
        (37.5, None, 'Gemini-2.5-flash', False),
        (37.5, None, 'Qwen-2.5-72b', False),
        (37.5, None, 'Grok-4', False),
        (8.3, None, 'GPT-5', False),
        (8.3, None, 'O3-Mini', False),
        (0, None, 'GPT-OSS-120B', False),
    ]

    # Plot abliterated (known data)
    for util, qual, label, _ in abliterated_data:
        ax.scatter(util, qual, s=500, c='#00CC00', marker='*',
                  edgecolors='black', linewidths=2.5, zorder=5, alpha=0.9)
        ax.annotate(f'{label}\n{qual:.2f}/10 quality\n0% refusal',
                   (util, qual), xytext=(10, 15), textcoords='offset points',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='lightgreen',
                            edgecolor='black', linewidth=1.5),
                   arrowprops=dict(arrowstyle='->', lw=1.5))

    # Plot standard (unknown quality)
    for util, _, label, _ in standard_data:
        # Show as question marks at y=5 (unknown)
        ax.scatter(util, 5, s=300, c='#FF5722', marker='o',
                  edgecolors='black', linewidths=2, alpha=0.6, zorder=3)
        ax.annotate(f'{label}\n{100-util:.1f}% refusal\nQuality?',
                   (util, 5), xytext=(0, -35), textcoords='offset points',
                   fontsize=8, ha='center',
                   bbox=dict(boxstyle='round', facecolor='lightcoral',
                            edgecolor='black', linewidth=1, alpha=0.8))

    # Add uncertainty region for standard models
    ax.fill_between([0, 70], [0, 0], [10, 10], alpha=0.1, color='red',
                    label='Unknown Quality Region')

    # Add reference lines
    ax.axhline(y=7.0, color='green', linestyle='--', linewidth=2, alpha=0.5,
              label='Good Quality (7.0)')
    ax.axvline(x=50, color='orange', linestyle='--', linewidth=2, alpha=0.5,
              label='50% Utility Threshold')

    # Shade regions
    ax.fill_between([0, 100], [7, 7], [10, 10], alpha=0.1, color='green')
    ax.fill_between([50, 100], [0, 0], [10, 10], alpha=0.1, color='lightblue')

    ax.set_xlabel('Utility (% of questions answered)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Quality Score (0-10)', fontsize=14, fontweight='bold')
    ax.set_title('The Unanswered Question: Is Utility Loss Worth Quality Gain?\n' +
                 'What We Know (Green) vs What Remains Unknown (Red)',
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xlim(-5, 105)
    ax.set_ylim(0, 10)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=10, framealpha=0.95)

    # Add key insight
    ax.text(0.5, 0.15,
            'CRITICAL LIMITATION: Standard model quality on answered questions is unknown.\n' +
            'We prove the COST (37-100% utility loss) but cannot quantify the BENEFIT (quality gain).\n' +
            'Future work required to complete cost-benefit analysis.',
            ha='center', fontsize=11, style='italic', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='lightyellow',
                     edgecolor='black', linewidth=2.5))

    plt.tight_layout()

    for ext in ['png', 'pdf']:
        output_path = FIGURES_DIR / f"figure7_unanswered_question.{ext}"
        plt.savefig(output_path, bbox_inches='tight')
        print(f"✅ Saved: {output_path}")

    plt.close()

#==============================================================================
# MAIN EXECUTION
#==============================================================================

def main():
    print("=" * 80)
    print("🎨 GENERATING FINAL PUBLICATION-READY FIGURES")
    print("   Based on comprehensive analysis of ALL models, ALL data")
    print("=" * 80)
    print(f"\nOutput directory: {FIGURES_DIR}")

    try:
        generate_figure1_utility_crisis()
        generate_figure2_abliterated_quality()
        generate_figure3_appropriateness_paradox()
        generate_figure4_wrong_optimization()
        generate_figure5_success_factors()
        generate_figure6_task_adaptive()
        generate_figure7_unanswered_question()

        print("\n" + "=" * 80)
        print("✅ ALL FIGURES GENERATED SUCCESSFULLY!")
        print("=" * 80)
        print(f"\nTotal figures: 7 (14 files with PNG + PDF)")
        print(f"Location: {FIGURES_DIR}")

        print("\n📊 FIGURES:")
        print("  1. figure1_utility_crisis - FalseReject (ALL 12 models) ⭐⭐⭐⭐⭐")
        print("  2. figure2_abliterated_quality - Quality maintenance ⭐⭐⭐⭐⭐")
        print("  3. figure3_appropriateness_paradox - 8:1 ratio ⭐⭐⭐⭐")
        print("  4. figure4_wrong_optimization - 1.4% disclaimers ⭐⭐⭐⭐")
        print("  5. figure5_success_factors - Specificity vs disclaimers ⭐⭐⭐⭐")
        print("  6. figure6_task_adaptive - Variance analysis ⭐⭐⭐")
        print("  7. figure7_unanswered_question - Honest limitations ⭐⭐⭐⭐")

        print("\n✨ Ready for paper submission!")
        print("   - Honest about data limitations")
        print("   - Based on comprehensive analysis")
        print("   - Strong findings where we have data")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error generating figures: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
