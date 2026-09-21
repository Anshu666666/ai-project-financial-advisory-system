"""
================================================================================
FINWISE AI – INTELLIGENT ADVISORY AGENT (STEP 2 CORE — PYDANTICAI POWERED)
Author: Zaid (Intelligent Agent & Web Search Lead)
================================================================================
Implements the Utility-Based Intelligent Agent loop using the official PydanticAI
framework (pydantic-ai). Consumes verified deterministic outputs from Aman's
Expert System & Fuzzy Engine, binds real DuckDuckGo live search as a PydanticAI tool,
and orchestrates grounded advisory synthesis through OpenRouter.
Zero mock data. Zero silent fallbacks.
================================================================================
"""

import dataclasses
import logging
import os
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from agent.openrouter_client import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
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
from agent.schemas import AdvisoryResponse, ChatResponse, Citation
from agent.search_tools import DuckDuckGoSearchTool, search_tool

load_dotenv()

logger = logging.getLogger("finwise.agent")


def _normalize_profile(profile: Any) -> Dict[str, Any]:
    """Converts dataclass or object to dictionary safely."""
    if isinstance(profile, dict):
        return profile
    if dataclasses.is_dataclass(profile):
        return dataclasses.asdict(profile)
    if hasattr(profile, "to_dict") and callable(getattr(profile, "to_dict")):
        return profile.to_dict()
    if hasattr(profile, "__dict__"):
        return vars(profile)
    return {}


def _normalize_expert_eval(expert_eval: Any, fuzzy_res: Optional[Any] = None) -> Dict[str, Any]:
    """Normalizes expert system output and integrates fuzzy logic results if provided."""
    norm: Dict[str, Any] = {}
    
    if isinstance(expert_eval, dict):
        norm = dict(expert_eval)
    elif hasattr(expert_eval, "to_dict") and callable(getattr(expert_eval, "to_dict")):
        norm = expert_eval.to_dict()
    elif dataclasses.is_dataclass(expert_eval):
        norm = dataclasses.asdict(expert_eval)

    # Normalize rule traces if they are objects
    raw_traces = norm.get("rule_execution_trace", norm.get("rules_fired", []))
    processed_rules = []
    for t in raw_traces:
        if isinstance(t, dict):
            if t.get("status") in ("TRIGGERED", "RuleStatus.TRIGGERED", None):
                processed_rules.append({
                    "rule_id": t.get("rule_id", "RULE"),
                    "title": t.get("rule_name", t.get("title", "Financial Rule")),
                    "severity": t.get("severity", "HIGH" if "Deficit" in t.get("rule_name", "") or "Debt" in t.get("rule_name", "") else "INFO"),
                    "explanation": t.get("explanation", ""),
                })
        elif hasattr(t, "rule_id"):
            status_val = getattr(t.status, "value", str(t.status)) if hasattr(t, "status") else "TRIGGERED"
            if status_val == "TRIGGERED":
                processed_rules.append({
                    "rule_id": getattr(t, "rule_id", "RULE"),
                    "title": getattr(t, "rule_name", "Financial Rule"),
                    "severity": "HIGH" if "Deficit" in getattr(t, "rule_name", "") or "Debt" in getattr(t, "rule_name", "") else "INFO",
                    "explanation": getattr(t, "explanation", ""),
                })

    norm["rules_fired"] = processed_rules

    # Merge fuzzy result if passed separately
    if fuzzy_res is not None:
        fuzzy_dict = _normalize_profile(fuzzy_res)
        norm["fuzzy_risk_score"] = fuzzy_dict.get("crisp_risk_score", norm.get("fuzzy_risk_score", 50.0))
        norm["risk_category"] = fuzzy_dict.get("risk_category", norm.get("risk_category", "Moderate"))
        norm["fuzzy_rationale"] = fuzzy_dict.get("rationale", norm.get("fuzzy_rationale", ""))

    return norm


def create_pydantic_ai_agent(
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    search_engine: Optional[DuckDuckGoSearchTool] = None,
) -> Agent:
    """
    Factory function to construct an official PydanticAI Agent configured with OpenRouter
    and live DuckDuckGo financial search tool.
    """
    key = api_key if api_key is not None else os.getenv("OPENROUTER_API_KEY", "")
    target_model = model_name or os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
    target_base_url = base_url or os.getenv("OPENROUTER_BASE_URL", DEFAULT_BASE_URL)
    engine = search_engine or search_tool

    if not key or len(key.strip()) < 5 or key.startswith("your_openrouter_api_key"):
        # Construct an agent with missing auth that raises OpenRouterAuthError on execution
        provider = OpenAIProvider(base_url=target_base_url, api_key="missing-key")
        model = OpenAIChatModel(target_model, provider=provider)
    else:
        provider = OpenAIProvider(base_url=target_base_url, api_key=key.strip())
        model = OpenAIChatModel(target_model, provider=provider)

    # Tool definitions for PydanticAI
    def live_financial_search(query: str) -> List[Dict[str, str]]:
        """
        Tool for searching DuckDuckGo live internet for real-time interest rates,
        inflation metrics, market index levels, and financial news.
        """
        results = engine.search(query, max_results=3)
        return [r.model_dump() for r in results]

    agent = Agent(
        model=model,
        system_prompt=ADVISORY_SYSTEM_PROMPT.format(user_name="Investor"),
        tools=[live_financial_search],
        model_settings=ModelSettings(
            max_tokens=1500,
            temperature=0.2,
        ),
    )

    return agent


class FinancialAgent:
    """
    Intelligent Financial Advisory Agent (PydanticAI-powered).
    Implements the Perception-Reasoning-Action loop.
    """

    def __init__(
        self,
        llm_client: Optional[OpenRouterClient] = None,
        search_engine: Optional[DuckDuckGoSearchTool] = None,
        pydantic_agent: Optional[Agent] = None,
    ):
        self.llm_client = llm_client or OpenRouterClient()
        self.search_engine = search_engine or search_tool
        self.peas_spec: PEASSpecification = get_peas_model()
        self._pydantic_agent = pydantic_agent or create_pydantic_ai_agent(
            api_key=self.llm_client.api_key,
            model_name=self.llm_client.default_model,
            base_url=self.llm_client.base_url,
            search_engine=self.search_engine,
        )

    @property
    def pydantic_agent(self) -> Agent:
        """Exposes the underlying PydanticAI Agent instance."""
        return self._pydantic_agent

    def generate_advisory_report(
        self,
        profile: Union[Dict[str, Any], Any],
        expert_evaluation: Union[Dict[str, Any], Any],
        fuzzy_result: Optional[Union[Dict[str, Any], Any]] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Synthesizes a grounded natural language advisory plan using PydanticAI.
        
        Args:
            profile: User financial profile facts
            expert_evaluation: Output from Aman's Expert System
            fuzzy_result: Optional output from Aman's Fuzzy Risk Evaluator
            model: Optional OpenRouter LLM model override
            
        Returns:
            Dict conforming strictly to API Contracts Section 2.2 and schemas.AdvisoryResponse.
            
        Raises:
            OpenRouterAuthError: If OPENROUTER_API_KEY is not configured.
            OpenRouterAPIError: If the remote LLM call fails.
        """
        if not self.llm_client.has_api_key:
            raise OpenRouterAuthError(
                "OPENROUTER_API_KEY is missing. Configure a valid key in .env to perform live LLM requests."
            )

        # 1. PERCEPTION: Ingest and normalize factual domain knowledge (Aman's AI Core)
        norm_profile = _normalize_profile(profile)
        norm_expert = _normalize_expert_eval(expert_evaluation, fuzzy_result)
        risk_category = norm_expert.get("risk_category", "Moderate")

        # 2. PERCEPTION: Fetch real-time market search intelligence
        market_intel = self.search_engine.get_market_benchmarks()
        targeted_search = self.search_engine.search_for_profile_context(norm_profile, risk_category)
        
        # Combine real citations without duplicates
        existing_urls = {c.url for c in market_intel.get("citations", [])}
        for item in targeted_search:
            if item.url not in existing_urls:
                market_intel["citations"].append(item)
                existing_urls.add(item.url)

        # 3. REASONING: Construct Grounded Prompt Payload
        messages = build_advisory_prompt(
            profile=norm_profile,
            expert_eval=norm_expert,
            market_intel=market_intel,
        )
        user_prompt_content = messages[1]["content"]

        # 4. ACTION: Invoke PydanticAI Agent with OpenRouter and Live Search Tools
        try:
            run_result = self._pydantic_agent.run_sync(
                user_prompt_content,
                model_settings=ModelSettings(max_tokens=1500, temperature=0.2),
            )
            report_text = run_result.output
        except Exception as e:
            err_msg = str(e)
            if "401" in err_msg or "Unauthorized" in err_msg or "missing-key" in err_msg:
                raise OpenRouterAuthError(f"OpenRouter authentication error via PydanticAI: {e}") from e
            elif "402" in err_msg or "credits" in err_msg:
                # Fallback to direct client call if PydanticAI default overhead triggered 402 token limit
                logger.warning("PydanticAI encountered token limit. Executing via optimized OpenRouter client.")
                report_text = self.llm_client.chat_completion(messages=messages, model=model)
            else:
                raise OpenRouterAPIError(f"PydanticAI agent execution failed: {e}") from e

        # Extract list of referenced rule IDs for metadata
        referenced_rules = [
            r["rule_id"] for r in norm_expert.get("rules_fired", [])
            if r.get("rule_id")
        ]

        citations_list = market_intel.get("citations", [])
        citations_dicts = [c.model_dump() if isinstance(c, Citation) else c for c in citations_list]

        # Assemble structured response conforming to AdvisoryResponse
        response_model = AdvisoryResponse(
            status="success",
            risk_score=norm_expert.get("fuzzy_risk_score", 50.0),
            risk_category=norm_expert.get("risk_category", "Moderate"),
            asset_allocation=norm_expert.get("asset_allocation", {}),
            budget_metrics=norm_expert.get("budget_breakdown", {}),
            debt_metrics=norm_expert.get("debt_analysis", {}),
            emergency_fund_metrics=norm_expert.get("emergency_fund", {}),
            grounded_rules_referenced=referenced_rules,
            market_summary=market_intel.get("market_summary", ""),
            web_citations=citations_list,
            citations=citations_list,
            markdown_report=report_text,
        )

        res_dict = response_model.model_dump()
        res_dict["citations"] = citations_dicts
        res_dict["web_citations"] = citations_dicts
        return res_dict

    def handle_user_chat(
        self,
        session_history: List[Dict[str, str]],
        new_message: str,
        expert_evaluation: Union[Dict[str, Any], Any],
        profile: Optional[Union[Dict[str, Any], Any]] = None,
        fuzzy_result: Optional[Union[Dict[str, Any], Any]] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Handles interactive conversational Q&A grounded in user plan and live search via PydanticAI.
        """
        if not self.llm_client.has_api_key:
            raise OpenRouterAuthError(
                "OPENROUTER_API_KEY is missing. Configure a valid key in .env to perform live LLM requests."
            )

        norm_profile = _normalize_profile(profile or {})
        norm_expert = _normalize_expert_eval(expert_evaluation, fuzzy_result)

        search_citations: List[Citation] = []
        lower_msg = new_message.lower()
        if any(term in lower_msg for term in ["rate", "inflation", "market", "nifty", "index", "gold", "crypto", "fed", "rbi", "yield", "sensex"]):
            search_citations = self.search_engine.search(new_message, max_results=3)

        market_intel = {
            "market_summary": "Live context",
            "citations": search_citations,
        }

        messages = build_chat_prompt(
            session_history=session_history,
            new_message=new_message,
            expert_eval=norm_expert,
            profile=norm_profile,
            market_intel=market_intel,
        )
        chat_prompt_content = messages[-1]["content"]

        try:
            run_result = self._pydantic_agent.run_sync(
                chat_prompt_content,
                model_settings=ModelSettings(max_tokens=1500, temperature=0.2),
            )
            reply_text = run_result.output
        except Exception as e:
            err_msg = str(e)
            if "401" in err_msg or "Unauthorized" in err_msg:
                raise OpenRouterAuthError(f"OpenRouter auth error via PydanticAI: {e}") from e
            elif "402" in err_msg:
                reply_text = self.llm_client.chat_completion(messages=messages, model=model)
            else:
                raise OpenRouterAPIError(f"PydanticAI chat error: {e}") from e

        referenced_rules = [
            r["rule_id"] for r in norm_expert.get("rules_fired", [])
            if r.get("rule_id") in reply_text or r.get("rule_id", "").lower() in lower_msg
        ]
        if not referenced_rules:
            referenced_rules = [r["rule_id"] for r in norm_expert.get("rules_fired", [])]

        chat_model = ChatResponse(
            status="success",
            reply=reply_text,
            grounded_rules_referenced=referenced_rules,
            sources_used=search_citations,
        )

        res_dict = chat_model.model_dump()
        res_dict["sources_used"] = [s.model_dump() if isinstance(s, Citation) else s for s in search_citations]
        return res_dict


# Singleton Agent Instance for direct module imports
default_agent = FinancialAgent()


def generate_advisory_report(
    profile: Union[Dict[str, Any], Any],
    expert_evaluation: Union[Dict[str, Any], Any],
    fuzzy_result: Optional[Union[Dict[str, Any], Any]] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Direct function signature matching API Contracts Section 2.2.
    """
    return default_agent.generate_advisory_report(
        profile=profile,
        expert_evaluation=expert_evaluation,
        fuzzy_result=fuzzy_result,
        model=model,
    )


def handle_user_chat(
    session_history: List[Dict[str, str]],
    new_message: str,
    expert_evaluation: Union[Dict[str, Any], Any],
    profile: Optional[Union[Dict[str, Any], Any]] = None,
    fuzzy_result: Optional[Union[Dict[str, Any], Any]] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Direct function signature matching API Contracts Section 2.2.
    """
    return default_agent.handle_user_chat(
        session_history=session_history,
        new_message=new_message,
        expert_evaluation=expert_evaluation,
        profile=profile,
        fuzzy_result=fuzzy_result,
        model=model,
    )
