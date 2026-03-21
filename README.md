# GEPA Prompt Optimization Pipeline

A comprehensive automated prompt optimization system using the **GEPA (General-Purpose Prompt Optimizer)** framework. This pipeline iteratively improves natural language prompts for mathematical reasoning tasks through intelligent evaluation and reflection-based prompt generation.

## 📋 Project Overview

This project provides an end-to-end pipeline for optimizing prompts used by language models on problem-solving tasks. The system:

- **Analyzes datasets** to understand task characteristics (token counts, complexity, distributions)
- **Optimizes prompts** through iterative refinement using GEPA's multi-candidate approach
- **Generates reports** with detailed metrics and before/after comparisons
- **Manages execution** via shell scripts and Python modules with configurable settings

### Key Characteristics

- **Local-first inference**: Uses Ollama for local model execution (no cloud API calls required by default)
- **Configurable models**: Support for multiple language models via LiteLLM integration
- **Type-safe**: Full Python type hints and Pydantic validation
- **Modular design**: Separated concerns for data analysis, optimization, and reporting
- **Comprehensive logging**: Pipeline execution is logged with timestamps and detailed output

## 🏗️ Project Structure

```
prompt_gepa/
├── src/
│   ├── constants.py          # Configuration constants and paths
│   ├── data_analysis.py      # Dataset statistics and analysis
│   └── optimization.py       # Main optimization pipeline using GEPA
│
├── data/
│   ├── train.csv            # Training dataset (15 examples)
│   ├── test.csv             # Test dataset (10 examples)
│   └── seed_prompt.txt      # Initial prompt template
│
├── reports/
│   ├── data_analysis_report.txt     # Dataset analysis output
│   └── optimization_report.txt      # Optimization results
│
├── pipeline.sh              # Main execution script
├── pyproject.toml           # Project dependencies and metadata
├── uv.lock                  # Locked dependency versions
└── README.md                # This file
```

## 🎯 Features

### 1. Data Analysis Module (`src/data_analysis.py`)

Analyzes input/output datasets to generate detailed statistics:

- **Per-split metrics**: Examples count, character/token ranges, averages
- **Token estimation**: Rough 4-char-per-token heuristic for prompt sizing
- **Sample inspection**: First 3 examples from each split for manual review
- **Combined statistics**: Aggregated metrics across train/test splits

**Output**: `reports/data_analysis_report.txt`

### 2. Optimization Module (`src/optimization.py`)

Runs the GEPA optimization framework to improve prompts:

- **Dual LM architecture**:
  - Task LM: Evaluates prompt quality on test samples
  - Reflection LM: Generates improved prompt variations
- **Budget-constrained**: Configurable maximum number of LM calls
- **Train/val split**: Trains on subset, validates on held-out data
- **Metric tracking**: Logs improvement metrics throughout optimization

**Output**: `reports/optimization_report.txt`

### 3. Pipeline Script (`pipeline.sh`)

Orchestrates execution with options for:

- Standalone data analysis: `./pipeline.sh --analysis`
- Standalone optimization: `./pipeline.sh --optimization`
- Full pipeline: `./pipeline.sh --all` (default)

Features:
- Automatic virtual environment creation with `uv`
- Dependency synchronization
- Timestamped logging of all operations
- Exit on error with descriptive messages

## 📦 Dependencies

### Core Runtime Dependencies

```toml
gepa>=0.1.0              # Prompt optimization framework
pydantic>=2.0.0          # Data validation
litellm>=1.0.0           # LLM provider abstraction
openai>=1.3.0            # OpenAI SDK (for API-based models)
requests>=2.31.0         # HTTP library
tqdm>=4.65.0             # Progress bars
colorama>=0.4.6          # Colored terminal output
```

### Development Dependencies (optional)

```toml
python-dotenv>=1.0.0     # Environment variable management
pytest>=7.0.0            # Testing framework
black>=23.0.0            # Code formatter
flake8>=6.0.0            # Linter
mypy>=1.0.0              # Static type checker
```

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.10 or higher
- **uv**: Package manager and virtual environment tool
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Ollama** (for local inference, optional):
  - Install: `https://ollama.ai`
  - Run: `ollama serve` in a separate terminal
  - Pull models:
    ```bash
    ollama pull qwen2.5:7b
    ollama pull qwen2.5:72b
    ```

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd prompt_gepa
   ```

2. **Create and activate virtual environment**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Configure environment** (if using OpenAI API)
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   # Or create a .env file:
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

## 💻 Usage

### Run Full Pipeline

```bash
./pipeline.sh
```

Outputs:
- `reports/data_analysis_report.txt` - Dataset analysis
- `reports/optimization_report.txt` - Optimization results with best prompt

### Run Data Analysis Only

```bash
./pipeline.sh --analysis
```

Generates dataset statistics without running optimization.

### Run Optimization Only

```bash
./pipeline.sh --optimization
```

Runs prompt optimization on the dataset.

### Manual Execution (Python)

Run individual modules directly:

```bash
# Data analysis
python src/data_analysis.py

# Optimization
python src/optimization.py
```

## ⚙️ Configuration

Edit `src/constants.py` to customize the pipeline:

```python
# Language models (default: Ollama-based)
TASK_LM = "ollama/qwen3:1.7b"      # Model for evaluation
REFLECTION_LM = "ollama/qwen3:8b"   # Model for improvement

# Ollama server
OLLAMA_HOST = "http://localhost:11434"

# Optimization settings
MAX_METRIC_CALLS = 100    # Budget: max LM calls
VAL_SPLIT = 0.2           # Validation set fraction (20%)

# Can also use OpenAI:
# TASK_LM = "openai/gpt-4-turbo"
# REFLECTION_LM = "openai/gpt-4"
```

## 📊 Output Examples

### Data Analysis Report

```
======================================================================
GEPA PROMPT OPTIMIZATION — DATA ANALYSIS REPORT
Generated: 2026-03-21 22:30:45
======================================================================

TRAIN SET
  Examples: 15
  Input length: min=20 max=156 avg=68.5 chars
  Output length: min=4 max=25 avg=12.3 chars
  Avg input tokens: 17.1
  Avg output tokens: 3.1
  Total tokens: 301
  
[Sample examples...]
```

### Optimization Report

```
======================================================================
GEPA PROMPT OPTIMIZATION — RESULTS REPORT
Generated: 2026-03-21 22:35:12
Elapsed: 42.3s
======================================================================

SEED PROMPT
[Initial prompt...]

OPTIMIZED PROMPT
[Improved prompt...]

CONFIGURATION
  task_lm: ollama/qwen3:1.7b
  reflection_lm: ollama/qwen3:8b
  max_metric_calls: 100
```

## 🔧 Development

### Code Formatting

Format code with Black:

```bash
python -m black src/
```

### Type Checking

Run mypy for static type analysis:

```bash
python -m mypy src/
```

### Linting

Check code quality with flake8:

```bash
python -m flake8 src/
```

### Running Tests

```bash
pytest
```

(Test files can be added in a `tests/` directory)

## 🌐 Model Options

### Local Inference (Ollama)

Free, fully local, no API keys needed:

```python
TASK_LM = "ollama/qwen2.5:7b"
REFLECTION_LM = "ollama/qwen2.5:72b"
```

### OpenAI API

High-quality commercial models:

```python
TASK_LM = "openai/gpt-4-mini"
REFLECTION_LM = "openai/gpt-4-turbo"
```

Requires: `OPENAI_API_KEY` environment variable

### Other Providers (via LiteLLM)

Anthropic, Google, Cohere, etc. See [LiteLLM documentation](https://litellm.ai/).

## 📝 Environment Variables

- `OLLAMA_HOST`: Ollama server URL (default: `http://localhost:11434`)
- `OPENAI_API_KEY`: OpenAI API key (if using OpenAI models)

Create a `.env` file to manage these:

```bash
OLLAMA_HOST=http://localhost:11434
OPENAI_API_KEY=sk-...
```

Then load with: `source .env` or install `python-dotenv`

## 🐛 Troubleshooting

### Error: "gepa not installed"

```bash
uv sync
```

### Error: "Connection refused" (Ollama)

Ensure Ollama is running:

```bash
ollama serve  # In a separate terminal
```

### Error: "Module not found"

Verify virtual environment is activated:

```bash
source .venv/bin/activate
```

Or use `uv run`:

```bash
uv run python src/data_analysis.py
```

## 📚 Additional Resources

- [GEPA Documentation](https://github.com/stanfordchen/gepa)
- [Ollama Documentation](https://ollama.ai)
- [LiteLLM Documentation](https://litellm.ai/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📄 License

This project is provided as-is for research and educational purposes.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes with clear messages
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

For issues, questions, or suggestions, please open an GitHub issue or contact the maintainers.

---

**Last Updated**: March 21, 2026  
**Version**: 0.1.0
