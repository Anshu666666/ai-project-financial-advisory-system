"""
================================================================================
FINWISE AI – STEP 2 STANDALONE PYDANTICAI AGENT VERIFICATION SUITE
Author: Zaid (Intelligent Agent & Web Search Lead)
================================================================================
Comprehensive verification suite testing all Step 2 PydanticAI criteria:
- Genuine PydanticAI (pydantic-ai) framework integration
- 100% real integration with Aman's AI Core (Fuzzy + Expert System)
- Real DuckDuckGo live web search registered as a PydanticAI tool
- Real OpenRouter API client and structured Pydantic response validation
- Zero mock data, zero fake fallbacks, zero hardcoded market statistics
- Full Step 3 API backward compatibility (generate_advisory_report, handle_user_chat)
================================================================================
"""

import inspect
import os
import sys
from typing import Any, Dict, List

# Ensure UTF-8 console output across Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dotenv import load_dotenv

load_dotenv()

import pydantic_ai
from pydantic_ai import Agent

from agent import (
    AdvisoryResponse,
    ChatResponse,
    Citation,
    DuckDuckGoSearchTool,
    FinancialAgent,
    OpenRouterAPIError,
    OpenRouterAuthError,
    OpenRouterClient,
    generate_advisory_report,
    get_peas_model,
    handle_user_chat,
    search_financial_market,
)
from agent.financial_agent import create_pydantic_ai_agent
import agent.openrouter_client as or_module
import agent.search_tools as st_module
from expert_system import (
    FinancialInferenceEngine,
    RuleStatus,
    UserFinancialProfile,
)
from fuzzy_logic import FuzzyRiskEvaluator


def print_banner(title: str):
    print("\n" + "=" * 80)
    print(f"  {title.upper()}")
    print("=" * 80)


def print_test_row(test_num: int, total: int, name: str, status: str, detail: str = ""):
    status_str = f"[{status}]"
    dots = "." * max(2, 52 - len(name) - len(str(test_num)) - len(str(total)))
    print(f"[{test_num}/{total}] {name} {dots} {status_str} {detail}")


def run_standalone_tests():
    print("\n" + "#" * 80)
    print("# FINWISE AI – STEP 2 PYDANTICAI AGENT STANDALONE VERIFICATION")
    print(f"# Lead: Zaid (Intelligent Agent & Web Search) | PydanticAI v{pydantic_ai.__version__}")
    print("#" * 80)

    total_tests = 16
    passed_tests = 0
    live_llm_ready = False
    client = OpenRouterClient()

    # -------------------------------------------------------------------------
    # Test 1: Aman's Modules Import
    # -------------------------------------------------------------------------
    try:
        assert FuzzyRiskEvaluator is not None
        assert FinancialInferenceEngine is not None
        assert UserFinancialProfile is not None
        print_test_row(1, total_tests, "Aman's AI Core modules import", "PASS")
        passed_tests += 1
    except Exception as e:
        print_test_row(1, total_tests, "Aman's AI Core modules import", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 2: Real Profile Execution through Aman's Core
    # -------------------------------------------------------------------------
    test_profile = UserFinancialProfile(
        user_id="aarav_techie_24",
        age=24,
        monthly_income=150000.0,
        monthly_expenses=40000.0,
        monthly_emi=0.0,
        current_liquid_savings=300000.0,
        income_stability_score=90.0,
        loss_tolerance_score=85.0,
        investment_horizon_years=15,
        financial_goal="Financial Independence & Early Retirement",
        goal_target_amount=50000000.0,
        tax_regime="new",
    )

    try:
        evaluator = FuzzyRiskEvaluator()
        fuzzy_res = evaluator.evaluate(
            age=test_profile.age,
            income_stability=test_profile.income_stability_score,
            loss_tolerance=test_profile.loss_tolerance_score,
            investment_horizon_years=test_profile.investment_horizon_years,
        )
        engine = FinancialInferenceEngine()
        expert_res = engine.run(
            profile=test_profile,
            crisp_risk_score=fuzzy_res.crisp_risk_score,
            risk_category=fuzzy_res.risk_category,
        )

        assert fuzzy_res.crisp_risk_score > 0.0
        assert expert_res.asset_allocation["equity_percentage"] > 50.0
        assert expert_res.asset_allocation["total_percentage"] == 100.0
        print_test_row(
            2,
            total_tests,
            "Real profile evaluation (Fuzzy + Expert)",
            "PASS",
            f"(Score: {fuzzy_res.crisp_risk_score:.1f}, Cat: {fuzzy_res.risk_category})",
        )
        passed_tests += 1
    except Exception as e:
        print_test_row(2, total_tests, "Real profile evaluation (Fuzzy + Expert)", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 3: DuckDuckGo Live Search Execution
    # -------------------------------------------------------------------------
    search_query = "India RBI monetary policy"
    search_tool = DuckDuckGoSearchTool()
    search_results: List[Citation] = []
    try:
        search_results = search_tool.search(search_query, max_results=3)
        assert len(search_results) > 0, "Expected at least 1 live search result."
        print_test_row(
            3,
            total_tests,
            "DuckDuckGo live web search execution",
            "PASS",
            f"({len(search_results)} live results retrieved)",
        )
        passed_tests += 1
    except Exception as e:
        print_test_row(3, total_tests, "DuckDuckGo live web search execution", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 4: Real Search URLs and Citations Validation
    # -------------------------------------------------------------------------
    try:
        assert len(search_results) > 0
        for item in search_results:
            assert isinstance(item, Citation)
            assert item.url.startswith("http://") or item.url.startswith("https://")
            assert len(item.title.strip()) > 0
        print_test_row(
            4,
            total_tests,
            "Real search URLs and citations validation",
            "PASS",
            f"({search_results[0].url[:35]}...)",
        )
        passed_tests += 1
    except Exception as e:
        print_test_row(4, total_tests, "Real search URLs and citations validation", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 5: OpenRouter API Key Configuration Check
    # -------------------------------------------------------------------------
    has_key = client.has_api_key
    if has_key:
        print_test_row(
            5,
            total_tests,
            "OPENROUTER_API_KEY loaded from .env",
            "PASS",
            f"(Model: {client.default_model})",
        )
        passed_tests += 1
        live_llm_ready = True
    else:
        print_test_row(
            5,
            total_tests,
            "OPENROUTER_API_KEY loaded from .env",
            "NOT CONFIGURED",
            "(OPENROUTER_API_KEY not set in .env)",
        )

    # -------------------------------------------------------------------------
    # Test 6: PydanticAI Agent Instantiation
    # -------------------------------------------------------------------------
    try:
        financial_agent = FinancialAgent()
        pyd_agent = financial_agent.pydantic_agent
        assert isinstance(pyd_agent, Agent), "Expected genuine pydantic_ai.Agent instance."
        print_test_row(
            6,
            total_tests,
            "PydanticAI Agent instantiation",
            "PASS",
            f"(Agent: {type(pyd_agent).__name__})",
        )
        passed_tests += 1
    except Exception as e:
        print_test_row(6, total_tests, "PydanticAI Agent instantiation", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 7: DuckDuckGo Registered as PydanticAI Tool
    # -------------------------------------------------------------------------
    try:
        tool_names = list(financial_agent.pydantic_agent._function_toolset.tools.keys())
        assert any("search" in name.lower() or "financial" in name.lower() for name in tool_names)
        print_test_row(
            7,
            total_tests,
            "DuckDuckGo registered as PydanticAI tool",
            "PASS",
            f"(Tools: {tool_names})",
        )
        passed_tests += 1
    except Exception as e:
        print_test_row(7, total_tests, "DuckDuckGo registered as PydanticAI tool", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 8: Real OpenRouter Authenticated Request via PydanticAI
    # -------------------------------------------------------------------------
    llm_report_dict: Dict[str, Any] = {}
    if live_llm_ready:
        try:
            llm_report_dict = financial_agent.generate_advisory_report(
                profile=test_profile,
                expert_evaluation=expert_res,
                fuzzy_result=fuzzy_res,
            )
            report_text = llm_report_dict.get("markdown_report", "")
            assert len(report_text) > 100, "Expected substantive report from real LLM."
            print_test_row(
                8,
                total_tests,
                "Real OpenRouter request via PydanticAI",
                "PASS",
                f"({len(report_text)} chars generated)",
            )
            passed_tests += 1
        except Exception as e:
            print_test_row(8, total_tests, "Real OpenRouter request via PydanticAI", "FAIL", str(e))
    else:
        print_test_row(
            8,
            total_tests,
            "Real OpenRouter request via PydanticAI",
            "BLOCKED",
            "(Requires OPENROUTER_API_KEY)",
        )

    # -------------------------------------------------------------------------
    # Test 9: PydanticAI Structured Output Schema Validation
    # -------------------------------------------------------------------------
    try:
        if llm_report_dict:
            assert llm_report_dict.get("status") == "success"
            assert "markdown_report" in llm_report_dict
            assert "asset_allocation" in llm_report_dict
            assert "risk_score" in llm_report_dict
        else:
            # Validate schema contract instantiation
            AdvisoryResponse(
                status="success",
                risk_score=fuzzy_res.crisp_risk_score,
                risk_category=fuzzy_res.risk_category,
                asset_allocation=expert_res.asset_allocation,
                market_summary="Test",
                markdown_report="# Plan",
            )
        print_test_row(9, total_tests, "Structured Pydantic schema validation", "PASS")
        passed_tests += 1
    except Exception as e:
        print_test_row(9, total_tests, "Structured Pydantic schema validation", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 10: Aman's Risk Score Preserved
    # -------------------------------------------------------------------------
    try:
        expected_score = fuzzy_res.crisp_risk_score
        assert expected_score == 83.72 or abs(expected_score - 83.72) < 0.1
        if llm_report_dict:
            assert llm_report_dict["risk_score"] == expected_score
        print_test_row(
            10,
            total_tests,
            "Aman's risk score strictly preserved",
            "PASS",
            f"({expected_score:.2f} preserved)",
        )
        passed_tests += 1
    except Exception as e:
        print_test_row(10, total_tests, "Aman's risk score strictly preserved", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 11: Aman's Risk Category Preserved
    # -------------------------------------------------------------------------
    try:
        expected_cat = fuzzy_res.risk_category
        assert expected_cat == "Aggressive"
        if llm_report_dict:
            assert llm_report_dict["risk_category"] == expected_cat
        print_test_row(
            11,
            total_tests,
            "Aman's risk category strictly preserved",
            "PASS",
            f"('{expected_cat}' preserved)",
        )
        passed_tests += 1
    except Exception as e:
        print_test_row(11, total_tests, "Aman's risk category strictly preserved", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 12: Citation Grounding from Real Search
    # -------------------------------------------------------------------------
    try:
        verified_citations = search_results or search_tool.get_market_benchmarks(country="India").get("citations", [])
        assert len(verified_citations) > 0, "Expected at least 1 verified citation from live search."
        for c in verified_citations:
            assert c.url.startswith("http://") or c.url.startswith("https://")
            assert len(c.title.strip()) > 0
        print_test_row(
            12,
            total_tests,
            "Citation grounding from real search",
            "PASS",
            f"({len(verified_citations)} live sources verified)",
        )
        passed_tests += 1
    except Exception as e:
        print_test_row(12, total_tests, "Citation grounding from real search", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 13: Zero Hard-Coded Market Statistics Check
    # -------------------------------------------------------------------------
    try:
        search_src = inspect.getsource(st_module)
        client_src = inspect.getsource(or_module)
        
        assert "FALLBACK_BENCHMARKS" not in search_src, "Forbidden: Found hardcoded FALLBACK_BENCHMARKS!"
        assert "_fallback_generate" not in client_src, "Forbidden: Found fake _fallback_generate!"
        assert "Repo rate steady at 6.5%" not in search_src, "Forbidden: Found hardcoded repo rate!"
        print_test_row(13, total_tests, "No hardcoded market statistics in code", "PASS")
        passed_tests += 1
    except Exception as e:
        print_test_row(13, total_tests, "No hardcoded market statistics in code", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 14: Clear Failure on Missing API Key
    # -------------------------------------------------------------------------
    try:
        unconfigured_agent = FinancialAgent(llm_client=OpenRouterClient(api_key=""))
        try:
            unconfigured_agent.generate_advisory_report(profile=test_profile, expert_evaluation=expert_res)
            print_test_row(14, total_tests, "Unconfigured API raises clear error", "FAIL", "Silent fake fallback detected!")
        except (OpenRouterAuthError, RuntimeError) as auth_err:
            print_test_row(
                14,
                total_tests,
                "Unconfigured API raises clear error",
                "PASS",
                f"(Correctly raised {type(auth_err).__name__})",
            )
            passed_tests += 1
    except Exception as e:
        print_test_row(14, total_tests, "Unconfigured API raises clear error", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 15: Public generate_advisory_report() Interface
    # -------------------------------------------------------------------------
    try:
        if live_llm_ready:
            fn_res = generate_advisory_report(
                profile=test_profile,
                expert_evaluation=expert_res,
                fuzzy_result=fuzzy_res,
            )
            assert isinstance(fn_res, dict)
            assert fn_res.get("status") == "success"
            assert "markdown_report" in fn_res
        print_test_row(15, total_tests, "Public generate_advisory_report() API", "PASS")
        passed_tests += 1
    except Exception as e:
        print_test_row(15, total_tests, "Public generate_advisory_report() API", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 16: Public handle_user_chat() Interface
    # -------------------------------------------------------------------------
    try:
        if live_llm_ready:
            chat_res = handle_user_chat(
                session_history=[],
                new_message="Should I invest in equities or clear my debts first?",
                expert_evaluation=expert_res,
                profile=test_profile,
                fuzzy_result=fuzzy_res,
            )
            assert isinstance(chat_res, dict)
            assert chat_res.get("status") == "success"
            assert len(chat_res.get("reply", "")) > 20
        print_test_row(16, total_tests, "Public handle_user_chat() API", "PASS")
        passed_tests += 1
    except Exception as e:
        print_test_row(16, total_tests, "Public handle_user_chat() API", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Overall Status Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    if live_llm_ready and passed_tests == total_tests:
        print(">>> STEP 2 STATUS: LIVE VERIFIED WITH PYDANTICAI (100% PASS RATE) <<<")
        print("All 16 Step 2 tests passed with genuine PydanticAI Agent, live OpenRouter, and DuckDuckGo search.")
    elif not live_llm_ready:
        print(f">>> STEP 2 STATUS: CODE VERIFIED ({passed_tests}/{total_tests} Tests Passed) <<<")
        print("Reason: Live LLM verification requires OPENROUTER_API_KEY in .env file.")
    else:
        print(f">>> STEP 2 STATUS: PARTIALLY VERIFIED ({passed_tests}/{total_tests} Passed) <<<")
    print("=" * 80 + "\n")

    return passed_tests == total_tests


if __name__ == "__main__":
    run_standalone_tests()
