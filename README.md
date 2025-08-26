# TradingAgents: Multi-Agent LLM Financial Trading Framework

This project is a multi-agent Large Language Model (LLM) based framework for financial trading analysis. It uses a team of specialized AI agents to analyze a stock, conduct research, and make trading decisions.

## Features

*   **Multi-Agent System**: Different agents with specialized roles (analyst, researcher, trader, etc.) collaborate to provide a comprehensive analysis.
*   **Extensible Framework**: Easily add new agents, data sources, and models.
*   **Command-Line and Chatbot UI**: Interact with the system through either a powerful CLI or a user-friendly chatbot interface.
*   **In-depth Analysis**: The agents perform fundamental analysis, technical analysis, news sentiment analysis, and more.

## Getting Started

### Prerequisites

*   Python 3.10 or higher
*   An LLM API key (e.g., OpenAI, Anthropic, Google)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/TauricResearch/TradingAgents.git
    cd TradingAgents
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the root of the project and add your API keys:
    ```
    OPENAI_API_KEY="your-openai-api-key"
    FINNHUB_API_KEY="your-finnhub-api-key"
    # Add other keys as needed
    ```

## How to Run

### Chatbot UI (Recommended)

The chatbot UI provides a user-friendly way to interact with the TradingAgents framework.

To run the chatbot UI, use the following command:

```bash
chainlit run app.py -w
```

This will start the Chainlit server and open the UI in your web browser. The `-w` flag enables auto-reloading, so the server will restart automatically when you make changes to the code.

### Command-Line Interface (CLI)

The CLI provides a powerful and scriptable way to run the analysis.

To run the CLI, use the following command:
```bash
python -m cli.main analyze
```
The CLI will guide you through the process of selecting the ticker, analysis date, and other parameters.
