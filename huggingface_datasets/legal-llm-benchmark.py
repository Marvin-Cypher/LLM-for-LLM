"""Legal LLM Benchmark Dataset - HuggingFace Dataset Loading Script"""

import json
import datasets

_CITATION = """\
@article{legal-llm-safety-2025,
  title={Safety-Utility Trade-offs in Legal AI: An LLM Evaluation Across 12 Models},
  author={[Your Name]},
  journal={arXiv preprint arXiv:2501.XXXXX},
  year={2025},
  url={https://github.com/marvintong/legal-llm-benchmark}
}
"""

_DESCRIPTION = """\
Legal LLM Benchmark: Evaluating 12 Large Language Models across 163 legal tasks.

This benchmark measures the critical safety-utility tradeoff in production AI systems,
revealing a safety paradox: safety-trained models achieve 87% higher quality but 58%
higher refusal rates. Two widely-used models refuse 87-96% of legitimate legal questions.

The dataset is organized into 3 tiers:
- TIER 1: Questions only (163 legal tasks)
- TIER 2: Responses (1,908 model responses)
- TIER 3: Evaluations (1,956 scored responses with refusal labels)

Key findings:
- Human validation: Cohen's κ=0.91 [95% CI: 0.84, 0.98]
- Statistical rigor: ANOVA F=142.3, η²=0.93; Spearman ρ=0.82
- Catastrophic over-refusal documented in GPT-OSS-120B (95.8%) and O3-Mini (87.5%)
"""

_HOMEPAGE = "https://github.com/marvintong/legal-llm-benchmark"
_LICENSE = "MIT"

_URLS = {
    # TIER 1: Questions
    "phase1_questions": "1_questions_phase1.json",
    "phase2_questions": "1_questions_phase2.json",
    "phase3_questions": "1_questions_phase3.json",

    # TIER 2: Responses
    "phase1_responses": "2_responses_phase1.json",
    "phase2_responses": "2_responses_phase2.json",
    "phase3_responses": "2_responses_phase3.json",

    # TIER 3: Evaluations
    "phase1_evaluations": "3_evaluations_phase1.json",
    "phase2_evaluations": "3_evaluations_phase2.json",
    "phase3_evaluations": "3_evaluations_phase3.json",
}

class LegalLLMBenchmark(datasets.GeneratorBasedBuilder):
    """Legal LLM Benchmark Dataset"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="phase1_questions",
            version=VERSION,
            description="Phase 1: 100 legal Q&A questions (TIER 1 - Questions Only)"
        ),
        datasets.BuilderConfig(
            name="phase2_questions",
            version=VERSION,
            description="Phase 2: 39 contract analysis tasks (TIER 1 - Questions Only)"
        ),
        datasets.BuilderConfig(
            name="phase3_questions",
            version=VERSION,
            description="Phase 3: 24 FalseReject adversarial questions (TIER 1 - Questions Only)"
        ),
        datasets.BuilderConfig(
            name="phase1_evaluations",
            version=VERSION,
            description="Phase 1: 100 Q&A with 12 model responses + evaluations (TIER 3)"
        ),
        datasets.BuilderConfig(
            name="phase3_evaluations",
            version=VERSION,
            description="Phase 3: 24 FalseReject with model responses + refusal labels (TIER 3)"
        ),
    ]

    DEFAULT_CONFIG_NAME = "phase1_evaluations"

    def _info(self):
        if self.config.name in ["phase1_questions", "phase2_questions", "phase3_questions"]:
            # TIER 1: Questions only
            features = datasets.Features({
                "id": datasets.Value("string"),
                "question": datasets.Value("string"),
                "category": datasets.Value("string"),
                "difficulty": datasets.Value("string"),
            })
        else:
            # TIER 3: Evaluations (simplified schema for viewer)
            features = datasets.Features({
                "question_id": datasets.Value("string"),
                "question": datasets.Value("string"),
                "category": datasets.Value("string"),
                "model_responses": datasets.Value("string"),  # JSON string
            })

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        url = _URLS[self.config.name]
        filepath = dl_manager.download(url)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": filepath},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        if self.config.name in ["phase1_questions", "phase2_questions", "phase3_questions"]:
            # TIER 1: Questions only
            questions = data.get("questions", data)  # Handle both formats
            for idx, question in enumerate(questions):
                yield idx, {
                    "id": question.get("id", str(idx)),
                    "question": question.get("question", ""),
                    "category": question.get("category", ""),
                    "difficulty": question.get("difficulty", ""),
                }
        else:
            # TIER 3: Evaluations (flatten model_responses for viewer)
            questions = data.get("questions", [])
            for idx, question in enumerate(questions):
                yield idx, {
                    "question_id": question.get("question_id", str(idx)),
                    "question": question.get("question", ""),
                    "category": question.get("category", ""),
                    "model_responses": json.dumps(question.get("model_responses", {})),
                }
