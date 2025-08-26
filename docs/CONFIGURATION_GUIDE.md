# TradingAgents Configuration Guide

## Table of Contents

1. [Configuration Overview](#configuration-overview)
2. [Default Configuration](#default-configuration)
3. [Environment Variables](#environment-variables)
4. [LLM Configuration](#llm-configuration)
5. [Data Source Configuration](#data-source-configuration)
6. [Workflow Configuration](#workflow-configuration)
7. [Performance Configuration](#performance-configuration)
8. [Security Configuration](#security-configuration)
9. [Advanced Configuration](#advanced-configuration)
10. [Configuration Examples](#configuration-examples)
11. [Troubleshooting](#troubleshooting)

## Configuration Overview

The TradingAgents framework uses a hierarchical configuration system that allows for flexible customization of all aspects of the trading workflow. Configuration can be set through:

1. **Default Configuration**: Base settings in `default_config.py`
2. **Environment Variables**: Runtime environment settings
3. **Custom Configuration**: Application-specific overrides
4. **CLI Arguments**: Command-line interface parameters

### Configuration Precedence

```
CLI Arguments > Environment Variables > Custom Configuration > Default Configuration
```

## Default Configuration

### Base Configuration Structure

The framework's default configuration is defined in [`tradingagents/default_config.py`](../tradingagents/default_config.py):

```python
DEFAULT_CONFIG = {
    # Directory Configuration
    "project_dir": str,           # Project root directory
    "results_dir": str,           # Output directory for reports and logs
    "data_dir": str,              # Cached data location (Tauric TradingDB)
    "data_cache_dir": str,        # Local cache directory
    
    # LLM Configuration
    "llm_provider": str,          # LLM provider ("openai", "anthropic", "google")
    "deep_think_llm": str,        # Model for strategic thinking/analysis
    "quick_think_llm": str,       # Model for fast responses/routine tasks
    "backend_url": str,           # LLM API endpoint URL
    
    # Workflow Configuration
    "max_debate_rounds": int,           # Bull/Bear research debate iterations
    "max_risk_discuss_rounds": int,     # Risk assessment discussion rounds
    "max_recur_limit": int,             # Maximum recursion depth
    
    # Data Configuration
    "online_tools": bool,         # Use real-time data sources vs cached data
}
```

### Default Values

```python
DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": "/Users/yluo/Documents/Code/ScAI/FR1-data",  # Note: Update for your environment
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    
    # LLM settings
    "llm_provider": "openai",
    "deep_think_llm": "o4-mini",      # Fast model for development
    "quick_think_llm": "gpt-4o-mini", # Cost-effective model
    "backend_url": "https://api.openai.com/v1",
    
    # Workflow settings
    "max_debate_rounds": 1,           # Minimal debates for speed
    "max_risk_discuss_rounds": 1,     # Minimal risk discussion
    "max_recur_limit": 100,
    
    # Data settings
    "online_tools": True,             # Use real-time data by default
}
```

## Environment Variables

### Required Environment Variables

These environment variables must be set for the framework to function:

```bash
# OpenAI API Configuration
export OPENAI_API_KEY="your_openai_api_key_here"

# FinnHub API Configuration  
export FINNHUB_API_KEY="your_finnhub_api_key_here"
```

### Optional Environment Variables

```bash
# Custom Results Directory
export TRADINGAGENTS_RESULTS_DIR="/path/to/custom/results"

# Custom Data Directory (for Tauric TradingDB)
export TRADINGAGENTS_DATA_DIR="/path/to/trading/data"

# Debug Mode
export TRADINGAGENTS_DEBUG="true"

# Logging Level
export TRADINGAGENTS_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR

# API Rate Limiting
export TRADINGAGENTS_RATE_LIMIT="60"   # Requests per minute

# Cache TTL (Time To Live)
export TRADINGAGENTS_CACHE_TTL="3600"  # Seconds
```

### Provider-Specific Environment Variables

#### Anthropic Configuration
```bash
export ANTHROPIC_API_KEY="your_anthropic_api_key"
export ANTHROPIC_API_URL="https://api.anthropic.com"  # Optional
```

#### Google GenAI Configuration
```bash
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"  # Optional
```

#### Reddit API Configuration (Optional)
```bash
export REDDIT_CLIENT_ID="your_reddit_client_id"
export REDDIT_CLIENT_SECRET="your_reddit_client_secret"
export REDDIT_USER_AGENT="TradingAgents/1.0"
```

## LLM Configuration

### Supported Providers

#### OpenAI Configuration
```python
config = {
    "llm_provider": "openai",
    "backend_url": "https://api.openai.com/v1",
    "deep_think_llm": "o1-preview",        # Strategic analysis
    "quick_think_llm": "gpt-4o-mini",      # Fast operations
}
```

**Available Models:**
- `o1-preview`: Most advanced reasoning (expensive)
- `o1-mini`: Advanced reasoning (cost-effective)
- `gpt-4o`: Multimodal capabilities
- `gpt-4o-mini`: Fast and cost-effective
- `gpt-4-turbo`: Previous generation
- `gpt-3.5-turbo`: Legacy model

#### Anthropic Configuration
```python
config = {
    "llm_provider": "anthropic",
    "backend_url": "https://api.anthropic.com",  # Optional
    "deep_think_llm": "claude-3-opus",
    "quick_think_llm": "claude-3-haiku",
}
```

**Available Models:**
- `claude-3-opus`: Highest capability
- `claude-3-sonnet`: Balanced performance
- `claude-3-haiku`: Fastest and most cost-effective

#### Google GenAI Configuration
```python
config = {
    "llm_provider": "google",
    "deep_think_llm": "gemini-2.0-flash",
    "quick_think_llm": "gemini-2.0-flash",
}
```

**Available Models:**
- `gemini-2.0-flash`: Latest Gemini model
- `gemini-pro`: Previous generation
- `gemini-pro-vision`: Multimodal capabilities

### Custom LLM Endpoints

#### OpenRouter Configuration
```python
config = {
    "llm_provider": "openai",  # Uses OpenAI-compatible interface
    "backend_url": "https://openrouter.ai/api/v1",
    "deep_think_llm": "anthropic/claude-3-opus",
    "quick_think_llm": "anthropic/claude-3-haiku",
}

# Set API key
os.environ["OPENAI_API_KEY"] = "your_openrouter_api_key"
```

#### Ollama (Local) Configuration
```python
config = {
    "llm_provider": "openai",  # Uses OpenAI-compatible interface
    "backend_url": "http://localhost:11434/v1",
    "deep_think_llm": "llama3.1:70b",
    "quick_think_llm": "llama3.1:8b",
}

# Set dummy API key for local models
os.environ["OPENAI_API_KEY"] = "ollama"
```

### Model Selection Strategy

#### Development Configuration
```python
# Fast, cost-effective for development
development_config = {
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4o-mini",
    "quick_think_llm": "gpt-4o-mini",
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "online_tools": False,  # Use cached data
}
```

#### Production Configuration
```python
# High-quality analysis for production
production_config = {
    "llm_provider": "openai",
    "deep_think_llm": "o1-preview",      # Best reasoning
    "quick_think_llm": "gpt-4o-mini",    # Cost balance
    "max_debate_rounds": 3,              # Thorough analysis
    "max_risk_discuss_rounds": 2,
    "online_tools": True,                # Real-time data
}
```

#### Cost-Optimized Configuration
```python
# Minimize costs while maintaining quality
cost_optimized_config = {
    "llm_provider": "anthropic",
    "deep_think_llm": "claude-3-sonnet",   # Good balance
    "quick_think_llm": "claude-3-haiku",   # Very cost-effective
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "online_tools": True,
}
```

## Data Source Configuration

### Online vs Offline Data

#### Online Data Sources (Real-time)
```python
config = {
    "online_tools": True,  # Enable real-time data fetching
}
```

**Available Online Sources:**
- Yahoo Finance: Real-time price data
- FinnHub: Professional financial data
- Google News: Current news articles
- Reddit: Social sentiment analysis
- OpenAI: AI-powered analysis

#### Offline Data Sources (Cached)
```python
config = {
    "online_tools": False,  # Use cached data
    "data_dir": "/path/to/tauric/tradingdb",  # Cached dataset location
}
```

**Cached Data Sources:**
- Tauric TradingDB: Curated historical dataset
- Local cache: Previously fetched data
- Preprocessed indicators: Pre-calculated technical analysis

### Data Source Priorities

```python
# Configure data source preferences
data_config = {
    "prefer_cached": True,     # Use cache when available
    "cache_ttl": 3600,         # Cache time-to-live (seconds)
    "retry_on_failure": True,  # Retry failed requests
    "fallback_to_cache": True, # Use cache if online fails
}
```

### API Rate Limiting

```python
rate_limit_config = {
    "openai_rpm": 3000,        # OpenAI requests per minute
    "finnhub_rpm": 60,         # FinnHub requests per minute
    "yahoo_rpm": 2000,         # Yahoo Finance requests per minute
    "google_rpm": 100,         # Google News requests per minute
    "retry_delay": 60,         # Delay between retries (seconds)
    "max_retries": 3,          # Maximum retry attempts
}
```

## Workflow Configuration

### Agent Selection

```python
# Select specific analysts for analysis
analyst_config = {
    "selected_analysts": [
        "market",       # Technical analysis
        "social",       # Social sentiment
        "news",         # News analysis
        "fundamentals"  # Fundamental analysis
    ]
}

# Minimal configuration (faster execution)
minimal_config = {
    "selected_analysts": ["market", "fundamentals"]
}

# Comprehensive analysis
comprehensive_config = {
    "selected_analysts": ["market", "social", "news", "fundamentals"]
}
```

### Debate Configuration

```python
debate_config = {
    "max_debate_rounds": 3,           # Bull vs Bear rounds
    "max_risk_discuss_rounds": 2,     # Risk assessment rounds
    "debate_timeout": 300,            # Timeout per round (seconds)
    "require_consensus": False,       # Force agreement before proceeding
    "min_debate_rounds": 1,           # Minimum required rounds
}
```

### Workflow Timing

```python
timing_config = {
    "agent_timeout": 180,       # Maximum time per agent (seconds)
    "total_timeout": 1800,      # Maximum total execution time
    "tool_timeout": 60,         # Maximum time per tool call
    "retry_timeout": 30,        # Timeout for retries
}
```

## Performance Configuration

### Memory Management

```python
memory_config = {
    "enable_agent_memory": True,      # Enable persistent agent memory
    "memory_size": 1000,              # Maximum memory entries per agent
    "memory_ttl": 86400,              # Memory time-to-live (seconds)
    "auto_cleanup": True,             # Automatic memory cleanup
    "memory_compression": True,       # Compress stored memories
}
```

### Caching Configuration

```python
cache_config = {
    "enable_caching": True,           # Enable response caching
    "cache_backend": "redis",         # Cache backend (redis, memory, file)
    "cache_host": "localhost",        # Redis host
    "cache_port": 6379,               # Redis port
    "cache_db": 0,                    # Redis database
    "cache_ttl": 3600,                # Cache time-to-live
    "cache_prefix": "tradingagents",  # Cache key prefix
}
```

### Parallelization

```python
parallel_config = {
    "enable_parallel_tools": True,    # Parallel tool execution
    "max_workers": 4,                 # Maximum parallel workers
    "tool_batch_size": 3,             # Tools per batch
    "parallel_timeout": 120,          # Timeout for parallel execution
}
```

## Security Configuration

### API Security

```python
security_config = {
    "validate_ssl": True,             # Validate SSL certificates
    "timeout": 30,                    # Request timeout
    "max_redirects": 3,               # Maximum HTTP redirects
    "user_agent": "TradingAgents/1.0", # Custom user agent
}
```

### Data Privacy

```python
privacy_config = {
    "anonymize_logs": True,           # Remove sensitive data from logs
    "encrypt_cache": False,           # Encrypt cached data
    "secure_temp": True,              # Use secure temporary directories
    "auto_cleanup_temp": True,        # Clean temporary files
}
```

### Audit Trail

```python
audit_config = {
    "enable_audit": True,             # Enable audit logging
    "audit_level": "INFO",            # Audit log level
    "audit_file": "audit.log",        # Audit log file
    "log_api_calls": True,            # Log all API calls
    "log_decisions": True,            # Log trading decisions
}
```

## Advanced Configuration

### Custom Agent Configuration

```python
custom_agent_config = {
    "custom_prompts": {
        "market_analyst": "Custom market analysis prompt...",
        "trader": "Custom trader prompt..."
    },
    "agent_temperatures": {
        "research_manager": 0.3,      # Conservative for strategic decisions
        "risk_judge": 0.1,            # Very conservative for risk
        "default": 0.7                # Default temperature
    },
    "agent_max_tokens": {
        "market_analyst": 2000,
        "fundamentals_analyst": 3000,
        "default": 1500
    }
}
```

### Integration Configuration

```python
integration_config = {
    "enable_webhooks": False,         # Enable webhook notifications
    "webhook_url": "https://...",     # Webhook endpoint
    "slack_integration": False,       # Slack notifications
    "email_notifications": False,    # Email alerts
    "database_logging": False,       # Log to database
    "export_formats": ["json", "csv", "markdown"]  # Export formats
}
```

### Development Configuration

```python
dev_config = {
    "debug_mode": True,               # Enable debug output
    "verbose_logging": True,          # Detailed logs
    "save_intermediate": True,        # Save intermediate states
    "enable_profiling": True,         # Performance profiling
    "mock_external_apis": False,      # Mock external API calls
    "test_mode": False,               # Enable test mode
}
```

## Configuration Examples

### Example 1: High-Performance Production

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

production_config = DEFAULT_CONFIG.copy()
production_config.update({
    # High-quality models
    "llm_provider": "openai",
    "deep_think_llm": "o1-preview",
    "quick_think_llm": "gpt-4o",
    
    # Thorough analysis
    "max_debate_rounds": 3,
    "max_risk_discuss_rounds": 2,
    
    # Real-time data
    "online_tools": True,
    
    # Comprehensive analysis
    "selected_analysts": ["market", "social", "news", "fundamentals"],
    
    # Performance optimization
    "enable_caching": True,
    "enable_parallel_tools": True,
    "max_workers": 6,
    
    # Monitoring
    "enable_audit": True,
    "verbose_logging": True,
    
    # Custom output
    "results_dir": "./production_results"
})

ta = TradingAgentsGraph(config=production_config)
```

### Example 2: Cost-Optimized Development

```python
dev_config = DEFAULT_CONFIG.copy()
dev_config.update({
    # Cost-effective models
    "llm_provider": "anthropic",
    "deep_think_llm": "claude-3-haiku",
    "quick_think_llm": "claude-3-haiku",
    
    # Minimal analysis for speed
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    
    # Use cached data
    "online_tools": False,
    
    # Limited analysis
    "selected_analysts": ["market", "fundamentals"],
    
    # Development features
    "debug_mode": True,
    "save_intermediate": True,
    "mock_external_apis": True,
})

ta = TradingAgentsGraph(debug=True, config=dev_config)
```

### Example 3: Research Configuration

```python
research_config = DEFAULT_CONFIG.copy()
research_config.update({
    # Balanced models
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4o",
    "quick_think_llm": "gpt-4o-mini",
    
    # Extended debates for research
    "max_debate_rounds": 5,
    "max_risk_discuss_rounds": 3,
    
    # Real-time data for accuracy
    "online_tools": True,
    
    # Full analysis suite
    "selected_analysts": ["market", "social", "news", "fundamentals"],
    
    # Research features
    "enable_agent_memory": True,
    "memory_size": 5000,
    "export_formats": ["json", "csv", "markdown"],
    
    # Detailed logging
    "audit_level": "DEBUG",
    "log_api_calls": True,
    "log_decisions": True,
})

ta = TradingAgentsGraph(config=research_config)
```

### Example 4: Multi-Provider Configuration

```python
# Configuration for provider redundancy
multi_provider_config = DEFAULT_CONFIG.copy()
multi_provider_config.update({
    # Primary provider
    "llm_provider": "openai",
    "deep_think_llm": "o1-preview",
    "quick_think_llm": "gpt-4o-mini",
    
    # Fallback configuration
    "fallback_providers": [
        {
            "provider": "anthropic",
            "deep_think_llm": "claude-3-opus",
            "quick_think_llm": "claude-3-haiku"
        },
        {
            "provider": "google",
            "deep_think_llm": "gemini-2.0-flash",
            "quick_think_llm": "gemini-2.0-flash"
        }
    ],
    
    # Retry logic
    "retry_on_failure": True,
    "max_retries": 2,
    "fallback_on_error": True,
})
```

## Troubleshooting

### Common Configuration Issues

#### 1. API Key Problems
```bash
# Check if environment variables are set
echo $OPENAI_API_KEY
echo $FINNHUB_API_KEY

# Verify API key validity
python -c "
import openai
client = openai.OpenAI()
try:
    response = client.models.list()
    print('OpenAI API key is valid')
except Exception as e:
    print(f'OpenAI API key error: {e}')
"
```

#### 2. Model Availability
```python
# Test model availability
from tradingagents.graph.trading_graph import TradingAgentsGraph

try:
    config = {"llm_provider": "openai", "deep_think_llm": "o1-preview"}
    ta = TradingAgentsGraph(config=config)
    print("Model configuration valid")
except Exception as e:
    print(f"Model error: {e}")
```

#### 3. Data Source Issues
```python
# Test data source connectivity
from tradingagents.agents.utils.agent_utils import Toolkit

toolkit = Toolkit(config={"online_tools": True})
try:
    data = toolkit.get_YFin_data_online("AAPL", "2024-01-01", "2024-01-31")
    print("Data sources accessible")
except Exception as e:
    print(f"Data source error: {e}")
```

#### 4. Configuration Validation
```python
def validate_config(config):
    """Validate configuration completeness and correctness."""
    required_keys = [
        "llm_provider", "deep_think_llm", "quick_think_llm",
        "max_debate_rounds", "online_tools"
    ]
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration: {key}")
    
    # Validate LLM provider
    valid_providers = ["openai", "anthropic", "google"]
    if config["llm_provider"] not in valid_providers:
        raise ValueError(f"Invalid LLM provider: {config['llm_provider']}")
    
    # Validate debate rounds
    if config["max_debate_rounds"] < 1:
        raise ValueError("max_debate_rounds must be >= 1")
    
    print("Configuration validation passed")

# Use validation
validate_config(your_config)
```

### Performance Troubleshooting

#### Slow Execution
```python
# Optimize for speed
speed_config = {
    "quick_think_llm": "gpt-4o-mini",    # Fastest model
    "max_debate_rounds": 1,               # Minimal debates
    "online_tools": False,                # Use cached data
    "enable_parallel_tools": True,        # Parallel execution
    "max_workers": 4,                     # Increase parallelism
}
```

#### High Costs
```python
# Optimize for cost
cost_config = {
    "llm_provider": "anthropic",
    "deep_think_llm": "claude-3-haiku",   # Most cost-effective
    "quick_think_llm": "claude-3-haiku",
    "max_debate_rounds": 1,
    "enable_caching": True,               # Cache responses
    "prefer_cached": True,                # Use cache when available
}
```

#### Memory Issues
```python
# Optimize memory usage
memory_config = {
    "enable_agent_memory": False,         # Disable memory
    "auto_cleanup": True,                 # Automatic cleanup
    "cache_backend": "file",              # Use file cache instead of memory
    "memory_compression": True,           # Compress data
}
```

### Debug Configuration

```python
debug_config = {
    "debug_mode": True,
    "verbose_logging": True,
    "log_level": "DEBUG",
    "save_intermediate": True,
    "enable_profiling": True,
    "audit_level": "DEBUG",
}

# Enable debug mode
ta = TradingAgentsGraph(debug=True, config=debug_config)
```

---

This configuration guide provides comprehensive coverage of all customization options available in the TradingAgents framework. Use these configurations to optimize the system for your specific use case, whether development, production, research, or cost optimization.