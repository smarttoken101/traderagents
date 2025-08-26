<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <!-- Keep these links. Translations will automatically update with the README. -->
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=zh">中文</a>
</div>

---

# TradingAgents: Multi-Agents LLM Financial Trading Framework 

> 🎉 **TradingAgents** officially released! We have received numerous inquiries about the work, and we would like to express our thanks for the enthusiasm in our community.
>
> So we decided to fully open-source the framework. Looking forward to building impactful projects with you!

<div align="center">
<a href="https://www.star-history.com/#TauricResearch/TradingAgents&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" />
   <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" style="width: 80%; height: auto;" />
 </picture>
</a>
</div>

<div align="center">

🚀 [Framework Overview](#tradingagents-framework) | ⚡ [Quick Start](#installation-and-cli) | 🎬 [Demo](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [API Usage](#tradingagents-package) | 📚 [Documentation](#documentation) | 🤝 [Contributing](#contributing) | 📄 [Citation](#citation)

</div>

## Documentation

📖 **Complete Documentation Suite**

- **[📋 Technical Specification](docs/TECHNICAL_SPECIFICATION.md)** - Complete architecture and component details
- **[🔧 API Documentation](docs/API_DOCUMENTATION.md)** - Comprehensive API reference and examples
- **[👨‍💻 Developer Guide](docs/DEVELOPER_GUIDE.md)** - Setup, development workflow, and contribution guide
- **[🏗️ Architecture Diagrams](docs/ARCHITECTURE_DIAGRAMS.md)** - Visual system architecture and data flows
- **[⚙️ Configuration Guide](docs/CONFIGURATION_GUIDE.md)** - Detailed configuration options and customization
- **[🧪 Testing Guide](docs/TESTING_GUIDE.md)** - Testing framework and examples
- **[🚀 Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Production deployment and scaling

## Table of Contents

1. [Framework Overview](#tradingagents-framework)
2. [Key Features](#key-features)
3. [Quick Start](#installation-and-cli)
4. [Package Usage](#tradingagents-package)
5. [Agent Architecture](#agent-architecture)
6. [Configuration](#configuration)
7. [Examples](#examples)
8. [Performance](#performance)
9. [Contributing](#contributing)
10. [Citation](#citation)

## TradingAgents Framework

### Overview

TradingAgents is a sophisticated multi-agent trading framework that leverages Large Language Models (LLMs) to simulate the collaborative decision-making processes of professional trading firms. The system orchestrates specialized AI agents representing different roles in financial analysis, research, trading, and risk management to create a comprehensive trading decision pipeline.

### Core Value Proposition

- **🎯 Collaborative Intelligence**: Multiple specialized agents work together to analyze different aspects of market conditions
- **🔄 Structured Decision Process**: Formal debate mechanisms ensure balanced risk assessment
- **📊 Comprehensive Analysis**: Technical, fundamental, sentiment, and news analysis integration
- **⚖️ Risk-Aware**: Multi-layered risk evaluation with conservative, neutral, and aggressive perspectives
- **🔧 Highly Configurable**: Supports multiple LLM providers and customizable workflows
- **📈 Research-Backed**: Built on academic research with proven methodologies

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> TradingAgents framework is designed for research purposes. Trading performance may vary based on many factors, including the chosen backbone language models, model temperature, trading periods, the quality of data, and other non-deterministic factors. [It is not intended as financial, investment, or trading advice.](https://tauric.ai/disclaimer/)

## Key Features

### 🎯 Multi-Agent Architecture
- **Specialized Roles**: Each agent focuses on specific domain expertise
- **Collaborative Decision Making**: Agents debate and discuss to reach consensus
- **Scalable Design**: Easy to add new agents or modify existing workflows

### 🔌 Flexible LLM Integration
- **Multiple Providers**: OpenAI, Anthropic, Google GenAI support
- **Smart Model Selection**: Fast models for routine tasks, deep models for strategic decisions
- **Cost Optimization**: Intelligent model routing to minimize API costs

### 📊 Comprehensive Data Sources
- **Market Data**: Yahoo Finance, FinnHub integration
- **Social Sentiment**: Reddit, social media analysis
- **News Analysis**: Google News, financial news aggregation
- **Fundamental Data**: Financial statements, insider trading data

### 🔄 Robust Workflow Engine
- **LangGraph Orchestration**: State-based workflow management
- **Error Recovery**: Graceful handling of API failures and data issues
- **Debug Mode**: Detailed execution tracing for development

### 💾 Advanced State Management
- **Persistent Memory**: Agents learn from past decisions
- **Session State**: Complete audit trail of decision processes
- **Export Capabilities**: JSON, Markdown report generation

Our framework decomposes complex trading tasks into specialized roles, ensuring a robust, scalable approach to market analysis and decision-making.

### Analyst Team
- Fundamentals Analyst: Evaluates company financials and performance metrics, identifying intrinsic values and potential red flags.
- Sentiment Analyst: Analyzes social media and public sentiment using sentiment scoring algorithms to gauge short-term market mood.
- News Analyst: Monitors global news and macroeconomic indicators, interpreting the impact of events on market conditions.
- Technical Analyst: Utilizes technical indicators (like MACD and RSI) to detect trading patterns and forecast price movements.

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### Researcher Team
- Comprises both bullish and bearish researchers who critically assess the insights provided by the Analyst Team. Through structured debates, they balance potential gains against inherent risks.

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Trader Agent
- Composes reports from the analysts and researchers to make informed trading decisions. It determines the timing and magnitude of trades based on comprehensive market insights.

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Risk Management and Portfolio Manager
- Continuously evaluates portfolio risk by assessing market volatility, liquidity, and other risk factors. The risk management team evaluates and adjusts trading strategies, providing assessment reports to the Portfolio Manager for final decision.
- The Portfolio Manager approves/rejects the transaction proposal. If approved, the order will be sent to the simulated exchange and executed.

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## Installation and CLI

### Installation

Clone TradingAgents:
```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

Create a virtual environment in any of your favorite environment managers:
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Required APIs

You will also need the FinnHub API for financial data. All of our code is implemented with the free tier.
```bash
export FINNHUB_API_KEY=$YOUR_FINNHUB_API_KEY
```

You will need the OpenAI API for all the agents.
```bash
export OPENAI_API_KEY=$YOUR_OPENAI_API_KEY
```

### CLI Usage

You can also try out the CLI directly by running:
```bash
python -m cli.main
```
You will see a screen where you can select your desired tickers, date, LLMs, research depth, etc.

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

An interface will appear showing results as they load, letting you track the agent's progress as it runs.

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

## TradingAgents Package

### Implementation Details

We built TradingAgents with LangGraph to ensure flexibility and modularity. We utilize `o1-preview` and `gpt-4o` as our deep thinking and fast thinking LLMs for our experiments. However, for testing purposes, we recommend you use `o4-mini` and `gpt-4.1-mini` to save on costs as our framework makes **lots of** API calls.

### Python Usage

To use TradingAgents inside your code, you can import the `tradingagents` module and initialize a `TradingAgentsGraph()` object. The `.propagate()` function will return a decision. You can run `main.py`, here's also a quick example:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# forward propagate
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

You can also adjust the default configuration to set your own choice of LLMs, debate rounds, etc.

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4.1-nano"  # Use a different model
config["quick_think_llm"] = "gpt-4.1-nano"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds
config["online_tools"] = True # Use online tools or cached data

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# forward propagate
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

> For `online_tools`, we recommend enabling them for experimentation, as they provide access to real-time data. The agents' offline tools rely on cached data from our **Tauric TradingDB**, a curated dataset we use for backtesting. We're currently in the process of refining this dataset, and we plan to release it soon alongside our upcoming projects. Stay tuned!

You can view the full list of configurations in [`tradingagents/default_config.py`](tradingagents/default_config.py). For detailed configuration options, see the [Configuration Guide](docs/CONFIGURATION_GUIDE.md).

## Agent Architecture

The TradingAgents framework implements a sophisticated multi-agent architecture with specialized roles:

### 👥 Analyst Team (Data Gathering & Analysis)
- **Market Analyst**: Technical analysis using 8+ indicators (MACD, RSI, Bollinger Bands, etc.)
- **Social Media Analyst**: Sentiment analysis from Reddit and social platforms
- **News Analyst**: Global news and macroeconomic event analysis
- **Fundamentals Analyst**: Financial statement analysis and insider trading monitoring

### 🎭 Research Team (Strategic Debate)
- **Bull Researcher**: Advocates for positive investment positions
- **Bear Researcher**: Identifies risks and potential downsides
- **Research Manager**: Moderates debate and synthesizes insights

### 💼 Trading Team (Decision Making)
- **Trader Agent**: Converts research insights into actionable trading plans

### 🛡️ Risk Management Team (Risk Assessment)
- **Aggressive Analyst**: High-risk, high-reward perspective
- **Conservative Analyst**: Risk-averse, capital preservation focus
- **Neutral Analyst**: Balanced, moderate risk approach
- **Risk Manager**: Final risk evaluation and trade approval/rejection

### 📈 Portfolio Management
- **Portfolio Manager**: Final trade execution decisions and position management

For detailed architecture diagrams and workflows, see [Architecture Diagrams](docs/ARCHITECTURE_DIAGRAMS.md).

## Configuration

### Environment Variables
```bash
# Required API Keys
export OPENAI_API_KEY="your_openai_api_key"
export FINNHUB_API_KEY="your_finnhub_api_key"

# Optional Configuration
export TRADINGAGENTS_RESULTS_DIR="./custom_results"
```

### Custom Configuration Example
```python
from tradingagents.default_config import DEFAULT_CONFIG

# Customize for production use
config = DEFAULT_CONFIG.copy()
config.update({
    "llm_provider": "anthropic",           # Use Anthropic Claude
    "deep_think_llm": "claude-3-opus",     # Strategic analysis
    "quick_think_llm": "claude-3-haiku",   # Fast operations
    "max_debate_rounds": 3,                # More thorough debates
    "online_tools": True,                  # Real-time data
    "results_dir": "./production_results"  # Custom output location
})
```

## Examples

### Basic Stock Analysis
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Initialize framework
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# Analyze a stock
final_state, decision = ta.propagate("NVDA", "2024-05-10")

# Access results
print(f"Decision: {decision}")
print(f"Market Analysis: {final_state['market_report']}")
print(f"Final Decision: {final_state['final_trade_decision']}")
```

### Batch Analysis
```python
tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
results = []

for ticker in tickers:
    final_state, decision = ta.propagate(ticker, "2024-05-10")
    results.append({
        "ticker": ticker,
        "decision": decision,
        "confidence": extract_confidence(final_state["final_trade_decision"])
    })

print("Batch Analysis Results:", results)
```

### Custom Agent Selection
```python
# Use only specific analysts
ta = TradingAgentsGraph(
    selected_analysts=["market", "fundamentals"],  # Technical + Fundamental only
    debug=False,
    config=config
)

final_state, decision = ta.propagate("TSLA", "2024-06-15")
```

## Performance

### Execution Time
- **Full Analysis**: ~2-5 minutes (depending on LLM provider and debate rounds)
- **Market Data Fetching**: ~10-30 seconds
- **Agent Processing**: ~1-3 minutes per agent
- **Risk Assessment**: ~30-60 seconds

### Cost Optimization
- **Model Tiering**: Use `gpt-4o-mini` for development, `o1-preview` for production
- **Caching**: Enable offline mode for development and testing
- **Debate Limits**: Adjust `max_debate_rounds` based on analysis depth needs

### Scalability
- **Concurrent Analysis**: Support for multiple stock analysis in parallel
- **Memory Efficiency**: Automatic cleanup and garbage collection
- **API Rate Limiting**: Built-in respect for provider rate limits

For detailed performance optimization guidelines, see the [Developer Guide](docs/DEVELOPER_GUIDE.md).

## Contributing

We welcome contributions from the community! Whether it's fixing a bug, improving documentation, or suggesting a new feature, your input helps make this project better. 

### Ways to Contribute

- 🐛 **Bug Reports**: Submit detailed bug reports with reproduction steps
- 💡 **Feature Requests**: Suggest new agents, data sources, or capabilities
- 📖 **Documentation**: Improve guides, add examples, fix typos
- 🔧 **Code Contributions**: Implement new features or fix existing issues
- 🧪 **Testing**: Add test cases, improve test coverage
- 🎨 **Examples**: Create tutorials, use cases, and integration examples

### Getting Started

1. **Read the [Developer Guide](docs/DEVELOPER_GUIDE.md)** for setup instructions
2. **Check [Issues](https://github.com/TauricResearch/TradingAgents/issues)** for open tasks
3. **Join our [Discord](https://discord.com/invite/hk9PGKShPK)** for discussions
4. **Follow our [Contribution Guidelines](docs/DEVELOPER_GUIDE.md#contributing)**

### Research Community

If you are interested in this line of research, please consider joining our open-source financial AI research community [Tauric Research](https://tauric.ai/). We're building the future of AI-driven financial analysis together!

## Citation

Please reference our work if you find *TradingAgents* provides you with some help :)

```bibtex
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

> ⚠️ **Important**: TradingAgents framework is designed for research purposes. Trading performance may vary based on many factors, including the chosen backbone language models, model temperature, trading periods, the quality of data, and other non-deterministic factors. [It is not intended as financial, investment, or trading advice.](https://tauric.ai/disclaimer/)

## Support

- 📖 **Documentation**: [Complete documentation suite](docs/)
- 💬 **Discord**: [Join our community](https://discord.com/invite/hk9PGKShPK)
- 🐛 **Issues**: [GitHub Issues](https://github.com/TauricResearch/TradingAgents/issues)
- 📧 **Email**: yijia.xiao@cs.ucla.edu
- 🐦 **Twitter**: [@TauricResearch](https://x.com/TauricResearch)

---

<div align="center">
  <sub>Built with ❤️ by the <a href="https://tauric.ai/">Tauric Research</a> team</sub>
</div>
