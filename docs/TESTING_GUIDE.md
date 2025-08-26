# TradingAgents Testing Guide

## Table of Contents

1. [Testing Overview](#testing-overview)
2. [Test Setup](#test-setup)
3. [Unit Testing](#unit-testing)
4. [Integration Testing](#integration-testing)
5. [End-to-End Testing](#end-to-end-testing)
6. [Test Data & Fixtures](#test-data--fixtures)
7. [Mocking Strategies](#mocking-strategies)
8. [Best Practices](#best-practices)

## Testing Overview

The TradingAgents framework uses pytest for comprehensive testing across:
- **Unit Tests**: Individual component testing
- **Integration Tests**: Agent interaction testing
- **End-to-End Tests**: Complete workflow testing

### Test Structure
```
tests/
├── unit/                    # Unit tests
│   ├── test_agents/        # Agent tests
│   ├── test_dataflows/     # Data access tests
│   └── test_graph/         # Graph orchestration tests
├── integration/            # Integration tests
├── e2e/                   # End-to-end tests
├── fixtures/              # Test data
└── conftest.py            # pytest configuration
```

## Test Setup

### Dependencies
```bash
pip install pytest pytest-cov pytest-mock responses
```

### pytest Configuration (`pytest.ini`)
```ini
[tool:pytest]
testpaths = tests
addopts = --cov=tradingagents --cov-report=html --verbose
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    api: Tests requiring external APIs
```

### Test Configuration (`conftest.py`)
```python
import pytest
import os
from unittest.mock import patch
from tradingagents.default_config import DEFAULT_CONFIG

@pytest.fixture(scope="session")
def test_config():
    """Test configuration."""
    config = DEFAULT_CONFIG.copy()
    config.update({
        "llm_provider": "openai",
        "deep_think_llm": "gpt-4o-mini",
        "quick_think_llm": "gpt-4o-mini",
        "online_tools": False,
        "max_debate_rounds": 1,
        "results_dir": "./test_results",
    })
    return config

@pytest.fixture(autouse=True)
def mock_api_keys():
    """Mock API keys for testing."""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test_key",
        "FINNHUB_API_KEY": "test_key"
    }):
        yield

@pytest.fixture
def sample_agent_state():
    """Sample agent state for testing."""
    return {
        "company_of_interest": "AAPL",
        "trade_date": "2024-05-10",
        "messages": [],
        "market_report": None,
        "sentiment_report": None,
        "final_trade_decision": None,
    }
```

## Unit Testing

### Agent Unit Tests

```python
# tests/unit/test_agents/test_market_analyst.py
import pytest
from unittest.mock import Mock, MagicMock
from tradingagents.agents.analysts.market_analyst import create_market_analyst

class TestMarketAnalyst:
    @pytest.fixture
    def mock_toolkit(self):
        toolkit = Mock()
        toolkit.config = {"online_tools": True}
        toolkit.get_YFin_data_online = Mock(return_value="Sample data")
        return toolkit
    
    def test_analyst_creation(self, mock_llm, mock_toolkit):
        """Test analyst node creation."""
        analyst_node = create_market_analyst(mock_llm, mock_toolkit)
        assert callable(analyst_node)
    
    def test_analyst_execution(self, mock_llm, mock_toolkit, sample_agent_state):
        """Test analyst execution."""
        mock_response = MagicMock()
        mock_response.content = "Market analysis complete"
        mock_response.tool_calls = []
        mock_llm.bind_tools.return_value.invoke.return_value = mock_response
        
        analyst_node = create_market_analyst(mock_llm, mock_toolkit)
        result = analyst_node(sample_agent_state)
        
        assert "messages" in result
        assert result["market_report"] == "Market analysis complete"
```

### Data Flow Unit Tests

```python
# tests/unit/test_dataflows/test_yfin_utils.py
import pytest
from unittest.mock import patch
import pandas as pd
from tradingagents.dataflows.yfin_utils import get_yfin_data

class TestYFinUtils:
    @patch('yfinance.download')
    def test_successful_data_retrieval(self, mock_download):
        """Test successful data retrieval."""
        sample_data = pd.DataFrame({
            'Close': [150.0, 151.0]
        }, index=pd.date_range('2024-05-10', periods=2))
        
        mock_download.return_value = sample_data
        result = get_yfin_data("AAPL", "2024-05-10", "2024-05-11")
        
        assert "AAPL" in result
        assert "150.0" in result
    
    @patch('yfinance.download')
    def test_error_handling(self, mock_download):
        """Test error handling."""
        mock_download.side_effect = Exception("API Error")
        result = get_yfin_data("INVALID", "2024-05-10", "2024-05-11")
        
        assert "Error" in result or result == ""
```

## Integration Testing

### Agent Workflow Integration

```python
# tests/integration/test_agent_workflows.py
import pytest
from unittest.mock import Mock, patch
from tradingagents.graph.trading_graph import TradingAgentsGraph

class TestAgentWorkflows:
    def test_analyst_coordination(self, test_config):
        """Test coordination between analysts."""
        with patch('tradingagents.agents.utils.agent_utils.Toolkit') as mock_toolkit:
            toolkit_instance = Mock()
            toolkit_instance.get_YFin_data.return_value = "Market data"
            mock_toolkit.return_value = toolkit_instance
            
            ta = TradingAgentsGraph(
                selected_analysts=["market"],
                config=test_config
            )
            
            # Test would execute coordination logic
            assert ta is not None
    
    def test_memory_integration(self, test_config):
        """Test memory system integration."""
        ta = TradingAgentsGraph(config=test_config)
        
        # Test memory storage
        ta.bull_memory.remember("Test situation", "Test outcome")
        memories = ta.bull_memory.recall("Test")
        
        assert isinstance(memories, list)
```

## End-to-End Testing

### Complete Workflow Tests

```python
# tests/e2e/test_complete_workflow.py
import pytest
from unittest.mock import patch, Mock
from tradingagents.graph.trading_graph import TradingAgentsGraph

class TestCompleteWorkflow:
    @pytest.mark.e2e
    @pytest.mark.slow
    def test_full_analysis_workflow(self, test_config):
        """Test complete analysis workflow."""
        with patch('langchain_openai.ChatOpenAI') as mock_llm_class:
            mock_llm = Mock()
            mock_response = Mock()
            mock_response.content = "Analysis complete"
            mock_response.tool_calls = []
            mock_llm.bind_tools.return_value.invoke.return_value = mock_response
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm
            
            ta = TradingAgentsGraph(
                selected_analysts=["market"],
                debug=False,
                config=test_config
            )
            
            final_state, decision = ta.propagate("AAPL", "2024-05-10")
            
            assert final_state["company_of_interest"] == "AAPL"
            assert final_state["trade_date"] == "2024-05-10"
            assert decision is not None
```

## Test Data & Fixtures

### Sample Data Fixtures

```python
# tests/fixtures/sample_data.py
import pytest
import pandas as pd

@pytest.fixture
def sample_market_data():
    """Sample market data for testing."""
    return pd.DataFrame({
        'Open': [150.0, 151.0, 152.0],
        'High': [155.0, 156.0, 157.0],
        'Low': [148.0, 149.0, 150.0],
        'Close': [152.0, 153.0, 154.0],
        'Volume': [1000000, 1100000, 1200000]
    }, index=pd.date_range('2024-05-10', periods=3))

@pytest.fixture
def sample_news_data():
    """Sample news data for testing."""
    return [
        {
            "headline": "Apple Reports Strong Quarterly Results",
            "summary": "Apple exceeded expectations in Q2 earnings...",
            "date": "2024-05-10"
        },
        {
            "headline": "Tech Stocks Rally on AI Optimism",
            "summary": "Technology stocks continue to surge...",
            "date": "2024-05-09"
        }
    ]
```

### Mock Response Fixtures

```python
# tests/fixtures/mock_responses.py
@pytest.fixture
def mock_llm_responses():
    """Mock LLM responses for different agents."""
    return {
        "market_analyst": "Technical analysis shows bullish trend with RSI at 65",
        "news_analyst": "Recent news sentiment is positive for the stock",
        "bull_researcher": "Strong fundamental indicators support bullish view",
        "bear_researcher": "Some concerns about market volatility",
        "trader": "Recommend BUY with position size of 100 shares",
        "risk_manager": "Risk assessment: APPROVED for execution"
    }
```

## Mocking Strategies

### LLM Provider Mocking

```python
@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch('openai.OpenAI') as mock_client:
        mock_instance = Mock()
        mock_response = Mock()
        mock_response.choices[0].message.content = "Mock LLM response"
        mock_instance.chat.completions.create.return_value = mock_response
        mock_client.return_value = mock_instance
        yield mock_instance
```

### External API Mocking

```python
@pytest.fixture
def mock_external_apis():
    """Mock all external APIs."""
    with patch('yfinance.download') as mock_yf, \
         patch('finnhub.Client') as mock_fh, \
         patch('praw.Reddit') as mock_reddit:
        
        # Configure mocks
        mock_yf.return_value = pd.DataFrame({'Close': [100]})
        mock_fh.return_value.company_news.return_value = []
        mock_reddit.return_value.subreddit.return_value.search.return_value = []
        
        yield {
            'yfinance': mock_yf,
            'finnhub': mock_fh,
            'reddit': mock_reddit
        }
```

## Best Practices

### Test Organization
- **Arrange-Act-Assert**: Structure tests clearly
- **Single Responsibility**: One test per behavior
- **Descriptive Names**: Clear test method names
- **Parametrization**: Test multiple scenarios efficiently

### Mock Management
```python
# Good: Specific mocking
@patch('tradingagents.dataflows.yfin_utils.yf.download')
def test_data_retrieval(self, mock_download):
    mock_download.return_value = expected_data
    # Test logic

# Avoid: Over-mocking
@patch.object(TradingAgentsGraph, '__init__', return_value=None)
def test_something(self, mock_init):  # Too broad
    # Test logic
```

### Performance Testing
```python
import time
import pytest

@pytest.mark.benchmark
def test_analysis_performance(benchmark):
    """Benchmark analysis performance."""
    def run_analysis():
        ta = TradingAgentsGraph(config=fast_config)
        return ta.propagate("AAPL", "2024-05-10")
    
    result = benchmark(run_analysis)
    assert result is not None
```

### Running Tests

```bash
# All tests
pytest

# Specific categories
pytest -m unit
pytest -m integration
pytest -m "not slow"

# With coverage
pytest --cov=tradingagents --cov-report=html

# Parallel execution
pytest -n auto

# Verbose output
pytest -v

# Specific test file
pytest tests/unit/test_agents/test_market_analyst.py
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.13
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r tests/requirements-test.txt
      - name: Run tests
        run: pytest --cov=tradingagents
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

This testing guide provides a comprehensive framework for ensuring code quality and reliability in the TradingAgents project. Follow these patterns for robust test coverage and maintainable test code.