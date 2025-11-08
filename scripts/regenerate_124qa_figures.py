#!/usr/bin/env python3
"""
Regenerate Figures 1-5 with 124 Q&A Questions (Phase 1 + FalseReject)

This script creates updated figures using the complete non-file Q&A dataset:
- Phase 1: 100 questions
- FalseReject: 24 questions
- Total: 124 Q&A questions (NO file-based contract tasks)

Generates:
- figure1_model_boxplot.png
- figure2_rejection_rates.png
- figure3_category_heatmap.png
- figure4_score_distribution.png
- figure5_model_rankings.png (NEW - overall rankings for 124 Q&A)
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality plotting style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'


class QA124FigureGenerator:
    """Generate figures for 124 Q&A questions (Phase 1 + FalseReject)"""

    def __init__(self):
        self.output_dir = Path('reports/academic/figures_124qa')
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.models = [
            'anthropic/claude-sonnet-4.5',
            'openai/gpt-5',
            'openai/gpt-oss-120b',
            'google/gemini-2.5-flash',
            'x-ai/grok-4',
            'deepseek/deepseek-chat-v3-0324',
            'z-ai/glm-4.6',
            'openai/o3-mini',
            'mistralai/mistral-large',
            'qwen/qwen-2.5-72b-instruct'
        ]

        self.model_display_names = {
            'anthropic/claude-sonnet-4.5': 'Claude Sonnet 4.5',
            'openai/gpt-5': 'GPT-5',
            'openai/gpt-oss-120b': 'GPT-OSS-120B',
            'google/gemini-2.5-flash': 'Gemini 2.5 Flash',
            'x-ai/grok-4': 'Grok-4',
            'deepseek/deepseek-chat-v3-0324': 'DeepSeek v3',
            'z-ai/glm-4.6': 'GLM-4.6',
            'openai/o3-mini': 'O3-Mini',
            'mistralai/mistral-large': 'Mistral Large',
            'qwen/qwen-2.5-72b-instruct': 'Qwen 2.5 72B'
        }

    def load_data(self):
        """Load Phase 1 + FalseReject data"""
        print("📂 Loading 124 Q&A questions data...")

        # Load Phase 1
        with open('results/phase1_final.json', 'r') as f:
            phase1 = json.load(f)

        # Load FalseReject
        with open('results/falsereject_benchmark_final.json', 'r') as f:
            falsereject = json.load(f)

        # Combine questions with source tracking
        all_questions = []

        # Add Phase 1 questions (indices 0-99)
        for idx, q in enumerate(phase1.get('questions', [])):
            q['source'] = 'phase1'
            q['source_index'] = idx  # Store the original array index
            all_questions.append(q)

        # Add FalseReject questions (indices 0-23)
        for idx, q in enumerate(falsereject.get('questions', [])):
            q['source'] = 'falsereject'
            q['source_index'] = idx  # Store the original array index
            all_questions.append(q)

        print(f"   ✅ Phase 1: {len(phase1.get('questions', []))} questions")
        print(f"   ✅ FalseReject: {len(falsereject.get('questions', []))} questions")
        print(f"   ✅ Total: {len(all_questions)} Q&A questions")

        self.questions = all_questions

        # Load evaluation scores
        self.load_evaluations()

        return all_questions

    def load_evaluations(self):
        """Load OpenAI batch evaluation results"""
        print("\n📂 Loading evaluation scores...")

        eval_dir = Path('batch_evaluation_jobs/results')

        # Parse appropriateness
        self.appropriateness_scores = {}
        with open(eval_dir / 'appropriateness_results.jsonl', 'r') as f:
            for line in f:
                result = json.loads(line)
                custom_id = result['custom_id']
                try:
                    response_text = result['response']['body']['choices'][0]['message']['content']
                    score_data = json.loads(response_text)
                    self.appropriateness_scores[custom_id] = score_data
                except:
                    pass

        print(f"   ✅ Loaded {len(self.appropriateness_scores)} appropriateness scores")

    def extract_scores_dataframe(self):
        """Extract all scores into a DataFrame"""
        print("\n📊 Extracting scores into DataFrame...")

        data = []

        for question in self.questions:
            q_id = question['question_id']
            category = question.get('category', 'general')
            source = question.get('source', 'unknown')
            source_index = question.get('source_index', 0)

            for model, response_data in question.get('model_responses', {}).items():
                response = response_data.get('response', '')

                # Build correct custom_id based on source and index
                # Format: approp_phase1_qa_{index}_{model}_{suffix} or approp_falsereject_{index}_{model}_{suffix}
                if source == 'phase1':
                    custom_id_prefix = f"approp_phase1_qa_{source_index}_{model}"
                elif source == 'falsereject':
                    custom_id_prefix = f"approp_falsereject_{source_index}_{model}"
                else:
                    custom_id_prefix = None

                score = None
                refusal_type = None

                # Find matching custom_id (ends with _suffix number)
                if custom_id_prefix:
                    for custom_id in self.appropriateness_scores.keys():
                        if custom_id.startswith(custom_id_prefix):
                            score = self.appropriateness_scores[custom_id].get('appropriateness_score')
                            refusal_type = self.appropriateness_scores[custom_id].get('refusal_type', 'unknown')
                            break

                data.append({
                    'question_id': q_id,
                    'category': category,
                    'source': source,
                    'model': model,
                    'model_display': self.model_display_names.get(model, model),
                    'score': score,
                    'refusal_type': refusal_type,
                    'response_length': len(response)
                })

        self.df = pd.DataFrame(data)
        print(f"   ✅ Extracted {len(self.df)} score records")
        print(f"   ✅ Non-null scores: {self.df['score'].notna().sum()}")

        return self.df

    def figure1_model_boxplot(self):
        """Figure 1: Model Performance Boxplot Distribution"""
        print("\n🎨 Generating Figure 1: Model Boxplot...")

        fig, ax = plt.subplots(figsize=(12, 6))

        # Prepare data for boxplot
        data_for_plot = []
        labels = []

        for model in self.models:
            model_scores = self.df[self.df['model'] == model]['score'].dropna()
            if len(model_scores) > 0:
                data_for_plot.append(model_scores)
                labels.append(self.model_display_names.get(model, model))

        # Create boxplot
        bp = ax.boxplot(data_for_plot, labels=labels, patch_artist=True,
                       showmeans=True, meanline=True)

        # Color boxes
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(data_for_plot)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax.set_ylabel('Appropriateness Score (0-10)', fontsize=12)
        ax.set_xlabel('Model', fontsize=12)
        ax.set_title('Figure 1: Model Performance Distribution (124 Q&A Questions)',
                    fontweight='bold', fontsize=13, pad=15)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        output_file = self.output_dir / 'figure1_model_boxplot.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"   ✅ Saved: {output_file}")

    def figure2_rejection_rates(self):
        """Figure 2: Rejection/Refusal Rates by Model"""
        print("\n🎨 Generating Figure 2: Rejection Rates...")

        fig, ax = plt.subplots(figsize=(10, 6))

        # Calculate refusal rates
        refusal_data = []

        for model in self.models:
            model_df = self.df[self.df['model'] == model]
            total = len(model_df)

            hard_refusal = len(model_df[model_df['refusal_type'] == 'hard_refusal'])
            soft_refusal = len(model_df[model_df['refusal_type'] == 'soft_refusal'])

            refusal_rate = (hard_refusal + soft_refusal) / total * 100 if total > 0 else 0

            refusal_data.append({
                'model': self.model_display_names.get(model, model),
                'refusal_rate': refusal_rate,
                'hard': hard_refusal,
                'soft': soft_refusal,
                'total': total
            })

        refusal_df = pd.DataFrame(refusal_data).sort_values('refusal_rate')

        # Create horizontal bar chart
        colors = ['red' if x > 30 else 'orange' if x > 15 else 'green'
                 for x in refusal_df['refusal_rate']]

        y_pos = np.arange(len(refusal_df))
        ax.barh(y_pos, refusal_df['refusal_rate'], color=colors, alpha=0.7)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(refusal_df['model'])
        ax.invert_yaxis()
        ax.set_xlabel('Refusal Rate (%)', fontsize=12)
        ax.set_title('Figure 2: Model Refusal Rates (124 Q&A Questions)',
                    fontweight='bold', fontsize=13, pad=15)

        # Add threshold lines
        ax.axvline(x=15, color='orange', linestyle='--', alpha=0.3, label='Medium (15%)')
        ax.axvline(x=30, color='red', linestyle='--', alpha=0.3, label='High (30%)')
        ax.legend()
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        # Add value labels
        for i, (idx, row) in enumerate(refusal_df.iterrows()):
            ax.text(row['refusal_rate'] + 1, i, f"{row['refusal_rate']:.1f}%",
                   va='center', fontsize=9)

        plt.tight_layout()
        output_file = self.output_dir / 'figure2_rejection_rates.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"   ✅ Saved: {output_file}")

    def figure3_category_heatmap(self):
        """Figure 3: Category-Specific Performance Heatmap"""
        print("\n🎨 Generating Figure 3: Category Heatmap...")

        # Calculate average scores by model and category
        pivot_data = self.df.groupby(['model', 'category'])['score'].mean().unstack(fill_value=0)

        # Reorder models by overall performance
        model_means = pivot_data.mean(axis=1).sort_values(ascending=False)
        pivot_data = pivot_data.loc[model_means.index]

        # Rename models for display
        pivot_data.index = [self.model_display_names.get(m, m) for m in pivot_data.index]

        # Create heatmap - larger figure to accommodate many categories
        fig, ax = plt.subplots(figsize=(20, 8))

        sns.heatmap(pivot_data, annot=False, cmap='RdYlGn',
                   center=6, vmin=0, vmax=10, cbar_kws={'label': 'Appropriateness Score'},
                   linewidths=0.5, ax=ax)

        ax.set_ylabel('Model', fontsize=12)
        ax.set_xlabel('Legal Category', fontsize=12)
        ax.set_title('Figure 3: Model Performance by Legal Category (124 Q&A Questions)',
                    fontweight='bold', fontsize=13, pad=15)

        plt.xticks(rotation=90, ha='center', fontsize=8)
        plt.yticks(rotation=0)
        plt.tight_layout()

        output_file = self.output_dir / 'figure3_category_heatmap.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"   ✅ Saved: {output_file}")

    def figure4_score_distribution(self):
        """Figure 4: Overall Score Distribution"""
        print("\n🎨 Generating Figure 4: Score Distribution...")

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot histogram of all scores
        scores = self.df['score'].dropna()

        ax.hist(scores, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
        ax.axvline(scores.mean(), color='red', linestyle='--', linewidth=2,
                  label=f'Mean: {scores.mean():.2f}')
        ax.axvline(scores.median(), color='orange', linestyle='--', linewidth=2,
                  label=f'Median: {scores.median():.2f}')

        ax.set_xlabel('Appropriateness Score', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Figure 4: Overall Score Distribution (124 Q&A Questions)',
                    fontweight='bold', fontsize=13, pad=15)
        ax.legend()
        ax.grid(alpha=0.3, linestyle='--')

        plt.tight_layout()
        output_file = self.output_dir / 'figure4_score_distribution.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"   ✅ Saved: {output_file}")

    def figure5_model_rankings(self):
        """Figure 5: Overall Model Rankings (NEW)"""
        print("\n🎨 Generating Figure 5: Model Rankings...")

        # Calculate overall rankings
        rankings = []

        for model in self.models:
            model_scores = self.df[self.df['model'] == model]['score'].dropna()

            if len(model_scores) > 0:
                rankings.append({
                    'model': self.model_display_names.get(model, model),
                    'mean_score': model_scores.mean(),
                    'std': model_scores.std(),
                    'n': len(model_scores)
                })

        rankings_df = pd.DataFrame(rankings).sort_values('mean_score', ascending=False)

        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 7))

        y_pos = np.arange(len(rankings_df))
        colors = plt.cm.RdYlGn(rankings_df['mean_score'] / 10)

        bars = ax.barh(y_pos, rankings_df['mean_score'], color=colors, alpha=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(rankings_df['model'])
        ax.invert_yaxis()
        ax.set_xlabel('Mean Appropriateness Score (0-10)', fontsize=12)
        ax.set_title('Figure 5: Overall Model Rankings (124 Q&A Questions)',
                    fontweight='bold', fontsize=13, pad=15)
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        # Add value labels with confidence intervals
        for i, (idx, row) in enumerate(rankings_df.iterrows()):
            ci = 1.96 * row['std'] / np.sqrt(row['n'])  # 95% CI
            ax.text(row['mean_score'] + 0.15, i,
                   f"{row['mean_score']:.2f} ± {ci:.2f}",
                   va='center', fontsize=9)

        plt.tight_layout()
        output_file = self.output_dir / 'figure5_model_rankings.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"   ✅ Saved: {output_file}")

        return rankings_df

    def generate_all_figures(self):
        """Generate all 5 figures"""
        print("\n" + "=" * 70)
        print("🎨 GENERATING 5 FIGURES FOR 124 Q&A QUESTIONS")
        print("=" * 70)

        self.figure1_model_boxplot()
        self.figure2_rejection_rates()
        self.figure3_category_heatmap()
        self.figure4_score_distribution()
        rankings = self.figure5_model_rankings()

        print("\n" + "=" * 70)
        print("✅ ALL FIGURES GENERATED!")
        print("=" * 70)
        print(f"\n📁 Output directory: {self.output_dir}/")
        print("\nGenerated figures:")
        print("  1. figure1_model_boxplot.png - Performance distributions")
        print("  2. figure2_rejection_rates.png - Refusal rate analysis")
        print("  3. figure3_category_heatmap.png - Category-specific performance")
        print("  4. figure4_score_distribution.png - Overall score histogram")
        print("  5. figure5_model_rankings.png - Overall rankings with CI")

        print("\n📊 Top 3 Models (124 Q&A Questions):")
        for i, (idx, row) in enumerate(rankings.head(3).iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            print(f"  {medal} {row['model']}: {row['mean_score']:.2f}/10 (n={int(row['n'])})")

        return rankings


def main():
    """Main execution"""
    print("=" * 70)
    print("📊 REGENERATE FIGURES 1-5 WITH 124 Q&A QUESTIONS")
    print("=" * 70)
    print("\nData sources:")
    print("  • Phase 1: 100 Q&A questions (no files)")
    print("  • FalseReject: 24 Q&A questions (over-refusal test)")
    print("  • Total: 124 Q&A questions")
    print("\n" + "=" * 70)

    generator = QA124FigureGenerator()

    # Load data
    generator.load_data()

    # Extract scores
    generator.extract_scores_dataframe()

    # Generate all figures
    rankings = generator.generate_all_figures()

    print("\n" + "=" * 70)
    print("✅ COMPLETE!")
    print("=" * 70)
    print("\nNext step: Copy figures to paper package:")
    print("  cp reports/academic/figures_124qa/*.png reports/paper/overleaf/figures/")
    print("=" * 70)


if __name__ == "__main__":
    main()
