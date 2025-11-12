#!/usr/bin/env python3
"""
Regenerate ALL figures for the legal LLM benchmark paper
Based on latest data including abliterated models
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
from collections import defaultdict
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "results"
FIGURES_DIR = BASE_DIR / "reports" / "paper" / "overleaf" / "figures"

# Ensure figures directory exists
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

def load_falsereject_data():
    """Load FalseReject analysis with abliterated models"""
    with open(RESULTS_DIR / "falsereject_analysis_with_abliterated.json", 'r') as f:
        return json.load(f)

def load_phase1_data():
    """Load Phase 1 data with evaluation scores"""
    with open(RESULTS_DIR / "phase1_final_with_abliterated_scored.json", 'r') as f:
        return json.load(f)

def load_phase2_data():
    """Load Phase 2 data with evaluation scores"""
    with open(RESULTS_DIR / "phase2_final_with_abliterated_scored.json", 'r') as f:
        return json.load(f)

#==============================================================================
# FIGURE 1: FalseReject Refusal Rates (Horizontal Bar Chart)
#==============================================================================

def generate_figure1_falsereject_rates():
    """Figure 1: FalseReject refusal rates for all 12 models"""

    print("\n📊 Generating Figure 1: FalseReject Refusal Rates...")

    data = load_falsereject_data()

    # Extract model names and refusal rates from model_analysis
    models = []
    refusal_rates = []
    is_abliterated = []

    for model, stats in data['model_analysis'].items():
        models.append(model)
        refusal_rates.append(stats['false_positive_rate'])  # Already in percentage
        is_abliterated.append('abliterated' in model.lower())

    # Sort by refusal rate
    sorted_indices = np.argsort(refusal_rates)
    models = [models[i] for i in sorted_indices]
    refusal_rates = [refusal_rates[i] for i in sorted_indices]
    is_abliterated = [is_abliterated[i] for i in sorted_indices]

    # Create color scheme
    colors = []
    for i, model in enumerate(models):
        if is_abliterated[i]:
            colors.append('#00ff00')  # Bright green for abliterated
        elif refusal_rates[i] < 50:
            colors.append('#4CAF50')  # Green for low refusal
        elif refusal_rates[i] < 75:
            colors.append('#FFC107')  # Orange for medium
        else:
            colors.append('#F44336')  # Red for high refusal

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))

    y_pos = np.arange(len(models))
    bars = ax.barh(y_pos, refusal_rates, color=colors, edgecolor='black', linewidth=1)

    # Add markers for abliterated models
    for i, (model, rate, abliterated) in enumerate(zip(models, refusal_rates, is_abliterated)):
        if abliterated:
            ax.text(rate + 2, i, '✓', fontsize=14, fontweight='bold', va='center')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(models, fontsize=10)
    ax.set_xlabel('Refusal Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('FalseReject Benchmark: Over-Refusal Rates on Legitimate Legal Questions',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 105)

    # Add percentage labels on bars
    for i, (bar, rate) in enumerate(zip(bars, refusal_rates)):
        width = bar.get_width()
        label_x = width + 1 if width < 90 else width - 3
        ha = 'left' if width < 90 else 'right'
        color = 'black' if width < 90 else 'white'
        ax.text(label_x, bar.get_y() + bar.get_height()/2,
                f'{rate:.1f}%', ha=ha, va='center', fontsize=9,
                fontweight='bold', color=color)

    # Legend
    legend_elements = [
        mpatches.Patch(color='#00ff00', label='Abliterated (0% refusal) ✓', edgecolor='black'),
        mpatches.Patch(color='#4CAF50', label='Low Over-Refusal (<50%)', edgecolor='black'),
        mpatches.Patch(color='#FFC107', label='Medium Over-Refusal (50-75%)', edgecolor='black'),
        mpatches.Patch(color='#F44336', label='High Over-Refusal (>75%)', edgecolor='black')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

    plt.tight_layout()

    output_path = FIGURES_DIR / "figure1_falsereject_refusal_rates.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")

    # Also save as PDF for publication
    plt.savefig(FIGURES_DIR / "figure1_falsereject_refusal_rates.pdf", bbox_inches='tight')

    plt.close()

#==============================================================================
# FIGURE 2: Tiered Rejection Rates (Grouped Bar)
#==============================================================================

def generate_figure2_tiered_rejection():
    """Figure 2: Models grouped by safety calibration level"""

    print("\n📊 Generating Figure 2: Tiered Rejection Rates...")

    data = load_falsereject_data()

    # Group models by tier
    tiers = {
        'Abliterated\n(0% refusal)': [],
        'Well-Calibrated\n(<50% refusal)': [],
        'Over-Calibrated\n(50-90% refusal)': [],
        'Severely Over-Calibrated\n(>90% refusal)': []
    }

    for model, stats in data['model_analysis'].items():
        rate = stats['false_positive_rate']  # Already percentage
        is_abliterated = 'abliterated' in model.lower()

        if is_abliterated:
            tiers['Abliterated\n(0% refusal)'].append((model, rate))
        elif rate < 50:
            tiers['Well-Calibrated\n(<50% refusal)'].append((model, rate))
        elif rate < 90:
            tiers['Over-Calibrated\n(50-90% refusal)'].append((model, rate))
        else:
            tiers['Severely Over-Calibrated\n(>90% refusal)'].append((model, rate))

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))

    tier_names = list(tiers.keys())
    tier_colors = ['#00ff00', '#4CAF50', '#FFC107', '#F44336']

    x_offset = 0
    bar_width = 0.6
    all_positions = []
    all_labels = []

    for tier_idx, (tier_name, models_in_tier) in enumerate(tiers.items()):
        if not models_in_tier:
            continue

        # Sort by refusal rate within tier
        models_in_tier.sort(key=lambda x: x[1])

        positions = np.arange(len(models_in_tier)) + x_offset
        rates = [rate for _, rate in models_in_tier]
        labels = [model for model, _ in models_in_tier]

        ax.bar(positions, rates, bar_width,
               label=tier_name, color=tier_colors[tier_idx],
               edgecolor='black', linewidth=1)

        # Add value labels
        for pos, rate in zip(positions, rates):
            ax.text(pos, rate + 2, f'{rate:.1f}%',
                   ha='center', va='bottom', fontsize=8, fontweight='bold')

        all_positions.extend(positions)
        all_labels.extend(labels)

        x_offset += len(models_in_tier) + 0.5

    ax.set_xticks(all_positions)
    ax.set_xticklabels(all_labels, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Refusal Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Safety Calibration Tiers: Abliterated vs Standard Models',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 110)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    output_path = FIGURES_DIR / "figure2_tiered_rejection_rates.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.savefig(FIGURES_DIR / "figure2_tiered_rejection_rates.pdf", bbox_inches='tight')

    plt.close()

#==============================================================================
# FIGURE 3: Phase 1 Quality Scores (Actionability + Appropriateness)
#==============================================================================

def generate_figure3_phase1_quality():
    """Figure 3: Phase 1 quality scores for abliterated models"""

    print("\n📊 Generating Figure 3: Phase 1 Quality Scores...")

    data = load_phase1_data()

    # Collect scores by model and dimension
    model_scores = defaultdict(lambda: {'actionability': [], 'appropriateness': []})

    for question in data['questions']:
        for model, response in question['model_responses'].items():
            if 'abliterated' not in model:
                continue

            if 'evaluation' in response:
                if 'actionability_score' in response['evaluation']:
                    model_scores[model]['actionability'].append(response['evaluation']['actionability_score'])
                if 'appropriateness_score' in response['evaluation']:
                    model_scores[model]['appropriateness'].append(response['evaluation']['appropriateness_score'])

    # Calculate averages
    models = sorted(model_scores.keys())
    actionability_avgs = [np.mean(model_scores[m]['actionability']) if model_scores[m]['actionability'] else 0
                          for m in models]
    appropriateness_avgs = [np.mean(model_scores[m]['appropriateness']) if model_scores[m]['appropriateness'] else 0
                            for m in models]

    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(models))
    width = 0.35

    bars1 = ax.bar(x - width/2, actionability_avgs, width, label='Actionability',
                   color='#2196F3', edgecolor='black', linewidth=1)
    bars2 = ax.bar(x + width/2, appropriateness_avgs, width, label='Appropriateness',
                   color='#FF9800', edgecolor='black', linewidth=1)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{height:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('Average Score (0-10)', fontsize=12, fontweight='bold')
    ax.set_title('Phase 1 Quality Scores: Abliterated Models (Q&A Tasks)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=15, ha='right')
    ax.legend(fontsize=11)
    ax.set_ylim(0, 10)
    ax.grid(True, alpha=0.3, axis='y')

    # Add horizontal line at 7.0 (good performance threshold)
    ax.axhline(y=7.0, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Good (7.0)')

    plt.tight_layout()

    output_path = FIGURES_DIR / "figure3_phase1_quality_scores.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.savefig(FIGURES_DIR / "figure3_phase1_quality_scores.pdf", bbox_inches='tight')

    plt.close()

#==============================================================================
# FIGURE 4: Evaluation Theme Distribution (New Insight!)
#==============================================================================

def generate_figure4_theme_distribution():
    """Figure 4: Positive vs Negative evaluation themes (8:1 ratio)"""

    print("\n📊 Generating Figure 4: Evaluation Theme Distribution...")

    # Data from deep dive analysis
    positive_themes = {
        'Specific': 60.9,
        'Clear': 59.2,
        'Detailed': 45.0,
        'Professional': 41.2,
        'Practical': 40.6,
        'Helpful': 30.8,
        'Actionable': 30.5,
        'Concrete': 24.5
    }

    negative_themes = {
        'Fails': 10.7,
        'Incorrect': 2.9,
        'Unclear': 1.7,
        'Missing': 1.7,
        'Limited': 1.3
    }

    # Create side-by-side bar chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Positive themes
    pos_labels = list(positive_themes.keys())
    pos_values = list(positive_themes.values())

    bars1 = ax1.barh(pos_labels, pos_values, color='#4CAF50', edgecolor='black', linewidth=1)
    ax1.set_xlabel('Percentage of Evaluations (%)', fontsize=11, fontweight='bold')
    ax1.set_title('✅ Positive Quality Markers', fontsize=12, fontweight='bold', color='green')
    ax1.set_xlim(0, 70)

    for bar, val in zip(bars1, pos_values):
        ax1.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
                va='center', fontsize=9, fontweight='bold')

    # Negative themes
    neg_labels = list(negative_themes.keys())
    neg_values = list(negative_themes.values())

    bars2 = ax2.barh(neg_labels, neg_values, color='#F44336', edgecolor='black', linewidth=1)
    ax2.set_xlabel('Percentage of Evaluations (%)', fontsize=11, fontweight='bold')
    ax2.set_title('❌ Negative Quality Markers', fontsize=12, fontweight='bold', color='red')
    ax2.set_xlim(0, 70)

    for bar, val in zip(bars2, neg_values):
        ax2.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
                va='center', fontsize=9, fontweight='bold')

    fig.suptitle('GPT-4o Evaluation Themes: 8:1 Positive-to-Negative Ratio (n=478)',
                 fontsize=14, fontweight='bold', y=1.02)

    plt.tight_layout()

    output_path = FIGURES_DIR / "figure4_evaluation_themes.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.savefig(FIGURES_DIR / "figure4_evaluation_themes.pdf", bbox_inches='tight')

    plt.close()

#==============================================================================
# FIGURE 5: Failure Pattern Breakdown (New Insight!)
#==============================================================================

def generate_figure5_failure_patterns():
    """Figure 5: What causes low scores? (Incompleteness vs Disclaimers)"""

    print("\n📊 Generating Figure 5: Failure Pattern Analysis...")

    # Data from deep dive analysis
    failure_patterns = {
        'Incomplete Response': 87,  # 60/69 as percentage
        'Incorrect Legal Info': 25,  # 17/69
        'Lack of Specificity': 12,   # 8/69
        'Poor Structure': 6,         # 4/69
        'Missing Disclaimers': 1.4   # 1/69 - the "safety" issue!
    }

    labels = list(failure_patterns.keys())
    sizes = list(failure_patterns.values())

    # Color code: red for safety issue, blue for quality issues
    colors = ['#2196F3', '#2196F3', '#2196F3', '#2196F3', '#F44336']
    explode = [0, 0, 0, 0, 0.15]  # Explode the disclaimers slice

    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        startangle=90, colors=colors, explode=explode,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'},
                                        wedgeprops={'edgecolor': 'black', 'linewidth': 2})

    # Highlight the disclaimers slice
    for i, (label, autotext) in enumerate(zip(labels, autotexts)):
        if 'Disclaimers' in label:
            autotext.set_color('white')
            autotext.set_fontsize(12)

    ax.set_title('Failure Pattern Analysis: What Causes Low Scores (0-4/10)?\n' +
                 'Abliterated Models (n=69 low-scoring responses)',
                 fontsize=14, fontweight='bold', pad=20)

    # Add legend
    legend_elements = [
        mpatches.Patch(color='#2196F3', label='Standard LLM Limitations', edgecolor='black'),
        mpatches.Patch(color='#F44336', label='Safety-Related Issue (1.4%!)', edgecolor='black')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11)

    # Add annotation
    ax.text(0.5, -1.3, 'Key Insight: Safety training optimizes for a problem (missing disclaimers)\n' +
            'that accounts for only 1.4% of actual quality failures.',
            ha='center', fontsize=11, style='italic', bbox=dict(boxstyle='round',
            facecolor='lightyellow', edgecolor='black', linewidth=2))

    plt.tight_layout()

    output_path = FIGURES_DIR / "figure5_failure_patterns.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.savefig(FIGURES_DIR / "figure5_failure_patterns.pdf", bbox_inches='tight')

    plt.close()

#==============================================================================
# FIGURE 6: Task-Adaptive Performance (Variance Analysis)
#==============================================================================

def generate_figure6_task_variance():
    """Figure 6: Performance variance across task types"""

    print("\n📊 Generating Figure 6: Task-Adaptive Performance...")

    # Data from analysis
    task_performance = {
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

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    for ax, model in zip([ax1, ax2], ['Qwen-abliterated', 'Gemma-abliterated']):
        tasks = list(task_performance[model].keys())
        means = [task_performance[model][t]['mean'] for t in tasks]
        stds = [task_performance[model][t]['std'] for t in tasks]

        x = np.arange(len(tasks))

        # Bar chart with error bars
        bars = ax.bar(x, means, yerr=stds, capsize=10,
                     color=['#2196F3', '#FF9800', '#9C27B0'],
                     edgecolor='black', linewidth=1.5, alpha=0.8)

        # Add value labels
        for i, (bar, mean, std) in enumerate(zip(bars, means, stds)):
            ax.text(bar.get_x() + bar.get_width()/2, mean + std + 0.3,
                   f'{mean:.2f}\n(σ={std:.2f})', ha='center', va='bottom',
                   fontsize=9, fontweight='bold')

        ax.set_xticks(x)
        ax.set_xticklabels(tasks, rotation=20, ha='right')
        ax.set_title(model, fontsize=12, fontweight='bold')
        ax.set_ylim(0, 11)
        ax.grid(True, alpha=0.3, axis='y')

        # Add consistency interpretation
        for i, std in enumerate(stds):
            consistency = 'CONSISTENT' if std < 2.0 else 'VARIABLE'
            color = 'green' if std < 2.0 else 'orange'
            ax.text(i, 0.5, consistency, ha='center', fontsize=8,
                   fontweight='bold', color=color, rotation=90)

    ax1.set_ylabel('Score (0-10)', fontsize=12, fontweight='bold')

    fig.suptitle('Task-Adaptive Performance: Q&A vs Contract Drafting\n' +
                 'Error bars show standard deviation (consistency measure)',
                 fontsize=14, fontweight='bold', y=1.02)

    plt.tight_layout()

    output_path = FIGURES_DIR / "figure6_task_variance.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.savefig(FIGURES_DIR / "figure6_task_variance.pdf", bbox_inches='tight')

    plt.close()

#==============================================================================
# FIGURE 7: Success Factor Analysis (New Insight!)
#==============================================================================

def generate_figure7_success_factors():
    """Figure 7: What drives high scores? (Specificity vs Disclaimers)"""

    print("\n📊 Generating Figure 7: Success Factor Analysis...")

    # Data from deep dive
    success_factors = {
        'Specific + Actionable': 83.7,
        'Well-structured': 78.5,
        'Practical': 66.3,
        'Comprehensive': 51.7,
        'Appropriate Disclaimers': 1.7  # Only 1.7%!
    }

    labels = list(success_factors.keys())
    values = list(success_factors.values())

    # Color code: emphasize disclaimers
    colors = ['#2196F3', '#2196F3', '#2196F3', '#2196F3', '#F44336']

    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.barh(labels, values, color=colors, edgecolor='black', linewidth=2)

    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
               va='center', fontsize=11, fontweight='bold')

    ax.set_xlabel('Percentage of High-Score Justifications (%)', fontsize=12, fontweight='bold')
    ax.set_title('Success Factor Analysis: What Drives High Scores (8-10/10)?\n' +
                 'Abliterated Models (n=172 high-scoring responses)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 95)

    # Add legend
    legend_elements = [
        mpatches.Patch(color='#2196F3', label='Quality-Driven Success Factors', edgecolor='black'),
        mpatches.Patch(color='#F44336', label='Safety-Emphasized Factor (1.7%)', edgecolor='black')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11)

    # Add annotation
    ax.text(47, 0.3, 'Key Insight: Specificity (84%) drives success, not disclaimers (2%)\n' +
            'Safety training optimizes for the wrong quality dimension.',
            ha='center', fontsize=11, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow',
                     edgecolor='black', linewidth=2))

    plt.tight_layout()

    output_path = FIGURES_DIR / "figure7_success_factors.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.savefig(FIGURES_DIR / "figure7_success_factors.pdf", bbox_inches='tight')

    plt.close()

#==============================================================================
# FIGURE 8: Utility-Quality Tradeoff (Summary Visualization)
#==============================================================================

def generate_figure8_utility_quality_tradeoff():
    """Figure 8: The cost of safety over-calibration (summary)"""

    print("\n📊 Generating Figure 8: Utility-Quality Tradeoff...")

    fig, ax = plt.subplots(figsize=(12, 8))

    # Data points: (utility %, quality score, model name, is_abliterated)
    # Utility = 100 - refusal_rate
    data_points = [
        # Abliterated models (0% refusal = 100% utility)
        (100, 7.36, 'Gemma-abliterated', True),
        (100, 6.90, 'Qwen-abliterated', True),

        # Well-calibrated (low refusal)
        (62.5, 0, 'GLM-4.6', False),  # 37.5% refusal
        (54.2, 0, 'Mistral-123B', False),  # 45.8% refusal

        # Over-calibrated
        (41.7, 0, 'DeepSeek-R1', False),  # 58.3% refusal
        (37.5, 0, 'Gemma-2-27B-it', False),  # 62.5% refusal

        # Severely over-calibrated
        (8.3, 0, 'GPT-5/O3-Mini', False),  # 91.7% refusal
        (0, 0, 'GPT-OSS-120B', False),  # 100% refusal
    ]

    utilities = [d[0] for d in data_points]
    qualities = [d[1] for d in data_points]
    labels = [d[2] for d in data_points]
    is_abliterated = [d[3] for d in data_points]

    # Plot points
    for utility, quality, label, abliterated in data_points:
        if abliterated:
            ax.scatter(utility, quality, s=400, c='#00ff00', marker='*',
                      edgecolors='black', linewidths=2, zorder=5)
            ax.annotate(label, (utility, quality), xytext=(10, 10),
                       textcoords='offset points', fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle='round', facecolor='lightgreen', edgecolor='black'))
        else:
            # Standard models - quality unknown, show as question marks
            ax.scatter(utility, 5, s=200, c='#FF5722', marker='o',
                      edgecolors='black', linewidths=2, alpha=0.6, zorder=3)
            ax.annotate(f'{label}\n(Quality?)', (utility, 5), xytext=(0, -30),
                       textcoords='offset points', fontsize=8,
                       bbox=dict(boxstyle='round', facecolor='lightcoral',
                                edgecolor='black', alpha=0.7), ha='center')

    # Add reference lines
    ax.axhline(y=7.0, color='green', linestyle='--', linewidth=2, alpha=0.4, label='Good Quality (7.0)')
    ax.axvline(x=50, color='orange', linestyle='--', linewidth=2, alpha=0.4, label='50% Utility')

    # Shade regions
    ax.fill_between([0, 100], [0, 0], [7, 7], alpha=0.1, color='green', label='Acceptable Quality Range')
    ax.fill_between([0, 50], [0, 0], [10, 10], alpha=0.1, color='red', label='Low Utility Zone')

    ax.set_xlabel('Utility (% of questions answered)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Quality Score (0-10)', fontsize=13, fontweight='bold')
    ax.set_title('The Cost of Safety Over-Calibration:\nUtility vs Quality Tradeoff',
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xlim(-5, 105)
    ax.set_ylim(0, 10)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=10)

    # Add key insight box
    insight_text = ('Abliterated Models: 100% utility, 6.9-7.4/10 quality\n'
                   'Standard Models: 0-63% utility, quality unknown\n\n'
                   'Is unknown quality gain worth 37-100% utility loss?')
    ax.text(50, 1.5, insight_text, ha='center', fontsize=11, style='italic',
           bbox=dict(boxstyle='round', facecolor='lightyellow',
                    edgecolor='black', linewidth=2))

    plt.tight_layout()

    output_path = FIGURES_DIR / "figure8_utility_quality_tradeoff.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    plt.savefig(FIGURES_DIR / "figure8_utility_quality_tradeoff.pdf", bbox_inches='tight')

    plt.close()

#==============================================================================
# MAIN EXECUTION
#==============================================================================

def main():
    print("=" * 80)
    print("🎨 REGENERATING ALL FIGURES FOR LEGAL LLM BENCHMARK PAPER")
    print("=" * 80)
    print(f"\nOutput directory: {FIGURES_DIR}")
    print(f"Data sources:")
    print(f"  • FalseReject: {RESULTS_DIR / 'falsereject_analysis_with_abliterated.json'}")
    print(f"  • Phase 1: {RESULTS_DIR / 'phase1_final_with_abliterated_scored.json'}")
    print(f"  • Phase 2: {RESULTS_DIR / 'phase2_final_with_abliterated_scored.json'}")

    # Generate all figures
    try:
        generate_figure1_falsereject_rates()
        generate_figure2_tiered_rejection()
        generate_figure3_phase1_quality()
        generate_figure4_theme_distribution()
        generate_figure5_failure_patterns()
        generate_figure6_task_variance()
        generate_figure7_success_factors()
        generate_figure8_utility_quality_tradeoff()

        print("\n" + "=" * 80)
        print("✅ ALL FIGURES GENERATED SUCCESSFULLY!")
        print("=" * 80)
        print(f"\nTotal figures created: 8")
        print(f"Location: {FIGURES_DIR}")
        print("\nFigures:")
        print("  1. figure1_falsereject_refusal_rates.png/pdf")
        print("  2. figure2_tiered_rejection_rates.png/pdf")
        print("  3. figure3_phase1_quality_scores.png/pdf")
        print("  4. figure4_evaluation_themes.png/pdf (NEW!)")
        print("  5. figure5_failure_patterns.png/pdf (NEW!)")
        print("  6. figure6_task_variance.png/pdf (NEW!)")
        print("  7. figure7_success_factors.png/pdf (NEW!)")
        print("  8. figure8_utility_quality_tradeoff.png/pdf")
        print("\n✨ Ready for paper submission!")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error generating figures: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
