#!/usr/bin/env python3
"""
Regenerate FalseReject figures with all 12 models (10 standard + 2 abliterated)
This shows the dramatic 0% refusal rate for abliterated models vs 37-100% for standard models
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
FIGURES_DIR = BASE_DIR / "reports" / "paper" / "overleaf" / "figures"

# Color scheme
COLORS = {
    'abliterated': '#00C853',  # Bright green for 0% refusal
    'good': '#4CAF50',          # Green for <20%
    'fair': '#FFC107',          # Yellow for 20-50%
    'poor': '#FF9800',          # Orange for 50-80%
    'unusable': '#F44336'       # Red for >80%
}

def load_data():
    """Load FalseReject analysis with abliterated models"""
    analysis_file = BASE_DIR / "results" / "falsereject_analysis_with_abliterated.json"
    with open(analysis_file, 'r') as f:
        return json.load(f)

def clean_model_name(model_name):
    """Clean model name for display"""
    name = model_name.replace('anthropic/', '').replace('openai/', '')
    name = name.replace('google/', '').replace('x-ai/', '')
    name = name.replace('deepseek/', '').replace('z-ai/', '')
    name = name.replace('mistralai/', '').replace('qwen/', '')

    # Capitalize and format
    if name.startswith('gpt-'):
        name = name.upper()
    elif name.startswith('claude'):
        name = 'Claude Sonnet 4.5'
    elif name.startswith('gemini'):
        name = 'Gemini 2.5 Flash'
    elif name.startswith('grok'):
        name = 'Grok-4'
    elif name.startswith('deepseek'):
        name = 'DeepSeek v3'
    elif name.startswith('glm'):
        name = name.upper()
    elif name.startswith('qwen-'):
        name = 'Qwen 2.5 72B'
    elif name.startswith('qwen3-vl'):
        name = 'Qwen3-VL (Abliterated)'
    elif name.startswith('gemma3'):
        name = 'Gemma3 (Abliterated)'
    elif 'mistral' in name.lower():
        name = 'Mistral Large'
    elif name.startswith('o3-'):
        name = name.upper()

    return name

def get_color_for_rate(rate, is_abliterated=False):
    """Get color based on refusal rate"""
    if is_abliterated:
        return COLORS['abliterated']
    elif rate < 20:
        return COLORS['good']
    elif rate < 50:
        return COLORS['fair']
    elif rate < 80:
        return COLORS['poor']
    else:
        return COLORS['unusable']

def generate_refusal_rates_bar_chart(data):
    """Generate main FalseReject refusal rates bar chart"""
    print("\n📊 Generating refusal rates bar chart...")

    # Sort models by refusal rate (descending)
    models_sorted = sorted(
        data['model_analysis'].items(),
        key=lambda x: x[1]['false_positive_rate'],
        reverse=True
    )

    model_names = [clean_model_name(m[0]) for m in models_sorted]
    refusal_rates = [m[1]['false_positive_rate'] for m in models_sorted]
    is_abliterated = [m[1].get('is_abliterated', False) for m in models_sorted]
    colors = [get_color_for_rate(rate, abl) for rate, abl in zip(refusal_rates, is_abliterated)]

    # Create figure
    plt.figure(figsize=(14, 8))
    bars = plt.barh(model_names, refusal_rates, color=colors, edgecolor='black', linewidth=0.5)

    # Add value labels
    for i, (bar, rate) in enumerate(zip(bars, refusal_rates)):
        label = f'{rate:.1f}%'
        if is_abliterated[i]:
            label += ' ✓'
        plt.text(rate + 1, bar.get_y() + bar.get_height()/2, label,
                va='center', fontsize=10, fontweight='bold')

    plt.xlabel('Over-Refusal Rate (%)', fontsize=12, fontweight='bold')
    plt.ylabel('Model', fontsize=12, fontweight='bold')
    plt.title('FalseReject Benchmark: Over-Refusal Rates on Legitimate Legal Questions\n(Lower is Better - 12 Models Including Abliterated)',
              fontsize=14, fontweight='bold', pad=20)

    # Add reference lines
    plt.axvline(x=20, color='gray', linestyle='--', alpha=0.3, linewidth=1)
    plt.axvline(x=50, color='gray', linestyle='--', alpha=0.3, linewidth=1)
    plt.axvline(x=80, color='gray', linestyle='--', alpha=0.3, linewidth=1)

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS['abliterated'], edgecolor='black', label='Abliterated (0%)'),
        Patch(facecolor=COLORS['good'], edgecolor='black', label='Good (<20%)'),
        Patch(facecolor=COLORS['fair'], edgecolor='black', label='Fair (20-50%)'),
        Patch(facecolor=COLORS['poor'], edgecolor='black', label='Poor (50-80%)'),
        Patch(facecolor=COLORS['unusable'], edgecolor='black', label='Unusable (>80%)')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=10)

    plt.xlim(0, 105)
    plt.grid(axis='x', alpha=0.3, linestyle=':', linewidth=0.5)
    plt.tight_layout()

    output_file = FIGURES_DIR / "falsereject_analysis.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_file}")
    plt.close()

def generate_rejection_comparison(data):
    """Generate Figure 2 - Rejection rates comparison (grouped by tier)"""
    print("\n📊 Generating Figure 2 - Rejection rates comparison...")

    # Group models by tier
    abliterated_models = []
    good_models = []
    moderate_models = []
    severe_models = []

    for model_name, stats in data['model_analysis'].items():
        rate = stats['false_positive_rate']
        clean_name = clean_model_name(model_name)

        if stats.get('is_abliterated', False):
            abliterated_models.append((clean_name, rate))
        elif rate < 40:
            good_models.append((clean_name, rate))
        elif rate < 60:
            moderate_models.append((clean_name, rate))
        else:
            severe_models.append((clean_name, rate))

    # Sort each tier
    abliterated_models.sort(key=lambda x: x[1])
    good_models.sort(key=lambda x: x[1])
    moderate_models.sort(key=lambda x: x[1])
    severe_models.sort(key=lambda x: x[1])

    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(14, 10))

    y_pos = 0
    all_positions = []
    all_names = []
    all_rates = []
    all_colors = []

    def add_tier(models, color, tier_name):
        nonlocal y_pos
        if not models:
            return

        # Add tier label
        y_pos += 1

        for name, rate in models:
            all_positions.append(y_pos)
            all_names.append(name)
            all_rates.append(rate)
            all_colors.append(color)
            y_pos += 1

        y_pos += 0.5  # Gap between tiers

    # Add tiers from bottom to top
    add_tier(severe_models, COLORS['unusable'], 'Severe')
    add_tier(moderate_models, COLORS['poor'], 'Moderate')
    add_tier(good_models, COLORS['fair'], 'Good')
    add_tier(abliterated_models, COLORS['abliterated'], 'Abliterated')

    # Create bars
    bars = ax.barh(all_positions, all_rates, color=all_colors, edgecolor='black', linewidth=0.5)

    # Add value labels
    for pos, rate, is_abl in zip(all_positions, all_rates,
                                  [n.endswith('(Abliterated)') for n in all_names]):
        label = f'{rate:.1f}%'
        if is_abl:
            label += ' ✓'
        ax.text(rate + 1, pos, label, va='center', fontsize=9, fontweight='bold')

    ax.set_yticks(all_positions)
    ax.set_yticklabels(all_names, fontsize=10)
    ax.set_xlabel('Over-Refusal Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Model Safety Calibration Tiers\n(FalseReject Benchmark - 24 Legitimate Legal Questions)',
                 fontsize=14, fontweight='bold', pad=20)

    # Add tier labels on left
    tier_positions = {
        'Abliterated\n(No Safety)': (all_positions[0] + all_positions[len(abliterated_models)-1]) / 2 if abliterated_models else 0,
        'Well-Calibrated': (all_positions[len(abliterated_models)] + all_positions[len(abliterated_models)+len(good_models)-1]) / 2 if good_models else 0,
        'Over-Calibrated': (all_positions[len(abliterated_models)+len(good_models)] + all_positions[len(abliterated_models)+len(good_models)+len(moderate_models)-1]) / 2 if moderate_models else 0,
        'Severely\nOver-Calibrated': (all_positions[-len(severe_models)] + all_positions[-1]) / 2 if severe_models else 0,
    }

    ax.set_xlim(0, 105)
    ax.grid(axis='x', alpha=0.3, linestyle=':', linewidth=0.5)
    plt.tight_layout()

    output_file = FIGURES_DIR / "figure2_rejection_rates.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_file}")
    plt.close()

def main():
    print("=" * 80)
    print("REGENERATING FALSEREJECT FIGURES WITH 12 MODELS")
    print("=" * 80)

    # Load data
    print("\n📂 Loading data...")
    data = load_data()
    print(f"   Models: {len(data['model_analysis'])}")
    print(f"   Questions: {data['metadata']['total_questions']}")

    # Count abliterated models
    abliterated_count = sum(1 for m in data['model_analysis'].values() if m.get('is_abliterated', False))
    print(f"   Abliterated models: {abliterated_count}")

    # Generate figures
    generate_refusal_rates_bar_chart(data)
    generate_rejection_comparison(data)

    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    print(f"\nGenerated 2 figures:")
    print(f"  • falsereject_analysis.png - Main bar chart with all 12 models")
    print(f"  • figure2_rejection_rates.png - Tiered comparison")
    print("\nKey findings now visible in figures:")
    print("  • Abliterated models: 0% over-refusal (perfect utility)")
    print("  • Best standard models: 37-46% over-refusal")
    print("  • Worst standard models: 91-100% over-refusal")
    print("=" * 80)

if __name__ == "__main__":
    main()
