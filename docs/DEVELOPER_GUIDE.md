# TradingAgents Developer Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [Contributing](#contributing)
6. [Testing Guide](#testing-guide)
7. [Debugging](#debugging)
8. [Performance Optimization](#performance-optimization)
9. [Extending the Framework](#extending-the-framework)
10. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13** or higher
- **Git** for version control
- **Conda** or **virtualenv** for environment management
- **API Keys** for required services

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TauricResearch/TradingAgents.git
   cd TradingAgents
   ```

2. **Create Virtual Environment**
   ```bash
   # Using Conda (recommended)
   conda create -n tradingagents python=3.13
   conda activate tradingagents
   
   # Or using venv
   python -m venv tradingagents
   source tradingagents/bin/activate  # Linux/Mac
   # tradingagents\Scripts\activate   # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   export FINNHUB_API_KEY="your_finnhub_api_key"
   
   # Windows
   set OPENAI_API_KEY=your_openai_api_key
   set FINNHUB_API_KEY=your_finnhub_api_key
   ```

5. **Run Basic Test**
   ```bash
   python main.py
   ```

## Development Environment Setup

### IDE Configuration

#### VS Code Setup
1. Install recommended extensions:
   - Python
   - Pylance
   - Python Docstring Generator
   - GitLens

2. Configure settings in `.vscode/settings.json`:
   ```json
   {
     "python.defaultInterpreterPath": "./tradingagents/bin/python",
     "python.linting.enabled": true,
     "python.linting.pylintEnabled": true,
     "python.formatting.provider": "black",
     "python.sortImports.args": ["--profile", "black"],
     "files.exclude": {
       "**/__pycache__": true,
       "**/*.pyc": true
     }
   }
   ```

#### PyCharm Setup
1. Configure Project Structure:
   - Mark `tradingagents` as Sources Root
   - Mark `tests` as Test Sources Root

2. Set up Run Configurations:
   - Main Application: `main.py`
   - CLI Application: `cli/main.py`
   - Tests: pytest configuration

### Development Tools

#### Code Formatting and Linting
```bash
# Install development tools
pip install black isort pylint mypy pytest

# Format code
black tradingagents/ cli/ tests/

# Sort imports
isort tradingagents/ cli/ tests/

# Lint code
pylint tradingagents/ cli/

# Type checking
mypy tradingagents/
```

#### Pre-commit Hooks
Set up pre-commit hooks to ensure code quality:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
EOF

# Install hooks
pre-commit install
```

## Project Structure

```
TradingAgents/
├── tradingagents/              # Core framework
│   ├── agents/                 # Agent implementations
│   │   ├── analysts/           # Market analysis agents
│   │   ├── researchers/        # Research team agents
│   │   ├── trader/             # Trading decision agent
│   │   ├── managers/           # Management agents
│   │   ├── risk_mgmt/          # Risk management agents
│   │   └── utils/              # Agent utilities
│   ├── graph/                  # LangGraph orchestration
│   ├── dataflows/              # Data access layer
│   └── default_config.py       # Default configuration
├── cli/                        # Command-line interface
│   ├── main.py                 # CLI entry point
│   ├── models.py               # CLI data models
│   └── utils.py                # CLI utilities
├── docs/                       # Documentation
├── tests/                      # Test suites
├── results/                    # Output directory
├── main.py                     # Main entry point
├── requirements.txt            # Dependencies
├── pyproject.toml              # Project metadata
└── setup.py                    # Package setup
```

### Key Directories

#### `tradingagents/agents/`
Contains all agent implementations organized by role:
- **analysts/**: Technical, fundamental, news, and social analysis
- **researchers/**: Bull/bear research debate participants
- **trader/**: Trading decision synthesis
- **managers/**: Research and risk management coordination
- **risk_mgmt/**: Multi-perspective risk evaluation
- **utils/**: Shared agent utilities and state management

#### `tradingagents/graph/`
LangGraph orchestration components:
- **trading_graph.py**: Main orchestrator
- **setup.py**: Graph configuration and compilation
- **conditional_logic.py**: Agent transition logic
- **propagation.py**: State propagation handling

#### `tradingagents/dataflows/`
Data access and processing:
- **interface.py**: Unified data access API
- **Source-specific utilities**: YFinance, FinnHub, Reddit, etc.
- **data_cache/**: Local data caching

## Development Workflow

### Git Workflow

We follow a feature branch workflow:

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following project conventions
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

4. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create pull request on GitHub
   ```

### Commit Message Convention

We use conventional commits:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions/modifications
- `chore:` - Maintenance tasks

### Branch Protection

Main branch is protected with requirements:
- All tests must pass
- Code review required
- Up-to-date with main branch

## Contributing

### Code Style Guidelines

#### Python Style
- Follow PEP 8 standards
- Use Black for code formatting
- Maximum line length: 88 characters
- Use type hints for all public interfaces

#### Documentation Style
- Use Google-style docstrings
- Include examples in docstrings
- Update API documentation for changes

#### Example Function Documentation:
```python
def analyze_market_data(
    ticker: str, 
    start_date: str, 
    indicators: List[str]
) -> Dict[str, Any]:
    """Analyze market data using technical indicators.
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL')
        start_date: Analysis start date in 'YYYY-MM-DD' format
        indicators: List of technical indicators to calculate
        
    Returns:
        Dictionary containing analysis results with keys:
        - 'trend': Overall trend direction
        - 'signals': Trading signals
        - 'indicators': Calculated indicator values
        
    Raises:
        ValueError: If ticker is invalid
        DataAccessError: If market data unavailable
        
    Example:
        >>> result = analyze_market_data('AAPL', '2024-01-01', ['rsi', 'macd'])
        >>> print(result['trend'])
        'bullish'
    """
    # Implementation here
    pass
```

### Pull Request Guidelines

1. **PR Title**: Use conventional commit format
2. **Description**: Include:
   - What changes were made
   - Why the changes were necessary
   - Any breaking changes
   - Testing instructions

3. **Checklist**:
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] Code follows style guidelines
   - [ ] No breaking changes (or clearly documented)

### Code Review Process

1. **Automated Checks**: All CI checks must pass
2. **Peer Review**: At least one approval required
3. **Maintainer Review**: Core maintainer final approval
4. **Merge**: Squash and merge to main

## Testing Guide

### Test Structure

```
tests/
├── unit/                       # Unit tests
│   ├── test_agents/           # Agent tests
│   ├── test_dataflows/        # Data access tests
│   └── test_graph/            # Graph orchestration tests
├── integration/               # Integration tests
│   ├── test_end_to_end/      # Full workflow tests
│   └── test_api_integration/  # External API tests
├── fixtures/                  # Test data and fixtures
└── conftest.py               # pytest configuration
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Run with coverage
pytest --cov=tradingagents --cov-report=html

# Run specific test file
pytest tests/unit/test_agents/test_market_analyst.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_market_analysis"
```

### Writing Tests

#### Unit Test Example:
```python
import pytest
from unittest.mock import Mock, patch
from tradingagents.agents.analysts.market_analyst import create_market_analyst

class TestMarketAnalyst:
    @pytest.fixture
    def mock_llm(self):
        """Mock LLM for testing."""
        llm = Mock()
        llm.bind_tools.return_value.invoke.return_value.content = "Test analysis"
        return llm
    
    @pytest.fixture
    def mock_toolkit(self):
        """Mock toolkit for testing."""
        toolkit = Mock()
        toolkit.get_YFin_data_online = Mock()
        toolkit.get_stockstats_indicators_report_online = Mock()
        return toolkit
    
    def test_market_analyst_creation(self, mock_llm, mock_toolkit):
        """Test market analyst node creation."""
        analyst_node = create_market_analyst(mock_llm, mock_toolkit)
        assert callable(analyst_node)
    
    def test_market_analyst_execution(self, mock_llm, mock_toolkit):
        """Test market analyst execution."""
        analyst_node = create_market_analyst(mock_llm, mock_toolkit)
        
        state = {
            "trade_date": "2024-05-10",
            "company_of_interest": "AAPL",
            "messages": []
        }
        
        result = analyst_node(state)
        
        assert "messages" in result
        assert "market_report" in result
```

#### Integration Test Example:
```python
import pytest
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

class TestTradingWorkflow:
    @pytest.fixture
    def trading_graph(self):
        """Create trading graph for testing."""
        config = DEFAULT_CONFIG.copy()
        config["online_tools"] = False  # Use cached data for tests
        return TradingAgentsGraph(debug=False, config=config)
    
    def test_end_to_end_workflow(self, trading_graph):
        """Test complete trading workflow."""
        final_state, decision = trading_graph.propagate("AAPL", "2024-05-10")
        
        # Verify all required components are present
        assert final_state["company_of_interest"] == "AAPL"
        assert final_state["trade_date"] == "2024-05-10"
        assert final_state["market_report"] is not None
        assert final_state["final_trade_decision"] is not None
        assert decision is not None
```

### Test Configuration

#### `conftest.py`:
```python
import pytest
import os
from unittest.mock import patch

@pytest.fixture(scope="session")
def test_config():
    """Test configuration."""
    return {
        "llm_provider": "openai",
        "deep_think_llm": "gpt-4o-mini",
        "quick_think_llm": "gpt-4o-mini",
        "online_tools": False,
        "max_debate_rounds": 1,
        "max_risk_discuss_rounds": 1,
    }

@pytest.fixture(autouse=True)
def mock_api_keys():
    """Mock API keys for testing."""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test_key",
        "FINNHUB_API_KEY": "test_key"
    }):
        yield
```

## Debugging

### Debug Mode

Enable debug mode for detailed execution traces:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Enable debug mode
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# Execute with full tracing
final_state, decision = ta.propagate("AAPL", "2024-05-10")
```

### Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tradingagents.log'),
        logging.StreamHandler()
    ]
)

# Use in your code
logger = logging.getLogger(__name__)
logger.info("Starting analysis for AAPL")
```

### Common Debugging Techniques

1. **State Inspection**: Examine agent states at each step
2. **Tool Call Monitoring**: Track data source interactions
3. **LLM Response Analysis**: Review raw LLM outputs
4. **Memory Inspection**: Check agent memory contents

### Debug Utilities

```python
def debug_state(state, step_name):
    """Debug utility to inspect state."""
    print(f"\n=== {step_name} ===")
    for key, value in state.items():
        if key != "messages":
            print(f"{key}: {type(value)} - {str(value)[:100]}...")

def debug_messages(state):
    """Debug utility to inspect messages."""
    print("\n=== Messages ===")
    for i, msg in enumerate(state.get("messages", [])):
        print(f"Message {i}: {msg.type} - {str(msg.content)[:100]}...")
```

## Performance Optimization

### LLM Usage Optimization

1. **Model Selection**:
   - Use fast models (`gpt-4o-mini`) for routine tasks
   - Reserve powerful models (`o1-preview`) for strategic decisions

2. **Context Management**:
   - Minimize prompt length
   - Use structured outputs
   - Implement context pruning

3. **Caching**:
   - Cache LLM responses for repeated queries
   - Use local data caching for development

### Data Access Optimization

1. **Batch Requests**: Combine multiple API calls
2. **Parallel Processing**: Use concurrent data fetching
3. **Smart Caching**: Implement TTL-based cache invalidation

### Memory Management

```python
import gc
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_analysis(ticker, date):
    """Cache expensive analysis results."""
    # Expensive computation here
    pass

def cleanup_memory():
    """Clean up memory after analysis."""
    gc.collect()
```

## Extending the Framework

### Adding New Agents

1. **Create Agent Module**:
   ```python
   # tradingagents/agents/analysts/new_analyst.py
   from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
   
   def create_new_analyst(llm, toolkit):
       def new_analyst_node(state):
           # Implementation here
           return {
               "messages": [result],
               "new_report": report_content,
           }
       return new_analyst_node
   ```

2. **Register Agent**:
   ```python
   # In tradingagents/agents/__init__.py
   from .analysts.new_analyst import create_new_analyst
   
   __all__ = [
       # ... existing exports
       "create_new_analyst",
   ]
   ```

3. **Update Graph Setup**:
   ```python
   # In tradingagents/graph/setup.py
   if "new_analyst" in selected_analysts:
       analyst_nodes["new_analyst"] = create_new_analyst(
           self.quick_thinking_llm, self.toolkit
       )
   ```

### Adding New Data Sources

1. **Create Data Utility**:
   ```python
   # tradingagents/dataflows/new_data_source.py
   from typing import Annotated
   
   def get_new_data_source(
       ticker: Annotated[str, "Stock ticker"],
       date: Annotated[str, "Analysis date"],
       params: Annotated[dict, "Additional parameters"]
   ) -> str:
       """Fetch data from new source."""
       # Implementation here
       pass
   ```

2. **Register Tool**:
   ```python
   # In tradingagents/agents/utils/agent_utils.py
   class Toolkit:
       def __init__(self, config):
           # ... existing tools
           self.get_new_data_source = get_new_data_source
   ```

### Custom LLM Providers

```python
# Custom LLM provider implementation
from langchain_core.language_models import BaseLLM

class CustomLLMProvider(BaseLLM):
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
    
    def _call(self, prompt: str, stop: List[str] = None) -> str:
        # Implementation here
        pass
    
    @property
    def _llm_type(self) -> str:
        return "custom"

# Use in configuration
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "custom"
# Custom provider initialization logic
```

## Troubleshooting

### Common Issues

#### 1. API Key Errors
```bash
# Problem: Missing or invalid API keys
# Solution: Check environment variables
echo $OPENAI_API_KEY
echo $FINNHUB_API_KEY

# Set if missing
export OPENAI_API_KEY="your_key_here"
export FINNHUB_API_KEY="your_key_here"
```

#### 2. Import Errors
```bash
# Problem: Module not found
# Solution: Verify Python path and installation
pip list | grep tradingagents
python -c "import tradingagents; print(tradingagents.__file__)"
```

#### 3. Data Access Issues
```python
# Problem: Data source unavailable
# Solution: Use offline mode
config = DEFAULT_CONFIG.copy()
config["online_tools"] = False
ta = TradingAgentsGraph(config=config)
```

#### 4. Memory Issues
```python
# Problem: Out of memory
# Solution: Reduce model size and clear cache
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"  # Smaller model
config["quick_think_llm"] = "gpt-4o-mini"

# Clear cache periodically
import gc
gc.collect()
```

### Getting Help

1. **Check Documentation**: Review technical specification and API docs
2. **Search Issues**: Check GitHub issues for similar problems
3. **Create Issue**: Report bugs with detailed reproduction steps
4. **Community**: Join Discord for real-time help
5. **Logging**: Enable debug logging for detailed error information

### Performance Monitoring

```python
import time
import psutil
import functools

def monitor_performance(func):
    """Decorator to monitor function performance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        print(f"{func.__name__}:")
        print(f"  Time: {end_time - start_time:.2f}s")
        print(f"  Memory: {end_memory - start_memory:.2f}MB")
        
        return result
    return wrapper

# Use decorator
@monitor_performance
def analyze_stock(ticker, date):
    ta = TradingAgentsGraph()
    return ta.propagate(ticker, date)
```

---

This developer guide provides comprehensive information for setting up, developing, and contributing to the TradingAgents framework. For additional technical details, refer to the Technical Specification and API Documentation.