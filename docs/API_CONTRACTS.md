# 🔌 Interface & API Contracts

This document establishes the exact JSON contracts between the frontend and backend, as well as the internal Python contracts between the Backend Orchestrator (Person 2), the LLM Agent (Person 3), and the Expert System (Person 4).

---

## 1. Client-to-Backend HTTP Endpoints

### 1.1 `POST /api/v1/advisory/evaluate`
Triggers the full financial evaluation: runs Fuzzy Risk Profiling, Expert System rules, live Web Search, and LLM advisory synthesis.

#### Request Payload
```json
{
  "user_name": "Aarav Sharma",
  "age": 24,
  "monthly_income": 65000.0,
  "monthly_expenses": 32000.0,
  "current_savings": 45000.0,
  "total_debt": 120000.0,
  "debt_interest_rate": 11.5,
  "investment_horizon_years": 5,
  "loss_tolerance": "medium",
  "primary_goal": "wealth_creation",
  "notes": "Interested in tech stocks and building an emergency buffer."
}
```

#### Response Payload
```json
{
  "status": "success",
  "session_id": "sess_9823f4a1",
  "profile_summary": {
    "age": 24,
    "net_monthly_savings": 33000.0,
    "emergency_fund_months_covered": 1.41
  },
  "fuzzy_risk_assessment": {
    "crisp_score": 68.5,
    "category": "Moderate Growth",
    "fuzzy_memberships": {
      "conservative": 0.15,
      "moderate": 0.70,
      "aggressive": 0.15
    },
    "reasoning": "Young age and 5-year horizon support growth, but existing 11.5% interest debt softens risk appetite."
  },
  "expert_system_plan": {
    "recommended_allocation": {
      "equity_percentage": 55.0,
      "debt_bonds_percentage": 25.0,
      "gold_commodities_percentage": 5.0,
      "liquid_cash_percentage": 15.0
    },
    "budget_rule_check": {
      "needs_ratio": 49.2,
      "wants_ratio": 0.0,
      "savings_ratio": 50.8,
      "status": "Healthy (Needs under 50%)"
    },
    "actionable_rules_fired": [
      {
        "rule_id": "RULE_EMERGENCY_DEFICIT",
        "title": "Emergency Fund Deficit Detected",
        "severity": "HIGH",
        "explanation": "Current liquid savings cover only 1.4 months of expenses. Target is 6 months (₹1,92,000). Priority 1 is building this reserve."
      },
      {
        "rule_id": "RULE_HIGH_INTEREST_DEBT_AVALANCHE",
        "title": "High Interest Debt Warning",
        "severity": "CRITICAL",
        "explanation": "Existing debt carries an 11.5% interest rate, exceeding standard market returns. Direct 40% of surplus savings toward debt payoff."
      },
      {
        "rule_id": "RULE_AGE_BASED_EQUITY_CAP",
        "title": "Equity Exposure Governed by Horizon",
        "severity": "INFO",
        "explanation": "5-year horizon permits maximum 55% equity index exposure to cushion potential drawdown."
      }
    ]
  },
  "agent_market_intelligence": {
    "market_summary": "Current benchmark interest rates are stable; domestic indices are near historical valuations, making systematic SIPs preferable to lump sum.",
    "web_citations": [
      {
        "source": "RBI / Reserve Bank Policy Bulletin",
        "snippet": "Repo rate steady at 6.5%, retail inflation within target band."
      },
      {
        "source": "Market Index Overview",
        "snippet": "Index PE ratio trading around 22.1x; long-term DCA strategy suggested."
      }
    ]
  },
  "comprehensive_advisory_report": "# Comprehensive Financial Plan for Aarav\n\n### 1. Immediate Action Plan\nYour first financial imperative is **building your emergency cushion** and attacking the **₹1,20,000 debt** with its 11.5% interest rate...\n\n### 2. Suggested Asset Allocation\n- **Equity Index Funds**: 55%\n- **Short-term Debt / Liquid Funds**: 25%\n- **Gold ETF**: 5%\n- **Emergency High-Yield Bank Savings**: 15%\n\n*Disclaimer: For educational use only.*"
}
```

---

### 1.2 `POST /api/v1/advisory/chat`
Allows the user to ask follow-up questions grounded in their active financial plan.

#### Request Payload
```json
{
  "session_id": "sess_9823f4a1",
  "message": "Should I invest in crypto or pay off my 11.5% debt first?"
}
```

#### Response Payload
```json
{
  "session_id": "sess_9823f4a1",
  "reply": "Based on your financial plan and the expert rule `RULE_HIGH_INTEREST_DEBT_AVALANCHE`, you should **strongly prioritize paying off your 11.5% debt first**.\n\nA guaranteed 11.5% return from debt elimination far outperforms volatile asset speculation. Once your high-interest debt is cleared and your 6-month emergency reserve is filled, a tiny speculative allocation (under 5%) can be considered.",
  "grounded_rules_referenced": ["RULE_HIGH_INTEREST_DEBT_AVALANCHE"],
  "sources_used": []
}
```

---

## 2. Internal Python Module Contracts

### 2.1 Person 4 (Expert & Fuzzy Engine) $\rightarrow$ Person 2 (Backend Orchestrator)

```python
# Signature in backend/expert_system/engine.py
def evaluate_financial_profile(profile: dict) -> dict:
    """
    Evaluates profile through Fuzzy Logic and Forward-Chaining Rules.
    
    Args:
        profile: Dictionary matching FinancialProfileSchema
        
    Returns:
        dict containing:
            - 'fuzzy_risk_score': float (0-100)
            - 'risk_category': str ('Conservative' | 'Moderate' | 'Aggressive')
            - 'recommended_allocation': dict (equity, debt, gold, cash)
            - 'rules_fired': list[dict] (rule_id, title, severity, explanation)
            - 'budget_metrics': dict (needs, wants, savings ratios)
    """
```

### 2.2 Person 3 (Intelligent Agent & Search) $\rightarrow$ Person 2 (Backend Orchestrator)

```python
# Signature in backend/agent/financial_agent.py
def generate_advisory_report(profile: dict, expert_evaluation: dict) -> dict:
    """
    Triggers web search for market benchmarks and synthesizes final natural language plan.
    
    Args:
        profile: User profile dictionary
        expert_evaluation: Output from Person 4's evaluate_financial_profile
        
    Returns:
        dict containing:
            - 'market_summary': str
            - 'citations': list[dict]
            - 'markdown_report': str
    """

def handle_user_chat(session_history: list, new_message: str, expert_evaluation: dict) -> dict:
    """
    Answers follow-up conversational queries grounded in expert plan.
    """
```
