"""
================================================================================
FINWISE AI – GROUNDED PROMPT TEMPLATES & SYSTEM DIRECTIVES
Author: Zaid (Intelligent Agent & Web Search Lead)
================================================================================
Defines strict system instructions and formatting templates for the LLM.
Ensures zero hallucinations, strict fidelity to the Expert System's deterministic
calculations, and explicit citation of actual web search URLs and rule audit traces.
================================================================================
"""

from typing import Any, Dict, List
from agent.schemas import Citation


ADVISORY_SYSTEM_PROMPT = """You are FinWise AI, an advanced Hybrid Intelligent Financial Advisory Agent.
Your role is to act as a certified, highly articulate, and objective financial advisor.

CRITICAL INSTRUCTIONS & GUARDRAILS:
1. MATHEMATICAL FIDELITY & DETERMINISTIC AI CORE:
   - You must NEVER alter, recalculate, or contradict the numbers provided by the Rule-Based Expert System and Fuzzy Logic Evaluator.
   - Treat the supplied Risk Score and Risk Category as AUTHORITATIVE. Do not change or recalculate them.
   - Use the EXACT Asset Allocation percentages provided (Equity %, Debt %, Gold %, Cash %). They sum to 100%.
   - Use the EXACT Emergency Fund status, shortfall, and months covered.
   - Use the EXACT Debt-to-Income (DTI) ratio.
   - Use the EXACT 50/30/20 Budgeting allocations and Monthly SIP calculations.
2. EXPLAINABILITY & RULE AUDIT TRACE:
   - When explaining financial advice, explicitly cite the triggered Expert System Rule IDs (e.g. `[RULE_DTI_01]`, `[RULE_EMERGENCY_02]`, `[RULE_ALLOC_03]`).
   - Clearly explain WHY the rule fired based on the user's factual telemetry.
3. LIVE WEB CITATIONS & REAL DATA:
   - Incorporate the provided real-time market search snippets to contextualize interest rates, inflation, and market trends.
   - Use the EXACT URLs and source names provided in the search citations.
   - NEVER fabricate, invent, or hallucinate URLs or current financial statistics.
   - If a current macroeconomic statistic or rate was not found in the search results, explicitly state: "Current data could not be verified from available sources."
4. STRUCTURED ADVISORY REPORT:
   Produce a comprehensive, beautifully formatted Markdown report with the following sections:
   - # Comprehensive Financial Advisory Plan for {user_name}
   - ### 1. Executive Summary & Fuzzy Risk Profiling (Authoritative Score & Category)
   - ### 2. Immediate Cash Flow & Debt Health (Triggered Expert Rules & Rationale)
   - ### 3. Recommended Asset Allocation & Goal Strategy (Exact 100% Portfolio Breakdown)
   - ### 4. Macroeconomic Environment & Live Market Intelligence (With Real Citations)
   - ### 5. Actionable Implementation Roadmap (Immediate Priorities vs. Long-Term Plan)
   - *Disclaimer: For educational and informational purposes only. FinWise AI is not a SEBI/SEC licensed financial advisor.*
"""


def build_advisory_prompt(
    profile: Dict[str, Any],
    expert_eval: Dict[str, Any],
    market_intel: Dict[str, Any],
) -> List[Dict[str, str]]:
    """
    Constructs the grounded user message payload for the OpenRouter LLM.
    """
    user_name = profile.get("user_id", profile.get("user_name", "Investor"))
    age = profile.get("age", 30)
    monthly_income = profile.get("monthly_income", 0.0)
    monthly_expenses = profile.get("monthly_expenses", 0.0)
    monthly_emi = profile.get("monthly_emi", 0.0)
    current_liquid_savings = profile.get("current_liquid_savings", 0.0)
    horizon = profile.get("investment_horizon_years", 5)
    goal = profile.get("financial_goal", "Wealth Creation")
    goal_target = profile.get("goal_target_amount", 0.0)
    tax_regime = profile.get("tax_regime", "new")

    # Expert System telemetry (authoritative)
    fuzzy_score = expert_eval.get("fuzzy_risk_score", 50.0)
    risk_cat = expert_eval.get("risk_category", "Moderate")
    fuzzy_rationale = expert_eval.get("fuzzy_rationale", "Calibrated risk evaluation.")
    
    alloc = expert_eval.get("asset_allocation", {})
    dti = expert_eval.get("debt_analysis", {})
    ef = expert_eval.get("emergency_fund", {})
    budget = expert_eval.get("budget_breakdown", {})
    sip = expert_eval.get("sip_calculation", {})
    rules_fired = expert_eval.get("rules_fired", [])

    # Web search intelligence
    market_summary = market_intel.get("market_summary", "No live market summary available.")
    citations = market_intel.get("citations", [])
    
    citations_text = ""
    if citations:
        for idx, c in enumerate(citations, 1):
            if isinstance(c, Citation):
                citations_text += f"[{idx}] Title: {c.title}\n    Source: {c.source}\n    URL: {c.url}\n    Snippet: {c.snippet}\n\n"
            elif isinstance(c, dict):
                citations_text += f"[{idx}] Title: {c.get('title', '')}\n    Source: {c.get('source', '')}\n    URL: {c.get('url', '')}\n    Snippet: {c.get('snippet', '')}\n\n"
    else:
        citations_text = "No live web citations available for this session. (State that current data could not be verified from available sources if discussing macro numbers).\n"

    rules_text = ""
    for r in rules_fired:
        rules_text += f"- [{r.get('rule_id', 'RULE')}] {r.get('title', '')} (Severity: {r.get('severity', 'INFO')}): {r.get('explanation', '')}\n"
    if not rules_text:
        rules_text = "No critical alerts triggered; cash flow baseline is healthy.\n"

    user_payload = f"""
================================================================================
INPUT PROFILE FACTS (VERIFIED):
================================================================================
- User ID / Name: {user_name}
- Age: {age} years
- Monthly Net Income: INR {monthly_income:,.2f}
- Monthly Living Expenses: INR {monthly_expenses:,.2f}
- Monthly Existing EMI: INR {monthly_emi:,.2f}
- Current Liquid Savings: INR {current_liquid_savings:,.2f}
- Investment Horizon: {horizon} years
- Primary Financial Goal: {goal} (Target: INR {goal_target:,.2f})
- Tax Regime: {tax_regime.upper()}

================================================================================
AUTHORITATIVE DETERMINISTIC AI CORE (DO NOT MODIFY NUMBERS):
================================================================================
1. Mamdani Fuzzy Risk Score: {fuzzy_score:.2f} / 100.0 -> Category: {risk_cat}
   Rationale: {fuzzy_rationale}

2. Debt-to-Income (DTI) Analysis:
   - DTI Ratio: {dti.get('dti_ratio', 0.0):.1f}%
   - Status: {dti.get('dti_status', 'Healthy')}
   - Recommendation: {dti.get('recommendation', '')}

3. Emergency Fund Analysis:
   - Current Fund: INR {ef.get('current_fund', 0.0):,.2f}
   - Target 6-Month Baseline: INR {ef.get('target_fund', 0.0):,.2f}
   - Shortfall: INR {ef.get('shortfall', 0.0):,.2f}
   - Months Covered: {ef.get('months_covered', 0.0):.1f} months ({ef.get('status', 'Adequate')})
   - Recommendation: {ef.get('recommendation', '')}

4. 50/30/20 Budgeting Breakdown:
   - Needs Allocation (50% max): INR {budget.get('needs_allocation', 0.0):,.2f}
   - Wants Allocation (30% max): INR {budget.get('wants_allocation', 0.0):,.2f}
   - Savings Allocation (20% min): INR {budget.get('savings_allocation', 0.0):,.2f}
   - Actual Monthly Investable Surplus: INR {budget.get('investable_surplus', 0.0):,.2f}

5. Deterministic Asset Allocation (Sums to 100%):
   - Equity / Index Funds: {alloc.get('equity_percentage', 0.0):.1f}%
   - Debt / Fixed Income: {alloc.get('debt_percentage', 0.0):.1f}%
   - Gold / Commodities: {alloc.get('gold_percentage', 0.0):.1f}%
   - Liquid Cash: {alloc.get('cash_percentage', 0.0):.1f}%
   - Total Portfolio Sum: {alloc.get('total_percentage', 100.0):.1f}%

6. Goal Compounding SIP Requirement:
   - Required Monthly SIP: INR {sip.get('monthly_sip_required', 0.0):,.2f}
   - Expected Annual Rate of Return: {sip.get('expected_annual_return_pct', 0.0):.1f}%
   - Target Goal Amount: INR {sip.get('target_amount', 0.0):,.2f} in {sip.get('horizon_years', horizon)} years

7. Triggered Expert Production Rules & Audit Trace:
{rules_text}

================================================================================
REAL-TIME WEB SEARCH MARKET INTELLIGENCE & ACTUAL CITATIONS:
================================================================================
Search Context: {market_summary}

Actual Retrieved Web Sources:
{citations_text}

Synthesize the final Comprehensive Advisory Plan following all instructions and formatting rules.
"""

    return [
        {"role": "system", "content": ADVISORY_SYSTEM_PROMPT.format(user_name=user_name)},
        {"role": "user", "content": user_payload},
    ]


CHAT_SYSTEM_PROMPT = """You are FinWise AI's interactive financial advisory assistant.
You are answering follow-up questions from the user regarding their active financial advisory plan.

GUARDRAILS:
1. Ground your answers strictly in the user's verified Expert System facts, asset allocation, and fired rules.
2. If the user asks whether they should invest in high-risk assets (like crypto or penny stocks) while having high debt or an inadequate emergency fund, cite the appropriate rules (e.g. `RULE_DTI_01`, `RULE_EMERGENCY_02`) and explain why debt elimination or emergency reserve must take mathematical priority.
3. If citing external macroeconomic factors, use ONLY the provided real search sources with their actual URLs. Do not fabricate citations or current rates.
4. Keep the tone professional, objective, encouraging, and educational.
5. End with standard educational disclaimer.
"""


def build_chat_prompt(
    session_history: List[Dict[str, str]],
    new_message: str,
    expert_eval: Dict[str, Any],
    profile: Dict[str, Any],
    market_intel: Dict[str, Any],
) -> List[Dict[str, str]]:
    """
    Builds conversational chat prompt with session context and expert rules.
    """
    user_name = profile.get("user_id", profile.get("user_name", "Investor"))
    rules_fired = expert_eval.get("rules_fired", [])
    alloc = expert_eval.get("asset_allocation", {})
    dti = expert_eval.get("debt_analysis", {})
    ef = expert_eval.get("emergency_fund", {})
    risk_cat = expert_eval.get("risk_category", "Moderate")

    rules_summary = ", ".join([f"`{r.get('rule_id', '')}`: {r.get('title', '')}" for r in rules_fired]) or "None"

    context_header = (
        f"Active Investor Profile: {user_name} (Risk Tier: {risk_cat})\n"
        f"Key Metrics: DTI = {dti.get('dti_ratio', 0.0):.1f}%, Emergency Fund Shortfall = INR {ef.get('shortfall', 0.0):,.0f}\n"
        f"Asset Allocation: Equity {alloc.get('equity_percentage', 0.0):.1f}%, Debt {alloc.get('debt_percentage', 0.0):.1f}%, Gold {alloc.get('gold_percentage', 0.0):.1f}%, Cash {alloc.get('cash_percentage', 0.0):.1f}%\n"
        f"Triggered Rules: {rules_summary}\n"
    )

    citations = market_intel.get("citations", [])
    citations_context = ""
    if citations:
        citations_context = "\nReal Web Search Results for this query:\n"
        for c in citations:
            if isinstance(c, Citation):
                citations_context += f"- Title: {c.title} | URL: {c.url} | Snippet: {c.snippet}\n"
            elif isinstance(c, dict):
                citations_context += f"- Title: {c.get('title', '')} | URL: {c.get('url', '')} | Snippet: {c.get('snippet', '')}\n"

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": f"{CHAT_SYSTEM_PROMPT}\n\nCURRENT ACTIVE PLAN CONTEXT:\n{context_header}{citations_context}"}
    ]

    # Append session history (last 6 exchanges max)
    for msg in session_history[-6:]:
        messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", ""),
        })

    # Append new user message
    messages.append({
        "role": "user",
        "content": f"Follow-up Question: {new_message}",
    })

    return messages
