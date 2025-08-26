import chainlit as cl
import datetime
from pathlib import Path
from functools import wraps
import asyncio

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from cli.models import AnalystType

async def ask_question(question, default=None, type=str, timeout=120):
    """Helper function to ask a question and get a response."""
    while True:
        try:
            res = await cl.AskUserMessage(content=question, timeout=timeout).send()
            if res:
                # Basic validation for ticker
                if "ticker" in question.lower() and not res['output'].isalpha():
                    await cl.Message(content="Invalid ticker symbol. Please use letters only.").send()
                    continue
                # Basic validation for date
                if "date" in question.lower():
                    datetime.datetime.strptime(res['output'], "%Y-%m-%d")
                return type(res['output'])
        except ValueError:
            await cl.Message(content="Invalid date format. Please use YYYY-MM-DD.").send()
        except Exception as e:
            await cl.Message(content=f"An error occurred: {e}. Please try again.").send()
        return default

@cl.on_chat_start
async def start():
    """Main function to start the chat and get user selections."""
    await cl.Message(
        content="Welcome to the TradingAgents UI! Let's get started with the analysis."
    ).send()

    # Get user selections
    selected_ticker = await ask_question("Enter the ticker symbol to analyze:", "SPY")
    analysis_date = await ask_question(
        "Enter the analysis date (YYYY-MM-DD):",
        datetime.datetime.now().strftime("%Y-%m-%d"),
    )

    # Analyst selection
    analyst_options = [e.value for e in AnalystType]
    selected_analysts_str = await ask_question(
        f"Select analysts, separated by commas ({', '.join(analyst_options)}):",
        "market,social,news,fundamentals"
    )
    selected_analysts = [AnalystType(a.strip()) for a in selected_analysts_str.split(',')]

    # Research depth
    depth_options = [
        ("Shallow - Quick research, few debate and strategy discussion rounds", 1),
        ("Medium - Middle ground, moderate debate rounds and strategy discussion", 3),
        ("Deep - Comprehensive research, in depth debate and strategy discussion", 5),
    ]
    selected_research_depth_str = await ask_question(
        f"Select research depth (1, 3, or 5):", "1"
    )
    selected_research_depth = int(selected_research_depth_str)

    # LLM Provider
    provider_options = ["openai", "anthropic", "google", "openrouter", "ollama"]
    selected_llm_provider = await ask_question(
        f"Select LLM provider ({', '.join(provider_options)}):", "openai"
    )

    backend_url = "https://api.openai.com/v1" # Default to openai
    if selected_llm_provider == "anthropic":
        backend_url = "https://api.anthropic.com/v1"
    elif selected_llm_provider == "google":
        backend_url = "https://generativelanguage.googleapis.com/v1"
    elif selected_llm_provider == "openrouter":
        backend_url = "https://openrouter.ai/api/v1"
    elif selected_llm_provider == "ollama":
        backend_url = "http://localhost:11434/v1"


    # Thinker selection
    selected_shallow_thinker = await ask_question(
        f"Select shallow thinker model name:", "gpt-4o-mini"
    )

    selected_deep_thinker = await ask_question(
        f"Select deep thinker model name:", "gpt-4o-mini"
    )

    # Store selections in user session
    cl.user_session.set(
        "selections",
        {
            "ticker": selected_ticker,
            "analysis_date": analysis_date,
            "analysts": selected_analysts,
            "research_depth": selected_research_depth,
            "llm_provider": selected_llm_provider,
            "backend_url": backend_url,
            "shallow_thinker": selected_shallow_thinker,
            "deep_thinker": selected_deep_thinker,
        },
    )

    # Show a summary and a button to start
    summary = f"""
    Here are your selections:
    - **Ticker**: {selected_ticker}
    - **Analysis Date**: {analysis_date}
    - **Analysts**: {', '.join(a.value for a in selected_analysts)}
    - **Research Depth**: {selected_research_depth}
    - **LLM Provider**: {selected_llm_provider}
    - **Shallow Thinker**: {selected_shallow_thinker}
    - **Deep Thinker**: {selected_deep_thinker}

    Click the button below to start the analysis.
    """
    await cl.Message(
        content=summary,
        actions=[cl.Action(name="start_analysis", value="start", label="Start Analysis")],
    ).send()

@cl.action_callback("start_analysis")
async def on_action(action: cl.Action):
    """Callback to run the analysis when the 'Start Analysis' button is clicked."""
    if action.value == "start":
        await cl.Message(content="Starting analysis...").send()
        selections = cl.user_session.get("selections")

        # Create config
        config = DEFAULT_CONFIG.copy()
        config["max_debate_rounds"] = selections["research_depth"]
        config["max_risk_discuss_rounds"] = selections["research_depth"]
        config["quick_think_llm"] = selections["shallow_thinker"]
        config["deep_think_llm"] = selections["deep_thinker"]
        config["backend_url"] = selections["backend_url"]
        config["llm_provider"] = selections["llm_provider"].lower()

        # Initialize the graph
        graph = TradingAgentsGraph(
            [analyst.value for analyst in selections["analysts"]], config=config, debug=True
        )

        # Initialize state and get graph args
        init_agent_state = graph.propagator.create_initial_state(
            selections["ticker"], selections["analysis_date"]
        )
        args = graph.propagator.get_graph_args()

        # Stream the analysis
        final_report_content = ""
        final_state = None
        async for chunk in graph.graph.astream(init_agent_state, **args):
            final_state = chunk
            for key, value in chunk.items():
                if value:
                    author = key.replace("_", " ").title()
                    content = f"**{author}** completed.\n\n"
                    if isinstance(value, str):
                        content += value
                    elif isinstance(value, dict):
                        content += "\n".join(f"- **{k.replace('_', ' ').title()}**: {v}" for k, v in value.items())

                    await cl.Message(content=content, author=author).send()
            await asyncio.sleep(1)

        # Build and display the final report
        if final_state:
            final_report_content = "## Final Analysis Report\n\n"

            # Analyst Team Reports
            final_report_content += "### Analyst Team Reports\n"
            if final_state.get("market_report"):
                final_report_content += f"**Market Analyst:**\n{final_state['market_report']}\n\n"
            if final_state.get("sentiment_report"):
                final_report_content += f"**Social Analyst:**\n{final_state['sentiment_report']}\n\n"
            if final_state.get("news_report"):
                final_report_content += f"**News Analyst:**\n{final_state['news_report']}\n\n"
            if final_state.get("fundamentals_report"):
                final_report_content += f"**Fundamentals Analyst:**\n{final_state['fundamentals_report']}\n\n"

            # Research Team Decision
            if final_state.get("investment_plan"):
                final_report_content += "### Research Team Decision\n"
                final_report_content += f"{final_state['investment_plan']}\n\n"

            # Trading Team Plan
            if final_state.get("trader_investment_plan"):
                final_report_content += "### Trading Team Plan\n"
                final_report_content += f"{final_state['trader_investment_plan']}\n\n"

            # Portfolio Management Decision
            if final_state.get("final_trade_decision"):
                final_report_content += "### Portfolio Management Decision\n"
                final_report_content += f"{final_state['final_trade_decision']}\n\n"

            await cl.Message(content=final_report_content, author="Final Report").send()

            # Display the final decision
            decision = graph.process_signal(final_state.get("final_trade_decision", ""))
            await cl.Message(content=f"The final trading decision is: **{decision}**", author="Final Decision").send()
        else:
            await cl.Message(content="Analysis completed, but no final state was generated.", author="System").send()
