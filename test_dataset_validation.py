"""
================================================================================
FINWISE AI – COMPREHENSIVE DATASET VALIDATION RUNNER
Author: Aman (AI Core & Deterministic Reasoning Lead)
================================================================================
Evaluates the Fuzzy Logic Risk Evaluator and Rule-Based Expert System across
a comprehensive dataset of 8 real-world financial profiles and edge cases.
================================================================================
"""

import sys

# Configure UTF-8 encoding safely for Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from typing import List
from expert_system import (
    FinancialInferenceEngine,
    RuleStatus,
    UserFinancialProfile,
)
from fuzzy_logic import FuzzyRiskEvaluator


# 8 Diverse Real-World Financial Dataset Profiles
DATASET: List[UserFinancialProfile] = [
    # 1. Young Freelancer / Early Career
    UserFinancialProfile(
        user_id="USR_01_FREELANCER",
        age=22,
        monthly_income=35000.0,
        monthly_expenses=20000.0,
        monthly_emi=0.0,
        current_liquid_savings=15000.0,
        income_stability_score=40.0,
        loss_tolerance_score=75.0,
        investment_horizon_years=12,
        financial_goal="Long-term Wealth Building",
        goal_target_amount=10000000.0,
        tax_regime="new",
    ),
    # 2. High-Earning Tech Engineer
    UserFinancialProfile(
        user_id="USR_02_TECH_DEV",
        age=27,
        monthly_income=180000.0,
        monthly_expenses=50000.0,
        monthly_emi=25000.0,
        current_liquid_savings=400000.0,
        income_stability_score=90.0,
        loss_tolerance_score=85.0,
        investment_horizon_years=15,
        financial_goal="Early Retirement & Startup Fund",
        goal_target_amount=50000000.0,
        tax_regime="new",
    ),
    # 3. Double-Income Family with Heavy Home Loan EMI (High DTI)
    UserFinancialProfile(
        user_id="USR_03_HOME_LOAN_FAMILY",
        age=38,
        monthly_income=250000.0,
        monthly_expenses=90000.0,
        monthly_emi=110000.0,  # DTI = 44% -> High Risk
        current_liquid_savings=300000.0,  # Target: 6 * 90k = 540k (Deficit: 240k)
        income_stability_score=70.0,
        loss_tolerance_score=50.0,
        investment_horizon_years=8,
        financial_goal="Child Higher Education & Loan Prepayment",
        goal_target_amount=8000000.0,
        tax_regime="old",
    ),
    # 4. Single Earner on Tight Budget with Zero Savings
    UserFinancialProfile(
        user_id="USR_04_TIGHT_BUDGET",
        age=34,
        monthly_income=60000.0,
        monthly_expenses=45000.0,
        monthly_emi=10000.0,
        current_liquid_savings=5000.0,
        income_stability_score=50.0,
        loss_tolerance_score=25.0,
        investment_horizon_years=4,
        financial_goal="Emergency Buffer & Debt Freedom",
        goal_target_amount=1500000.0,
        tax_regime="new",
    ),
    # 5. Established Business Owner / High Net Worth
    UserFinancialProfile(
        user_id="USR_05_ENTREPRENEUR",
        age=48,
        monthly_income=600000.0,
        monthly_expenses=150000.0,
        monthly_emi=30000.0,
        current_liquid_savings=2500000.0,
        income_stability_score=75.0,
        loss_tolerance_score=70.0,
        investment_horizon_years=10,
        financial_goal="Intergenerational Wealth Transfer",
        goal_target_amount=100000000.0,
        tax_regime="old",
    ),
    # 6. Near-Retirement Senior Corporate Executive
    UserFinancialProfile(
        user_id="USR_06_PRE_RETIREE",
        age=58,
        monthly_income=320000.0,
        monthly_expenses=80000.0,
        monthly_emi=10000.0,
        current_liquid_savings=3500000.0,
        income_stability_score=85.0,
        loss_tolerance_score=20.0,
        investment_horizon_years=2,
        financial_goal="Capital Preservation & Post-Retirement Annuity",
        goal_target_amount=25000000.0,
        tax_regime="new",
    ),
    # 7. Senior Citizen / Pensioner
    UserFinancialProfile(
        user_id="USR_07_PENSIONER",
        age=68,
        monthly_income=80000.0,
        monthly_expenses=50000.0,
        monthly_emi=0.0,
        current_liquid_savings=1800000.0,
        income_stability_score=95.0,
        loss_tolerance_score=10.0,
        investment_horizon_years=1,
        financial_goal="Healthcare Reserve & Regular Income",
        goal_target_amount=2000000.0,
        tax_regime="new",
    ),
    # 8. Severe Debt Stress / 50% DTI
    UserFinancialProfile(
        user_id="USR_08_CRITICAL_DEBT",
        age=29,
        monthly_income=50000.0,
        monthly_expenses=35000.0,
        monthly_emi=25000.0,  # 50% DTI, Deficit Cashflow
        current_liquid_savings=0.0,
        income_stability_score=40.0,
        loss_tolerance_score=35.0,
        investment_horizon_years=3,
        financial_goal="Debt Liquidation",
        goal_target_amount=1000000.0,
        tax_regime="new",
    ),
]


def run_dataset_validation():
    print("\n" + "=" * 110)
    print("FINWISE AI – COMPREHENSIVE MULTI-PROFILE DATASET VALIDATION (8 PROFILES)")
    print("=" * 110)

    fuzzy_evaluator = FuzzyRiskEvaluator()
    inference_engine = FinancialInferenceEngine()

    passed_count = 0
    total_profiles = len(DATASET)

    # Table Header
    print(f"{'User ID':<24} | {'Age':<3} | {'Income (INR)':<12} | {'Risk Cat':<12} | {'Risk Score':<10} | {'DTI':<7} | {'Equity%':<7} | {'Debt%':<6} | {'Gold%':<5} | {'Cash%':<5} | {'Status'}")
    print("-" * 110)

    for profile in DATASET:
        # 1. Fuzzy Evaluation
        fuzzy_res = fuzzy_evaluator.evaluate(
            age=profile.age,
            income_stability=profile.income_stability_score,
            loss_tolerance=profile.loss_tolerance_score,
            investment_horizon_years=profile.investment_horizon_years,
        )

        # 2. Expert System Forward Chaining
        expert_res = inference_engine.run(
            profile=profile,
            crisp_risk_score=fuzzy_res.crisp_risk_score,
            risk_category=fuzzy_res.risk_category,
        )

        # 3. Assertions & Invariant Checks
        alloc = expert_res.asset_allocation
        total_alloc = alloc["total_percentage"]
        eq = alloc["equity_percentage"]
        dt = alloc["debt_percentage"]
        gd = alloc["gold_percentage"]
        cs = alloc["cash_percentage"]
        dti = expert_res.debt_analysis["dti_ratio"]

        # Check Invariants:
        assert total_alloc == 100.0, f"Portfolio must sum to 100%, got {total_alloc}"
        assert eq >= 0 and dt >= 0 and gd >= 0 and cs >= 0, "No negative allocations allowed"
        assert 0.0 <= fuzzy_res.crisp_risk_score <= 100.0, f"Risk score out of bounds: {fuzzy_res.crisp_risk_score}"
        assert fuzzy_res.risk_category in ["Conservative", "Moderate", "Aggressive"]
        assert expert_res.emergency_fund["target_fund"] == profile.monthly_expenses * 6.0
        assert expert_res.budget_breakdown["investable_surplus"] >= 0.0

        # Specific Persona Checks
        if profile.user_id == "USR_03_HOME_LOAN_FAMILY":
            assert dti > 40.0, "DTI must be > 40%"
            assert any(t.rule_id == "RULE_DTI_01" for t in expert_res.rule_execution_trace if t.status == RuleStatus.TRIGGERED)
        
        if profile.user_id == "USR_07_PENSIONER":
            assert fuzzy_res.risk_category == "Conservative"
            assert dt + cs >= 60.0, "Pensioner must have >= 60% fixed income + cash"

        passed_count += 1
        status_str = "[PASS]"
        print(f"{profile.user_id:<24} | {profile.age:<3} | {profile.monthly_income:<12,.0f} | {fuzzy_res.risk_category:<12} | {fuzzy_res.crisp_risk_score:<10.1f} | {dti:<6.1f}% | {eq:<7.1f} | {dt:<6.1f} | {gd:<5.1f} | {cs:<5.1f} | {status_str}")

    print("-" * 110)
    print(f"Summary: {passed_count}/{total_profiles} profiles validated with 100% mathematical integrity!")
    print("=" * 110 + "\n")


def print_detailed_profile_report(profile_id: str):
    """Generates an in-depth breakdown for an individual profile."""
    profile = next((p for p in DATASET if p.user_id == profile_id), None)
    if not profile:
        return

    fuzzy_evaluator = FuzzyRiskEvaluator()
    inference_engine = FinancialInferenceEngine()

    fuzzy_res = fuzzy_evaluator.evaluate(
        age=profile.age,
        income_stability=profile.income_stability_score,
        loss_tolerance=profile.loss_tolerance_score,
        investment_horizon_years=profile.investment_horizon_years,
    )
    expert_res = inference_engine.run(
        profile=profile,
        crisp_risk_score=fuzzy_res.crisp_risk_score,
        risk_category=fuzzy_res.risk_category,
    )

    print(f"\n==================== DETAILED DRILLDOWN: {profile.user_id} ====================")
    print(f"1. Profile Demographics: Age {profile.age}, Monthly Income: INR {profile.monthly_income:,.0f}, EMI: INR {profile.monthly_emi:,.0f}")
    print(f"2. Goal: {profile.financial_goal} (Target: INR {profile.goal_target_amount:,.0f} in {profile.investment_horizon_years} years)")
    print(f"3. Fuzzy Risk Category:  {fuzzy_res.risk_category} (Score: {fuzzy_res.crisp_risk_score:.2f}/100)")
    print(f"   Membership Degrees:   {fuzzy_res.membership_breakdown}")
    print(f"4. DTI Analysis:          {expert_res.debt_analysis['dti_ratio']}% -> {expert_res.debt_analysis['dti_status']}")
    print(f"5. Emergency Reserve:     Current: INR {expert_res.emergency_fund['current_fund']:,.0f} / Target: INR {expert_res.emergency_fund['target_fund']:,.0f} (Shortfall: INR {expert_res.emergency_fund['shortfall']:,.0f})")
    print(f"6. 50/30/20 Budget:       Needs limit: INR {expert_res.budget_breakdown['needs_allocation']:,.0f}, Investable Surplus: INR {expert_res.budget_breakdown['investable_surplus']:,.0f}/mo")
    print(f"7. Asset Allocation:      Equity: {expert_res.asset_allocation['equity_percentage']}% | Debt: {expert_res.asset_allocation['debt_percentage']}% | Gold: {expert_res.asset_allocation['gold_percentage']}% | Cash: {expert_res.asset_allocation['cash_percentage']}%")
    print(f"8. SIP Requirement:       INR {expert_res.sip_calculation['monthly_sip_required']:,.0f}/month at 12% CAGR")
    print(f"9. Tax Advisory:          {expert_res.tax_optimization['advice']}")
    print("10. Triggered Rules:")
    for t in expert_res.rule_execution_trace:
        if t.status == RuleStatus.TRIGGERED:
            print(f"    - [{t.rule_id}] {t.rule_name} (Priority {t.priority}): {t.explanation}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_dataset_validation()
    print_detailed_profile_report("USR_03_HOME_LOAN_FAMILY")
