# TradingAgents API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Core API](#core-api)
3. [Agent APIs](#agent-apis)
4. [Data Flow APIs](#data-flow-apis)
5. [Configuration APIs](#configuration-apis)
6. [State Management APIs](#state-management-apis)
7. [CLI APIs](#cli-apis)
8. [Error Handling](#error-handling)
9. [Examples](#examples)

## Overview

The TradingAgents framework provides a comprehensive API for building multi-agent trading systems. This documentation covers all public interfaces, their parameters, return values, and usage patterns.

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Initialize with default configuration
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# Execute trading analysis
final_state, decision = ta.propagate("NVDA", "2024-05-10")
```

## Core API

### TradingAgentsGraph

The main class that orchestrates the entire trading framework.

#### Constructor

```python
class TradingAgentsGraph:
    def __init__(
        self,
        selected_analysts: List[str] = ["market", "social", "news", "fundamentals"],
        debug: bool = False,
        config: Dict[str, Any] = None
    )
```

**Parameters:**
- `selected_analysts` (List[str]): List of analyst types to include in the workflow
  - Options: `["market", "social", "news", "fundamentals"]`
  - Default: All analysts enabled
- `debug` (bool): Enable debug mode with detailed tracing
  - Default: `False`
- `config` (Dict[str, Any]): Configuration dictionary
  - Default: `DEFAULT_CONFIG`

**Raises:**
- `ValueError`: If no analysts are selected
- `ValueError`: If unsupported LLM provider is specified

#### Methods

##### propagate()

Execute the trading analysis workflow for a specific company and date.

```python
def propagate(
    self, 
    company_name: str, 
    trade_date: str
) -> Tuple[Dict[str, Any], Any]
```

**Parameters:**
- `company_name` (str): Stock ticker symbol (e.g., "NVDA", "TSLA")
- `trade_date` (str): Analysis date in "YYYY-MM-DD" format

**Returns:**
- `Tuple[Dict[str, Any], Any]`: Final state dictionary and processed decision signal

**Example:**
```python
final_state, decision = ta.propagate("AAPL", "2024-05-10")
print(f"Decision: {decision}")
print(f"Final Report: {final_state['final_trade_decision']}")
```

##### process_signal()

Process the raw trading decision into a standardized signal.

```python
def process_signal(self, decision_text: str) -> str
```

**Parameters:**
- `decision_text` (str): Raw decision text from agents

**Returns:**
- `str`: Processed trading signal

##### reflect_and_remember()

Update agent memories based on trading outcomes.

```python
def reflect_and_remember(self, position_returns: float) -> None
```

**Parameters:**
- `position_returns` (float): Trading performance metric

**Note:** This method helps agents learn from past decisions.

### Configuration Management

#### DEFAULT_CONFIG

```python
DEFAULT_CONFIG: Dict[str, Any] = {
    "project_dir": str,           # Project directory path
    "results_dir": str,           # Results output directory
    "data_dir": str,              # Data cache directory
    "data_cache_dir": str,        # Local cache path
    "llm_provider": str,          # LLM provider ("openai", "anthropic", "google")
    "deep_think_llm": str,        # Model for strategic thinking
    "quick_think_llm": str,       # Model for fast responses
    "backend_url": str,           # LLM API endpoint
    "max_debate_rounds": int,     # Bull/Bear debate iterations
    "max_risk_discuss_rounds": int, # Risk assessment rounds
    "max_recur_limit": int,       # Maximum recursion depth
    "online_tools": bool,         # Use real-time data sources
}
```

#### Configuration Updates

```python
# Create custom configuration
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-3-opus"
config["quick_think_llm"] = "claude-3-haiku"
config["max_debate_rounds"] = 3
config["online_tools"] = True

# Use custom configuration
ta = TradingAgentsGraph(debug=True, config=config)
```

## Agent APIs

### Analyst Agents

#### Market Analyst

Analyzes technical indicators and market trends.

```python
def create_market_analyst(llm, toolkit) -> Callable
```

**Tools Used:**
- `get_YFin_data_online/offline`: Price and volume data
- `get_stockstats_indicators_report_online/offline`: Technical indicators

**Output:** Detailed technical analysis with trend insights and indicator tables

#### Social Media Analyst

Analyzes social sentiment and community discussions.

```python
def create_social_media_analyst(llm, toolkit) -> Callable
```

**Tools Used:**
- `get_stock_news_openai`: AI-powered news sentiment
- `get_reddit_stock_info`: Reddit discussion analysis

**Output:** Social sentiment analysis and community trend insights

#### News Analyst

Processes global news and macroeconomic events.

```python
def create_news_analyst(llm, toolkit) -> Callable
```

**Tools Used:**
- `get_global_news_openai`: Global news analysis
- `get_google_news`: Google News data
- `get_finnhub_news`: Financial news
- `get_reddit_news`: News discussions

**Output:** News impact analysis and macroeconomic assessment

#### Fundamentals Analyst

Analyzes company financial health and valuation.

```python
def create_fundamentals_analyst(llm, toolkit) -> Callable
```

**Tools Used:**
- `get_fundamentals_openai`: AI fundamental analysis
- `get_finnhub_company_insider_sentiment`: Insider sentiment
- `get_finnhub_company_insider_transactions`: Insider trading
- `get_simfin_balance_sheet`: Balance sheet data
- `get_simfin_cashflow`: Cash flow statements
- `get_simfin_income_stmt`: Income statements

**Output:** Comprehensive fundamental analysis with financial metrics

### Research Team

#### Bull Researcher

```python
def create_bull_researcher(llm, memory) -> Callable
```

**Purpose:** Advocates for positive investment positions
**Memory:** Maintains bullish research history
**Output:** Bullish investment thesis and growth opportunities

#### Bear Researcher

```python
def create_bear_researcher(llm, memory) -> Callable
```

**Purpose:** Identifies risks and potential downsides
**Memory:** Maintains bearish research history
**Output:** Risk assessment and bearish investment thesis

#### Research Manager

```python
def create_research_manager(llm, memory) -> Callable
```

**Purpose:** Moderates bull/bear debate and synthesizes insights
**LLM:** Uses deep-thinking model for strategic analysis
**Output:** Final research team recommendation

### Trading Team

#### Trader Agent

```python
def create_trader(llm, memory) -> Callable
```

**Purpose:** Converts research insights into actionable trading plans
**Input:** Research team recommendations
**Output:** Specific trade proposals with timing and sizing

### Risk Management Team

#### Risk Analysts

```python
def create_risky_debator(llm) -> Callable    # Aggressive perspective
def create_neutral_debator(llm) -> Callable  # Balanced perspective  
def create_safe_debator(llm) -> Callable     # Conservative perspective
```

**Purpose:** Multi-perspective risk evaluation
**Output:** Risk assessment from different viewpoints

#### Risk Manager

```python
def create_risk_manager(llm, memory) -> Callable
```

**Purpose:** Final risk evaluation and trade approval/rejection
**LLM:** Uses deep-thinking model for comprehensive analysis
**Output:** Final trading decision with risk justification

## Data Flow APIs

### Toolkit Class

Central interface for all data access tools.

```python
class Toolkit:
    def __init__(self, config: Dict[str, Any])
```

#### Market Data Tools

```python
# Yahoo Finance data
def get_YFin_data_online(ticker: str, start_date: str, end_date: str) -> str
def get_YFin_data(ticker: str, curr_date: str, look_back_days: int = 30) -> str

# Technical indicators
def get_stockstats_indicators_report_online(
    ticker: str, 
    start_date: str, 
    end_date: str, 
    indicators: List[str]
) -> str
def get_stockstats_indicators_report(
    ticker: str, 
    curr_date: str, 
    indicators: List[str], 
    look_back_days: int = 30
) -> str
```

#### News and Sentiment Tools

```python
# News analysis
def get_global_news_openai(query: str, curr_date: str) -> str
def get_google_news(query: str, curr_date: str, look_back_days: int = 7) -> str
def get_finnhub_news(ticker: str, curr_date: str, look_back_days: int = 7) -> str

# Social media analysis
def get_stock_news_openai(ticker: str, curr_date: str) -> str
def get_reddit_stock_info(ticker: str, curr_date: str, look_back_days: int = 7) -> str
def get_reddit_news(query: str, curr_date: str, look_back_days: int = 7) -> str
```

#### Fundamental Data Tools

```python
# Company fundamentals
def get_fundamentals_openai(ticker: str, curr_date: str) -> str

# Insider information
def get_finnhub_company_insider_sentiment(
    ticker: str, 
    curr_date: str, 
    look_back_days: int = 15
) -> str
def get_finnhub_company_insider_transactions(
    ticker: str, 
    curr_date: str, 
    look_back_days: int = 15
) -> str

# Financial statements
def get_simfin_balance_sheet(ticker: str, freq: str, curr_date: str) -> str
def get_simfin_cashflow(ticker: str, freq: str, curr_date: str) -> str
def get_simfin_income_stmt(ticker: str, freq: str, curr_date: str) -> str
```

### Data Configuration

```python
from tradingagents.dataflows.interface import set_config

# Configure data sources
set_config(config_dict)
```

## State Management APIs

### Agent States

#### AgentState

Main state container for the trading workflow.

```python
class AgentState(MessagesState):
    company_of_interest: str          # Stock ticker
    trade_date: str                   # Analysis date
    sender: str                       # Current agent
    
    # Analyst reports
    market_report: str                # Technical analysis
    sentiment_report: str             # Social sentiment
    news_report: str                  # News analysis
    fundamentals_report: str          # Fundamental analysis
    
    # Research outputs
    investment_debate_state: InvestDebateState
    investment_plan: str              # Research recommendation
    
    # Trading outputs
    trader_investment_plan: str       # Trading plan
    
    # Risk management
    risk_debate_state: RiskDebateState
    final_trade_decision: str         # Final decision
```

#### InvestDebateState

State for bull/bear research debates.

```python
class InvestDebateState(TypedDict):
    bull_history: str                 # Bullish conversation history
    bear_history: str                 # Bearish conversation history
    history: str                      # Combined conversation history
    current_response: str             # Latest response
    judge_decision: str               # Final judge decision
    count: int                        # Conversation length
```

#### RiskDebateState

State for risk management discussions.

```python
class RiskDebateState(TypedDict):
    risky_history: str                # Aggressive analyst history
    safe_history: str                 # Conservative analyst history
    neutral_history: str              # Neutral analyst history
    history: str                      # Combined history
    latest_speaker: str               # Last speaker
    current_risky_response: str       # Latest aggressive response
    current_safe_response: str        # Latest conservative response
    current_neutral_response: str     # Latest neutral response
    judge_decision: str               # Final risk decision
    count: int                        # Discussion length
```

### Memory Management

#### FinancialSituationMemory

Persistent memory for agents to learn from past decisions.

```python
class FinancialSituationMemory:
    def __init__(self, name: str, config: Dict[str, Any])
    
    def remember(self, situation: str, outcome: Any) -> None
    def recall(self, query: str) -> List[str]
    def clear(self) -> None
```

**Usage:**
```python
# Create memory for an agent
memory = FinancialSituationMemory("trader_memory", config)

# Store trading outcome
memory.remember("NVDA buy decision", {"return": 0.15, "duration": 30})

# Recall similar situations
similar_cases = memory.recall("NVDA trading decisions")
```

## CLI APIs

### Main CLI Interface

```python
from cli.main import app
import typer

# Run CLI application
if __name__ == "__main__":
    app()
```

### CLI Models

```python
from cli.models import AnalystType
from cli.utils import *

# Available analyst types
class AnalystType(str, Enum):
    MARKET = "market"
    SOCIAL = "social"
    NEWS = "news"
    FUNDAMENTALS = "fundamentals"
```

### Progress Tracking

```python
from cli.main import MessageBuffer

# Create message buffer for real-time updates
buffer = MessageBuffer(max_length=100)

# Track agent status
buffer.update_agent_status("Market Analyst", "complete")
buffer.add_message("info", "Analysis complete")
buffer.update_report_section("market_report", analysis_text)
```

## Error Handling

### Exception Types

```python
# Configuration errors
class ConfigurationError(Exception):
    """Raised when configuration is invalid"""

# Data access errors  
class DataAccessError(Exception):
    """Raised when data sources are unavailable"""

# LLM errors
class LLMError(Exception):
    """Raised when LLM providers fail"""

# Agent errors
class AgentExecutionError(Exception):
    """Raised when agent execution fails"""
```

### Error Recovery

```python
try:
    final_state, decision = ta.propagate("AAPL", "2024-05-10")
except DataAccessError as e:
    # Fallback to cached data
    config["online_tools"] = False
    ta = TradingAgentsGraph(config=config)
    final_state, decision = ta.propagate("AAPL", "2024-05-10")
except LLMError as e:
    # Switch to backup LLM provider
    config["llm_provider"] = "anthropic"
    ta = TradingAgentsGraph(config=config)
    final_state, decision = ta.propagate("AAPL", "2024-05-10")
```

## Examples

### Basic Trading Analysis

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Initialize framework
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# Analyze NVIDIA stock
final_state, decision = ta.propagate("NVDA", "2024-05-10")

# Access individual reports
print("Market Analysis:", final_state["market_report"])
print("News Analysis:", final_state["news_report"])
print("Final Decision:", final_state["final_trade_decision"])
```

### Custom Configuration

```python
# Create custom configuration
config = DEFAULT_CONFIG.copy()
config.update({
    "llm_provider": "anthropic",
    "deep_think_llm": "claude-3-opus",
    "quick_think_llm": "claude-3-haiku",
    "max_debate_rounds": 3,
    "online_tools": True,
    "results_dir": "./custom_results"
})

# Initialize with custom config
ta = TradingAgentsGraph(
    selected_analysts=["market", "fundamentals"],  # Only technical and fundamental analysis
    debug=False,
    config=config
)

# Execute analysis
final_state, decision = ta.propagate("TSLA", "2024-06-15")
```

### Batch Analysis

```python
import pandas as pd
from datetime import datetime, timedelta

# Define analysis parameters
tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
base_date = datetime(2024, 5, 1)
results = []

# Initialize framework
ta = TradingAgentsGraph(debug=False)

# Analyze multiple stocks
for ticker in tickers:
    for days_offset in range(0, 30, 7):  # Weekly analysis
        analysis_date = (base_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        
        try:
            final_state, decision = ta.propagate(ticker, analysis_date)
            
            results.append({
                "ticker": ticker,
                "date": analysis_date,
                "decision": decision,
                "market_score": extract_score(final_state["market_report"]),
                "sentiment_score": extract_score(final_state["sentiment_report"])
            })
            
        except Exception as e:
            print(f"Error analyzing {ticker} on {analysis_date}: {e}")

# Convert to DataFrame for analysis
df = pd.DataFrame(results)
print(df.head())
```

### Memory-Enhanced Analysis

```python
# Initialize with memory enabled
ta = TradingAgentsGraph(debug=True)

# Track performance over time
performances = []

for date in ["2024-05-01", "2024-05-15", "2024-06-01"]:
    final_state, decision = ta.propagate("AAPL", date)
    
    # Simulate trading outcome (replace with actual performance data)
    simulated_return = calculate_performance(decision, date)
    performances.append(simulated_return)
    
    # Update agent memories with performance
    ta.reflect_and_remember(simulated_return)

# Later analyses will benefit from accumulated experience
final_state, decision = ta.propagate("AAPL", "2024-06-15")
print("Decision with experience:", decision)
```

### CLI Integration

```python
import subprocess
import json

# Run CLI analysis programmatically
result = subprocess.run([
    "python", "-m", "cli.main",
    "--ticker", "NVDA",
    "--date", "2024-05-10",
    "--analysts", "market,fundamentals",
    "--output-format", "json"
], capture_output=True, text=True)

# Parse CLI output
if result.returncode == 0:
    analysis_result = json.loads(result.stdout)
    print("CLI Analysis:", analysis_result)
else:
    print("CLI Error:", result.stderr)
```

---

This API documentation provides comprehensive coverage of all public interfaces in the TradingAgents framework. For implementation details and internal APIs, refer to the Technical Specification document.