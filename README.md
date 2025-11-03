# 🤖 AI Code Review Agent

> Automated code analysis powered by GPT-4, LangChain & LangGraph

Transform your GitHub repositories into comprehensive code review reports with AI-driven insights on security, performance, bugs, and code quality.

## ✨ Features

- 🔍 **Deep Code Analysis** - Security vulnerabilities, bugs, performance issues
- 🏗️ **Architecture Review** - Design patterns and structural improvements
- 📊 **Quality Metrics** - Production-readiness assessment with severity ratings
- 💡 **Smart Suggestions** - Actionable enhancement recommendations
- 📝 **Documentation Audit** - README and API documentation quality check
- 💰 **Cost Estimation** - Preview analysis cost before running

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd code-review-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env
echo "MODEL_NAME=gpt-4o-mini" >> .env
echo "TEMPERATURE=0.1" >> .env
echo "MAX_TOKENS=16000" >> .env
```

## 📖 Usage

### Option 1: Web Interface (Streamlit)

Launch the interactive web app:

```bash
streamlit run app.py
```

1. Enter a GitHub repository URL
2. Click **"Estimate Cost"** to preview analysis cost
3. Click **"Confirm & Analyze"** to run the review
4. Download the generated markdown report

### Option 2: Command Line

Run analysis directly from terminal:

```bash
python -m Src.main https://github.com/username/repository
```

## 📋 Sample Output

The agent generates a comprehensive markdown report including:

- **Executive Summary** - Overall quality score and production readiness
- **Project Understanding** - Tech stack, features, and use cases
- **Security Issues** - Vulnerabilities with severity ratings
- **Bug Detection** - Logic errors and potential crashes
- **Performance Analysis** - Optimization opportunities
- **Code Quality** - Maintainability and best practices
- **Enhancement Suggestions** - Prioritized improvements

## 🛠️ Configuration

Customize analysis settings in `config.yaml`:

```yaml
review:
  supported_extensions: ['.py', '.js', '.java', '.ts', ...]
  ignore_patterns: ['node_modules/', '__pycache__/', ...]
  max_files: 100
```

## 💡 Example

```bash
# Analyze a repository
streamlit run app.py

# Or via CLI
python -m Src.main https://github.com/facebook/react
```

**Output**: Detailed markdown report with 200+ insights across security, performance, and code quality.

## 🧹 Cleanup

The agent automatically manages temporary repositories. Manual cleanup:

```python
from Src.tools import GitHubTools

github = GitHubTools()
github.cleanup_repository("/path/to/cloned/repo")
```

## 📦 Project Structure

```
├── app.py                  # Streamlit web interface
├── Src/
│   ├── agents/            # LangGraph workflow orchestration
│   ├── tools/             # GitHub, file scanner, LLM tools
│   ├── utils/             # Config, logging, report formatting
│   └── prompts/           # GPT-4 prompt templates
├── config.yaml            # Analysis configuration
└── .env                   # API keys (not tracked)
```

## 🔒 Privacy & Security

- Repositories are cloned temporarily and deleted after analysis
- No code is stored or transmitted beyond OpenAI API
- API keys are never logged or exposed

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Support for more programming languages
- Integration with CI/CD pipelines
- Custom rule configuration
- Multi-repository batch analysis

## 📄 License

MIT License - feel free to use for personal or commercial projects.

## 🙏 Acknowledgments

Built with:
- [LangChain](https://langchain.com/) - Agent framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Workflow orchestration
- [OpenAI GPT-4](https://openai.com/) - Code analysis engine
- [Streamlit](https://streamlit.io/) - Web interface

---

**Made with ❤️ by developers, for developers**