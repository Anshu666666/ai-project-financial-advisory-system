"""
================================================================================
FINWISE AI – BACKEND SCHEMAS & VALIDATION MODELS
Author: Anshuman (Core Backend & API Orchestration Lead)
================================================================================
Strict Pydantic models conforming to docs/API_CONTRACTS.md for API payload
validation, serialization, and type safety across all endpoints.
================================================================================
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


# ==============================================================================
# 1. EVALUATION REQUEST & INPUT VALIDATION
# ==============================================================================

class EvaluateRequest(BaseModel):
    """
    Client input payload sent to POST /api/v1/advisory/evaluate.
    Strictly validates user financial metrics and parameters.
    """
    user_name: str = Field(
        default="Valued Investor",
        min_length=1,
        max_length=100,
        description="Name of the user",
        examples=["Aarav Sharma"]
    )
    age: int = Field(
        ...,
        ge=18,
        le=100,
        description="User age in years (18 to 100)",
        examples=[24]
    )
    monthly_income: float = Field(
        ...,
        gt=0,
        description="Gross monthly income in INR",
        examples=[65000.0]
    )
    monthly_expenses: float = Field(
        ...,
        ge=0,
        description="Fixed essential monthly living expenses in INR",
        examples=[32000.0]
    )
    current_savings: float = Field(
        default=0.0,
        ge=0,
        description="Current liquid emergency savings in INR",
        examples=[45000.0]
    )
    total_debt: float = Field(
        default=0.0,
        ge=0,
        description="Total outstanding debt principal in INR",
        examples=[120000.0]
    )
    monthly_emi: float = Field(
        default=0.0,
        ge=0,
        description="Total monthly debt payments / EMIs in INR",
        examples=[5000.0]
    )
    debt_interest_rate: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Highest annual interest rate on existing debt in percent",
        examples=[11.5]
    )
    investment_horizon_years: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Target investment time horizon in years",
        examples=[5]
    )
    loss_tolerance: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Self-reported tolerance to short-term portfolio drawdowns",
        examples=["medium"]
    )
    income_stability: Literal["unstable", "moderate", "stable"] = Field(
        default="stable",
        description="Perceived stability and predictability of income stream",
        examples=["stable"]
    )
    primary_goal: str = Field(
        default="wealth_creation",
        description="Primary financial aspiration or target",
        examples=["wealth_creation"]
    )
    goal_target_amount: float = Field(
        default=0.0,
        ge=0,
        description="Target wealth amount for primary goal in INR",
        examples=[1000000.0]
    )
    tax_regime: Literal["old", "new"] = Field(
        default="new",
        description="Active income tax regime (old or new)",
        examples=["new"]
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional user context, preferences, or constraints",
        examples=["Interested in tech stocks and building an emergency buffer."]
    )

    @field_validator("monthly_emi")
    @classmethod
    def validate_emi_against_income(cls, v: float, info) -> float:
        income = info.data.get("monthly_income")
        if income and v > income:
            # We don't crash, but it will be flagged as critical debt stress
            pass
        return v


# ==============================================================================
# 2. EVALUATION RESPONSE SUB-MODELS
# ==============================================================================

class ProfileSummary(BaseModel):
    """Normalized high-level overview of the user's cash flow."""
    user_name: str
    age: int
    monthly_income: float
    monthly_expenses: float
    monthly_emi: float
    net_monthly_savings: float
    emergency_fund_months_covered: float
    dti_ratio: float


class FuzzyRiskAssessment(BaseModel):
    """Output from Aman's Fuzzy Logic Engine."""
    crisp_score: float = Field(description="Defuzzified risk appetite score from 0.0 to 100.0")
    category: str = Field(description="Linguistic category: Conservative, Moderate, or Aggressive")
    fuzzy_memberships: Dict[str, float] = Field(description="Degree of membership in each fuzzy set")
    reasoning: str = Field(description="Linguistic explanation of fuzzy inference firing")


class RuleFired(BaseModel):
    """Detailed audit trace for a specific production rule that fired."""
    rule_id: str
    title: str
    severity: Literal["INFO", "MEDIUM", "HIGH", "CRITICAL"]
    explanation: str


class RecommendedAllocation(BaseModel):
    """Deterministic asset allocation percentages strictly summing to 100%."""
    equity_percentage: float
    debt_bonds_percentage: float
    gold_commodities_percentage: float
    liquid_cash_percentage: float
    total_percentage: float = 100.0


class BudgetRuleCheck(BaseModel):
    """50/30/20 Budgeting Rule Analysis."""
    needs_ratio: float
    wants_ratio: float
    savings_ratio: float
    investable_surplus: float
    status: str


class ExpertSystemPlan(BaseModel):
    """Output from Aman's Rule-Based Expert System."""
    recommended_allocation: RecommendedAllocation
    budget_rule_check: BudgetRuleCheck
    actionable_rules_fired: List[RuleFired]
    dti_status: str
    emergency_fund_status: str
    monthly_sip_required: float
    tax_advice: str


class WebCitation(BaseModel):
    """Verified live web search citation with source URL and snippet."""
    title: str
    source: str
    url: str
    snippet: str


class AgentMarketIntelligence(BaseModel):
    """Output from Zaid's real-time Web Search & Market Context Tool."""
    market_summary: str
    web_citations: List[WebCitation]


class EvaluateResponse(BaseModel):
    """
    Complete response payload returned by POST /api/v1/advisory/evaluate.
    Strictly conforms to API Contracts Section 1.1.
    """
    status: Literal["success", "error"] = "success"
    session_id: str
    profile_summary: ProfileSummary
    fuzzy_risk_assessment: FuzzyRiskAssessment
    expert_system_plan: ExpertSystemPlan
    agent_market_intelligence: AgentMarketIntelligence
    comprehensive_advisory_report: str


# ==============================================================================
# 3. CONVERSATIONAL CHAT SCHEMAS
# ==============================================================================

class ChatRequest(BaseModel):
    """Payload for POST /api/v1/advisory/chat."""
    session_id: str = Field(..., min_length=5, description="Active session ID from evaluation")
    message: str = Field(..., min_length=1, max_length=1000, description="User follow-up question")


class ChatResponse(BaseModel):
    """Response payload for POST /api/v1/advisory/chat."""
    status: Literal["success", "error"] = "success"
    session_id: str
    reply: str
    grounded_rules_referenced: List[str] = []
    sources_used: List[WebCitation] = []


# ==============================================================================
# 4. SESSION & HISTORY SCHEMAS
# ==============================================================================

class ChatMessageItem(BaseModel):
    id: int
    session_id: str
    role: Literal["user", "assistant"]
    message: str
    timestamp: str


class SessionDetailResponse(BaseModel):
    session_id: str
    created_at: str
    user_name: str
    profile: Dict[str, Any]
    fuzzy_assessment: Dict[str, Any]
    expert_plan: Dict[str, Any]
    advisory_report: str
    chat_history: List[ChatMessageItem]


class SessionListItem(BaseModel):
    session_id: str
    user_name: str
    risk_category: str
    created_at: str
