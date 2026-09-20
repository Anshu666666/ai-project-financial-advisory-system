"""
Financial Knowledge Base & Domain Calculations.
Encapsulates mathematical formulas, SEBI/RBI guidelines, budgeting principles, and tax optimization logic.
"""

import math
from typing import Any, Dict, List
from expert_system.rules_catalog import ProductionRule, RuleStatus, RuleTrace, UserFinancialProfile


def calculate_dti(monthly_emi: float, monthly_income: float) -> Dict[str, Any]:
    """
    Calculate Debt-to-Income (DTI) Ratio and health status.
    DTI = (Total Monthly Debt Payments / Gross Monthly Income) * 100
    """
    if monthly_income <= 0:
        return {"dti_ratio": 100.0, "dti_status": "Critical", "recommendation": "Zero income reported."}

    dti = (monthly_emi / monthly_income) * 100.0
    if dti <= 30.0:
        status = "Healthy"
        rec = "DTI is well under the 30% healthy threshold. Surplus cash flow can be allocated directly into growth assets."
    elif dti <= 40.0:
        status = "Moderate"
        rec = "DTI is between 30%-40%. Debt is manageable, but refrain from taking on additional loans before building reserves."
    else:
        status = "High Risk"
        rec = "DTI exceeds 40%. High debt burden poses liquidity risk. Prioritize aggressive debt prepayment before high-risk equity."

    return {
        "dti_ratio": round(dti, 2),
        "dti_status": status,
        "recommendation": rec,
    }


def calculate_emergency_fund(monthly_expenses: float, current_liquid_savings: float) -> Dict[str, Any]:
    """
    Emergency Fund Requirement: 6 months of essential living expenses.
    """
    target = monthly_expenses * 6.0
    shortfall = max(0.0, target - current_liquid_savings)
    surplus = max(0.0, current_liquid_savings - target)

    if current_liquid_savings >= target:
        status = "Adequate"
        rec = f"Emergency buffer is fully funded at INR {current_liquid_savings:,.0f} (Target: INR {target:,.0f}). No emergency top-up needed."
    elif current_liquid_savings >= (monthly_expenses * 3.0):
        status = "Moderate"
        rec = f"Emergency reserve covers {current_liquid_savings / monthly_expenses:.1f} months. Recommend directing INR {shortfall/6:,.0f}/month over 6 months to reach 6-month safety net."
    else:
        status = "Critical Shortfall"
        rec = f"Critical liquidity risk: Current savings of INR {current_liquid_savings:,.0f} cover less than 3 months of expenses. Immediate funding priority."

    return {
        "target_fund": round(target, 2),
        "current_fund": round(current_liquid_savings, 2),
        "shortfall": round(shortfall, 2),
        "surplus": round(surplus, 2),
        "status": status,
        "recommendation": rec,
    }


def calculate_50_30_20_budget(monthly_income: float, monthly_expenses: float, monthly_emi: float) -> Dict[str, Any]:
    """
    Standard 50/30/20 Budgeting Rule Analysis:
    - 50% Needs (Rent, Groceries, Utilities, Minimum EMIs)
    - 30% Wants (Entertainment, Dining, Lifestyle)
    - 20% Savings & Debt Acceleration
    """
    needs_limit = monthly_income * 0.50
    wants_limit = monthly_income * 0.30
    savings_target = monthly_income * 0.20

    total_obligations = monthly_expenses + monthly_emi
    investable_surplus = max(0.0, monthly_income - total_obligations)

    return {
        "needs_allocation": round(needs_limit, 2),
        "wants_allocation": round(wants_limit, 2),
        "savings_allocation": round(savings_target, 2),
        "total_obligations": round(total_obligations, 2),
        "investable_surplus": round(investable_surplus, 2),
    }


def calculate_asset_allocation(
    crisp_risk_score: float,
    risk_category: str,
    investment_horizon_years: int,
    age: int,
) -> Dict[str, float]:
    """
    Deterministic Asset Allocation Matrix strictly summing to 100%.
    Equity %, Debt %, Gold %, Cash % computed based on Fuzzy Risk Score, Horizon, and Age.
    """
    # Cash / Liquid allocation for short term liquidity
    cash = 10.0 if investment_horizon_years <= 3 else 5.0

    # Gold allocation as macro-hedge (5% - 10%)
    gold = 10.0 if risk_category == "Moderate" else 5.0

    # Base equity derived from risk score [0 - 100]
    base_equity = 15.0 + (crisp_risk_score / 100.0) * 65.0

    # Horizon boost/penalty
    if investment_horizon_years >= 10:
        base_equity += 5.0
    elif investment_horizon_years <= 3:
        base_equity -= 15.0

    # Age adjustment (reduce equity past 50)
    if age > 50:
        base_equity -= (age - 50) * 0.8

    # Leave at least 10% room for debt
    max_equity = max(10.0, 100.0 - cash - gold - 10.0)
    equity = max(10.0, min(max_equity, round(base_equity, 1)))

    # Debt / Fixed Income takes the remainder
    debt = round(100.0 - (equity + gold + cash), 1)

    # Clean rounding to guarantee exactly 100.0
    total = round(equity + debt + gold + cash, 1)
    if total != 100.0:
        debt = round(debt + (100.0 - total), 1)

    return {
        "equity_percentage": equity,
        "debt_percentage": debt,
        "gold_percentage": gold,
        "cash_percentage": cash,
        "total_percentage": 100.0,
    }


def calculate_goal_sip(
    target_amount: float,
    horizon_years: int,
    expected_annual_return: float = 0.12,
) -> Dict[str, Any]:
    """
    Compute Required Monthly SIP using Compound Future Value Formula:
    FV = P * [((1 + r)^n - 1) / r] * (1 + r)
    => P = FV / ([((1 + r)^n - 1) / r] * (1 + r))
    """
    if horizon_years <= 0 or target_amount <= 0:
        return {"monthly_sip_required": 0.0, "total_invested": 0.0, "projected_wealth": 0.0}

    n_months = horizon_years * 12
    r_monthly = expected_annual_return / 12.0

    compounding_factor = (((1.0 + r_monthly) ** n_months - 1.0) / r_monthly) * (1.0 + r_monthly)
    monthly_sip = target_amount / compounding_factor
    total_invested = monthly_sip * n_months
    wealth_gain = target_amount - total_invested

    return {
        "target_amount": round(target_amount, 2),
        "horizon_years": horizon_years,
        "expected_cagr_percentage": round(expected_annual_return * 100.0, 1),
        "monthly_sip_required": round(monthly_sip, 2),
        "total_principal_invested": round(total_invested, 2),
        "projected_wealth_gain": round(wealth_gain, 2),
    }


def evaluate_tax_strategy(tax_regime: str, monthly_income: float) -> Dict[str, Any]:
    """
    Tax Optimization Recommendations (Old Regime 80C/80D vs New Regime Section 80CCD(2)).
    """
    annual_income = monthly_income * 12.0
    regime = tax_regime.lower().strip()

    if regime == "new":
        advice = (
            f"Under the New Tax Regime for annual income of INR {annual_income:,.0f}, personal deductions under 80C/80D are forgone for lower tax slab rates. "
            "Maximize Corporate NPS under Section 80CCD(2) (up to 10% or 14% of Basic Salary) for tax-exempt retirement contributions."
        )
    else:
        advice = (
            f"Under the Old Tax Regime for annual income of INR {annual_income:,.0f}, maximize INR 1.5L Section 80C limit (ELSS mutual funds, PPF, EPF), "
            "claim INR 25,000-50,000 under Section 80D for health insurance, and invest INR 50,000 in Section 80CCD(1B) Tier-1 NPS for extra tax shield."
        )

    return {
        "regime_evaluated": regime,
        "advice": advice,
    }


def build_default_rules() -> List[ProductionRule]:
    """
    Builds the production rule set evaluated by the forward chaining inference engine.
    """
    rules: List[ProductionRule] = []

    # Rule 1: DTI High Risk Alert
    def cond_dti_high(wm: Dict[str, Any]) -> bool:
        return wm["dti_analysis"]["dti_ratio"] > 40.0

    def act_dti_high(wm: Dict[str, Any], traces: List[RuleTrace]):
        traces.append(
            RuleTrace(
                rule_id="RULE_DTI_01",
                rule_name="High Debt-to-Income Ratio Alert",
                status=RuleStatus.TRIGGERED,
                condition="DTI > 40.0%",
                priority=10,
                explanation=f"DTI is {wm['dti_analysis']['dti_ratio']:.1f}%, exceeding the safe 40% threshold. Debt restructuring prioritized.",
            )
        )

    rules.append(
        ProductionRule(
            rule_id="RULE_DTI_01",
            name="High Debt-to-Income Ratio Alert",
            condition_description="DTI > 40.0%",
            priority=10,
            condition=cond_dti_high,
            action=act_dti_high,
        )
    )

    # Rule 2: Emergency Fund Deficit
    def cond_ef_shortfall(wm: Dict[str, Any]) -> bool:
        return wm["emergency_fund"]["shortfall"] > 0

    def act_ef_shortfall(wm: Dict[str, Any], traces: List[RuleTrace]):
        shortfall = wm["emergency_fund"]["shortfall"]
        traces.append(
            RuleTrace(
                rule_id="RULE_EMERGENCY_02",
                rule_name="Emergency Reserve Deficit Alert",
                status=RuleStatus.TRIGGERED,
                condition="Current Savings < 6 * Monthly Expenses",
                priority=20,
                explanation=f"Emergency fund has a shortfall of INR {shortfall:,.0f}. Monthly cash flow must fund liquid safety net first.",
            )
        )

    rules.append(
        ProductionRule(
            rule_id="RULE_EMERGENCY_02",
            name="Emergency Reserve Deficit Alert",
            condition_description="Current Savings < 6 * Monthly Expenses",
            priority=20,
            condition=cond_ef_shortfall,
            action=act_ef_shortfall,
        )
    )

    # Rule 3: Aggressive Growth Portfolio Rule
    def cond_agg_growth(wm: Dict[str, Any]) -> bool:
        return (
            wm.get("risk_category") == "Aggressive"
            and wm["profile"].investment_horizon_years >= 7
        )

    def act_agg_growth(wm: Dict[str, Any], traces: List[RuleTrace]):
        traces.append(
            RuleTrace(
                rule_id="RULE_ALLOC_03",
                rule_name="Aggressive Long-Term Equity Compounding",
                status=RuleStatus.TRIGGERED,
                condition="Risk == 'Aggressive' AND Horizon >= 7 years",
                priority=30,
                explanation=f"High risk appetite with {wm['profile'].investment_horizon_years}-year horizon warrants high equity allocation ({wm['asset_allocation']['equity_percentage']}%).",
            )
        )

    rules.append(
        ProductionRule(
            rule_id="RULE_ALLOC_03",
            name="Aggressive Long-Term Equity Compounding",
            condition_description="Risk == 'Aggressive' AND Horizon >= 7 years",
            priority=30,
            condition=cond_agg_growth,
            action=act_agg_growth,
        )
    )

    # Rule 4: Conservative Capital Preservation Rule
    def cond_cons_preservation(wm: Dict[str, Any]) -> bool:
        return (
            wm.get("risk_category") == "Conservative"
            or wm["profile"].investment_horizon_years <= 3
        )

    def act_cons_preservation(wm: Dict[str, Any], traces: List[RuleTrace]):
        traces.append(
            RuleTrace(
                rule_id="RULE_ALLOC_04",
                rule_name="Capital Preservation & High Fixed Income Rule",
                status=RuleStatus.TRIGGERED,
                condition="Risk == 'Conservative' OR Horizon <= 3 years",
                priority=35,
                explanation=f"Short horizon or conservative risk profile demands fixed income & debt focus ({wm['asset_allocation']['debt_percentage']}% debt + {wm['asset_allocation']['cash_percentage']}% cash).",
            )
        )

    rules.append(
        ProductionRule(
            rule_id="RULE_ALLOC_04",
            name="Capital Preservation & High Fixed Income Rule",
            condition_description="Risk == 'Conservative' OR Horizon <= 3 years",
            priority=35,
            condition=cond_cons_preservation,
            action=act_cons_preservation,
        )
    )

    # Rule 5: Goal SIP Solvency Check
    def cond_sip_check(wm: Dict[str, Any]) -> bool:
        required_sip = wm["sip_calculation"]["monthly_sip_required"]
        surplus = wm["budget_breakdown"]["investable_surplus"]
        return required_sip > surplus and required_sip > 0

    def act_sip_check(wm: Dict[str, Any], traces: List[RuleTrace]):
        req = wm["sip_calculation"]["monthly_sip_required"]
        surplus = wm["budget_breakdown"]["investable_surplus"]
        traces.append(
            RuleTrace(
                rule_id="RULE_SIP_05",
                rule_name="Goal SIP Cash Flow Shortfall Alert",
                status=RuleStatus.TRIGGERED,
                condition="Required Goal SIP > Investable Monthly Surplus",
                priority=40,
                explanation=f"Target goal requires INR {req:,.0f}/mo SIP, but current monthly surplus is INR {surplus:,.0f}/mo. Recommend extending horizon or trimming discretionary expenses.",
            )
        )

    rules.append(
        ProductionRule(
            rule_id="RULE_SIP_05",
            name="Goal SIP Cash Flow Shortfall Alert",
            condition_description="Required Goal SIP > Investable Monthly Surplus",
            priority=40,
            condition=cond_sip_check,
            action=act_sip_check,
        )
    )

    return rules
