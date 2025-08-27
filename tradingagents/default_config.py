import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CONFIG = {
    # API Keys
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "finnhub_api_key": os.getenv("FINNHUB_API_KEY"),
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
    "google_api_key": os.getenv("GOOGLE_API_KEY"),
    "reddit_client_id": os.getenv("REDDIT_CLIENT_ID"),
    "reddit_client_secret": os.getenv("REDDIT_CLIENT_SECRET"),
    "reddit_user_agent": os.getenv("REDDIT_USER_AGENT"),
    # Application Configuration
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "log_level": os.getenv("TRADINGAGENTS_LOG_LEVEL", "INFO"),
    "debug": os.getenv("TRADINGAGENTS_DEBUG", "false").lower() in ("true", "1", "t"),
    "cache_ttl": int(os.getenv("TRADINGAGENTS_CACHE_TTL", 3600)),
    "data_dir": "/Users/yluo/Documents/Code/ScAI/FR1-data",
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "openai",
    "deep_think_llm": "o4-mini",
    "quick_think_llm": "gpt-4o-mini",
    "backend_url": "https://api.openai.com/v1",
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": True,
    # Database Configuration
    "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379"),
}
