# Contributing to Legal LLM Benchmark

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Ways to Contribute

- 🐛 **Report bugs** via [GitHub Issues](https://github.com/YOUR_USERNAME/legal-llm-benchmark/issues)
- 📝 **Improve documentation** (README, code comments, guides)
- 🚀 **Add new models** to the benchmark
- 📊 **Contribute legal questions** to expand coverage
- 🔬 **Suggest evaluation improvements** 
- 🎨 **Enhance visualizations**

## Getting Started

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests (if applicable)
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Open a Pull Request

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and under 50 lines when possible

## Adding New Models

To add a new model to the benchmark:

1. Add model configuration to `config/models.yaml`
2. Implement API wrapper if needed in `src/models/`
3. Test with a small subset of questions
4. Submit PR with results

## Adding Legal Questions

When contributing new legal questions:

1. Ensure questions are appropriate (no real client data)
2. Categorize correctly (see existing categories in `data/`)
3. Provide expected answer characteristics
4. Test with 2-3 models before submitting

## Pull Request Process

1. Update the README.md with details of changes (if applicable)
2. Update requirements.txt if you add new dependencies
3. Your PR should pass all checks
4. Maintainers will review within 1 week

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on collaboration over competition
- No discrimination or harassment

## Questions?

Feel free to open an issue for questions or join discussions!

---

Thank you for contributing! 🙏
