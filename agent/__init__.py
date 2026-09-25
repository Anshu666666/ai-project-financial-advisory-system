"""
================================================================================
FINWISE AI – INTELLIGENT AGENT & WEB SEARCH PACKAGE
Author: Zaid (Intelligent Agent & Web Search Lead)
================================================================================
Exposes the complete Intelligent Agent subsystem:
- FinancialAgent (Perception-Reasoning-Action Loop)
- DuckDuckGoSearchTool (Live Financial Web Search & Benchmark Extractor)
- OpenRouterClient (Unified LLM Gateway)
- Grounded Prompt Synthesis & PEAS Formalization
- Structured Pydantic Output Schemas (AdvisoryResponse, ChatResponse, Citation)
================================================================================
"""

from agent.financial_agent import (
    FinancialAgent,
    default_agent,
    generate_advisory_report,
    handle_user_chat,
)
from agent.openrouter_client import (
    OpenRouterAPIError,
    OpenRouterAuthError,
    OpenRouterClient,
)
from agent.peas_model import PEASSpecification, get_peas_model
from agent.prompt_templates import (
    ADVISORY_SYSTEM_PROMPT,
    CHAT_SYSTEM_PROMPT,
    build_advisory_prompt,
    build_chat_prompt,
)
from agent.schemas import (
    AdvisoryMarketIntelligence,
    AdvisoryResponse,
    ChatResponse,
    Citation,
)
from agent.search_tools import (
    DuckDuckGoSearchTool,
    get_current_market_benchmarks,
    search_financial_market,
    search_tool,
)

__all__ = [
    "FinancialAgent",
    "default_agent",
    "generate_advisory_report",
    "handle_user_chat",
    "OpenRouterClient",
    "OpenRouterAuthError",
    "OpenRouterAPIError",
    "DuckDuckGoSearchTool",
    "search_tool",
    "search_financial_market",
    "get_current_market_benchmarks",
    "PEASSpecification",
    "get_peas_model",
    "build_advisory_prompt",
    "build_chat_prompt",
    "ADVISORY_SYSTEM_PROMPT",
    "CHAT_SYSTEM_PROMPT",
    "Citation",
    "AdvisoryResponse",
    "ChatResponse",
    "AdvisoryMarketIntelligence",
]
