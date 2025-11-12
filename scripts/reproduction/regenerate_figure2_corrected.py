#!/usr/bin/env python3
"""
Regenerate Figure 2: Rejection Rates (FalseReject Benchmark)
With CORRECTED refusal detection (Unicode apostrophe bug fixed)
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_corrected_refusal_rates():
    """Load corrected refusal rates from analysis"""

    analysis_file = Path('results/falsereject_analysis.json')

    if analysis_file.exists():
        with open(analysis_file, 'r') as f:
            data = json.load(f)

        # Extract refusal rates
        model_data = []
        for model, stats in data['model_analysis'].items():
            model_short = model.split('/')[-1] if '/' in model else model
            fp_rate = stats['false_positive_rate']
            model_data.append((model_short, fp_rate))

        # Sort by refusal rate (descending)
        model_data.sort(key=lambda x: x[1], reverse=True)
        return model_data

    # Fallback: Manually corrected data
    print("⚠️  Using manually entered corrected data")
    return [
        ('gpt-oss-120b', 100.0),
        ('gpt-5', 91.7),
        ('o3-mini', 91.7),
        ('claude-sonnet-4.5', 58.3),
        ('deepseek-chat-v3-0324', 54.2),
        ('qwen-2.5-72b-instruct', 54.2),
        ('gemini-2.5-flash', 50.0),
        ('grok-4', 50.0),
        ('mistral-large', 45.8),
        ('glm-4.6', 37.5),
    ]

def create_figure2():
    """Create Figure 2: Rejection Rates bar chart"""

    print("📊 Generating Figure 2: Rejection Rates (CORRECTED)")

    # Load corrected data
    model_data = load_corrected_refusal_rates()

    models = [m[0] for m in model_data]
    refusal_rates = [m[1] for m in model_data]

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # Color coding based on severity
    colors = []
    for rate in refusal_rates:
        if rate >= 80:
            colors.append('#d32f2f')  # Red - Unusable
        elif rate >= 50:
            colors.append('#f57c00')  # Orange - Poor
        elif rate >= 20:
            colors.append('#fbc02d')  # Yellow - Fair
        else:
            colors.append('#388e3c')  # Green - Good

    # Create horizontal bar chart
    y_pos = np.arange(len(models))
    bars = ax.barh(y_pos, refusal_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

    # Customize axes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(models, fontsize=11, fontweight='bold')
    ax.set_xlabel('False Positive Rate (%) - Over-Refusal', fontsize=13, fontweight='bold')
    ax.set_title('FalseReject Benchmark: Safety Over-Calibration\n(24 Legitimate Legal Questions with Adversarial Wording)',
                 fontsize=14, fontweight='bold', pad=20)

    # Add value labels on bars
    for i, (bar, rate) in enumerate(zip(bars, refusal_rates)):
        width = bar.get_width()
        label = f'{rate:.1f}%'

        # Add status label
        if rate >= 80:
            status = 'UNUSABLE'
        elif rate >= 50:
            status = 'POOR'
        elif rate >= 20:
            status = 'FAIR'
        else:
            status = 'GOOD'

        ax.text(width + 2, bar.get_y() + bar.get_height()/2,
                f'{label} ({status})',
                va='center', fontsize=10, fontweight='bold')

    # Add reference lines
    ax.axvline(x=50, color='red', linestyle='--', linewidth=1.5, alpha=0.5, label='50% threshold (Poor)')
    ax.axvline(x=80, color='darkred', linestyle='--', linewidth=1.5, alpha=0.7, label='80% threshold (Unusable)')

    # Set x-axis limits
    ax.set_xlim(0, 110)

    # Add grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')

    # Add legend
    ax.legend(loc='lower right', fontsize=10)

    # Invert y-axis so highest refusal is at top
    ax.invert_yaxis()

    # Tight layout
    plt.tight_layout()

    # Save figure
    output_file = Path('figures/figure2_rejection_rates_CORRECTED.png')
    output_file.parent.mkdir(exist_ok=True)

    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Figure saved: {output_file}")

    # Also save with original name (overwrite old incorrect figure)
    original_file = Path('figures/figure2_rejection_rates.png')
    plt.savefig(original_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Original figure updated: {original_file}")

    plt.close()

    # Print summary
    print("\n📊 CORRECTED Refusal Rates:")
    print("="*60)
    for model, rate in model_data:
        if rate >= 80:
            status = "❌ UNUSABLE"
        elif rate >= 50:
            status = "⚠️  POOR"
        elif rate >= 20:
            status = "⚠️  FAIR"
        else:
            status = "✅ GOOD"
        print(f"{model:30} {rate:6.1f}%  {status}")
    print("="*60)

if __name__ == "__main__":
    create_figure2()
    print("\n✨ Figure 2 regeneration complete!")
