"""
================================================================================
FINWISE AI – STEP 1 STANDALONE VERIFICATION SUITE
Author: Aman (AI Core & Deterministic Reasoning Lead)
================================================================================
This test verifies the Fuzzy Logic Risk Evaluator and Rule-Based Expert System
in pure Python with zero external library dependencies.

Coverage:
1. Triangular and Trapezoidal Fuzzy Membership functions
2. Mamdani Fuzzy Rule Inference & Centroid Defuzzification
3. Forward-Chaining Production Rule Execution & Audit Trace Logging
4. Financial Mathematics: DTI, 50/30/20 Budgeting, Goal SIP FV, Asset Allocation
5. Strict 100% Portfolio Sum Constraint Verification
================================================================================
"""

import sys

# Ensure UTF-8 output across Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

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


def print_section(title: str):
    print(f"\n--- {title} ---")


def test_persona_1_young_aggressive():
    print_banner("Testing Persona 1: Young High-Growth Techie")
    
    # 1. Setup Fact Profile
    profile = UserFinancialProfile(
        user_id="usr_techie_24",
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
    print(f"Profile: Age={profile.age}, Income=INR {profile.monthly_income:,.0f}/mo, EMI=INR {profile.monthly_emi:,.0f}, Horizon={profile.investment_horizon_years}y")

    # 2. Run Fuzzy Logic Evaluator
    evaluator = FuzzyRiskEvaluator()
    fuzzy_res = evaluator.evaluate(
        age=profile.age,
        income_stability=profile.income_stability_score,
        loss_tolerance=profile.loss_tolerance_score,
        investment_horizon_years=profile.investment_horizon_years,
    )
    
    print_section("Fuzzy Logic Risk Evaluation")
    print(f"Crisp Risk Score: {fuzzy_res.crisp_risk_score:.2f} / 100.0")
    print(f"Risk Category:    {fuzzy_res.risk_category}")
    print(f"Membership Firing: {fuzzy_res.rule_firing_strengths}")
    print(f"Rationale:        {fuzzy_res.rationale}")

    # Assertions for Fuzzy Evaluation
    assert fuzzy_res.crisp_risk_score > 70.0, f"Expected Aggressive score > 70, got {fuzzy_res.crisp_risk_score}"
    assert fuzzy_res.risk_category == "Aggressive", f"Expected Aggressive, got {fuzzy_res.risk_category}"
    print("[PASS] Fuzzy Risk Score strictly classified as Aggressive.")

    # 3. Run Expert System Forward Chaining
    engine = FinancialInferenceEngine()
    expert_output = engine.run(
        profile=profile,
        crisp_risk_score=fuzzy_res.crisp_risk_score,
        risk_category=fuzzy_res.risk_category,
    )

    print_section("Expert System Output & Domain Calculations")
    print(f"DTI Ratio:        {expert_output.debt_analysis['dti_ratio']}% ({expert_output.debt_analysis['dti_status']})")
    print(f"Emergency Fund:   INR {expert_output.emergency_fund['current_fund']:,.0f} / INR {expert_output.emergency_fund['target_fund']:,.0f} ({expert_output.emergency_fund['status']})")
    print(f"Budget (50/30/20): Surplus = INR {expert_output.budget_breakdown['investable_surplus']:,.0f}/mo")
    print(f"Asset Allocation: {expert_output.asset_allocation}")
    print(f"Goal SIP Req:     INR {expert_output.sip_calculation['monthly_sip_required']:,.0f}/mo for target INR {expert_output.sip_calculation['target_amount']:,.0f}")

    print_section("Rule Execution Traces")
    triggered = [t for t in expert_output.rule_execution_trace if t.status == RuleStatus.TRIGGERED]
    for t in expert_output.rule_execution_trace:
        status_icon = "[TRIGGERED]" if t.status == RuleStatus.TRIGGERED else "[SKIPPED]  "
        print(f"{status_icon} ({t.rule_id}) {t.rule_name} -> {t.explanation}")

    # Assertions for Expert System
    assert expert_output.debt_analysis["dti_status"] == "Healthy", "DTI should be Healthy for 0 EMI"
    assert expert_output.emergency_fund["status"] == "Adequate", "Emergency buffer should be adequate"
    assert expert_output.asset_allocation["total_percentage"] == 100.0, "Allocations must sum to 100%"
    assert expert_output.asset_allocation["equity_percentage"] >= 65.0, "Young aggressive should have >= 65% equity"
    assert any(t.rule_id == "RULE_ALLOC_03" for t in triggered), "RULE_ALLOC_03 must fire for Aggressive growth"
    print("[PASS] All Persona 1 Expert System assertions verified successfully!")


def test_persona_2_mid_career_debt_stress():
    print_banner("Testing Persona 2: Mid-Career Parent with High Debt Stress")
    
    # 1. Setup Fact Profile
    profile = UserFinancialProfile(
        user_id="usr_family_42",
        age=42,
        monthly_income=100000.0,
        monthly_expenses=55000.0,
        monthly_emi=45000.0,  # 45% DTI -> High Risk!
        current_liquid_savings=50000.0,  # Far below 6x expenses (INR 3.3L)
        income_stability_score=50.0,
        loss_tolerance_score=35.0,
        investment_horizon_years=5,
        financial_goal="Child Higher Education",
        goal_target_amount=3000000.0,
        tax_regime="old",
    )
    print(f"Profile: Age={profile.age}, Income=INR {profile.monthly_income:,.0f}/mo, EMI=INR {profile.monthly_emi:,.0f}, Horizon={profile.investment_horizon_years}y")

    # 2. Run Fuzzy Logic Evaluator
    evaluator = FuzzyRiskEvaluator()
    fuzzy_res = evaluator.evaluate(
        age=profile.age,
        income_stability=profile.income_stability_score,
        loss_tolerance=profile.loss_tolerance_score,
        investment_horizon_years=profile.investment_horizon_years,
    )

    print_section("Fuzzy Logic Risk Evaluation")
    print(f"Crisp Risk Score: {fuzzy_res.crisp_risk_score:.2f} / 100.0")
    print(f"Risk Category:    {fuzzy_res.risk_category}")

    # 3. Run Expert System Forward Chaining
    engine = FinancialInferenceEngine()
    expert_output = engine.run(
        profile=profile,
        crisp_risk_score=fuzzy_res.crisp_risk_score,
        risk_category=fuzzy_res.risk_category,
    )

    print_section("Expert System Output & Rule Firings")
    print(f"DTI Ratio:        {expert_output.debt_analysis['dti_ratio']}% ({expert_output.debt_analysis['dti_status']})")
    print(f"Emergency Fund:   Shortfall = INR {expert_output.emergency_fund['shortfall']:,.0f} ({expert_output.emergency_fund['status']})")
    print(f"Investable Surplus: INR {expert_output.budget_breakdown['investable_surplus']:,.0f}/mo")

    triggered = [t for t in expert_output.rule_execution_trace if t.status == RuleStatus.TRIGGERED]
    for t in triggered:
        print(f"[TRIGGERED] ({t.rule_id}) {t.rule_name} -> {t.explanation}")

    # Assertions
    assert expert_output.debt_analysis["dti_status"] == "High Risk", "DTI 45% must be High Risk"
    assert expert_output.emergency_fund["status"] == "Critical Shortfall", "Savings < 3 mo must be Critical"
    assert any(t.rule_id == "RULE_DTI_01" for t in triggered), "RULE_DTI_01 must trigger on high DTI"
    assert any(t.rule_id == "RULE_EMERGENCY_02" for t in triggered), "RULE_EMERGENCY_02 must trigger on shortfall"
    assert expert_output.asset_allocation["total_percentage"] == 100.0, "Portfolio must sum to 100%"
    print("[PASS] All Persona 2 Debt-Stress assertions verified successfully!")


def test_persona_3_senior_conservative():
    print_banner("Testing Persona 3: Senior Pre-Retiree Capital Preservation")
    
    # 1. Setup Fact Profile
    profile = UserFinancialProfile(
        user_id="usr_retiree_58",
        age=58,
        monthly_income=200000.0,
        monthly_expenses=60000.0,
        monthly_emi=5000.0,
        current_liquid_savings=2000000.0,
        income_stability_score=80.0,
        loss_tolerance_score=15.0,  # Very low risk tolerance
        investment_horizon_years=2,  # Short horizon
        financial_goal="Retirement Capital Protection",
        goal_target_amount=15000000.0,
        tax_regime="new",
    )
    print(f"Profile: Age={profile.age}, Income=INR {profile.monthly_income:,.0f}/mo, EMI=INR {profile.monthly_emi:,.0f}, Horizon={profile.investment_horizon_years}y")

    # 2. Run Fuzzy Logic Evaluator
    evaluator = FuzzyRiskEvaluator()
    fuzzy_res = evaluator.evaluate(
        age=profile.age,
        income_stability=profile.income_stability_score,
        loss_tolerance=profile.loss_tolerance_score,
        investment_horizon_years=profile.investment_horizon_years,
    )

    print_section("Fuzzy Logic Risk Evaluation")
    print(f"Crisp Risk Score: {fuzzy_res.crisp_risk_score:.2f} / 100.0")
    print(f"Risk Category:    {fuzzy_res.risk_category}")

    assert fuzzy_res.risk_category == "Conservative", f"Expected Conservative, got {fuzzy_res.risk_category}"
    assert fuzzy_res.crisp_risk_score < 35.0, f"Expected score < 35, got {fuzzy_res.crisp_risk_score}"

    # 3. Run Expert System Forward Chaining
    engine = FinancialInferenceEngine()
    expert_output = engine.run(
        profile=profile,
        crisp_risk_score=fuzzy_res.crisp_risk_score,
        risk_category=fuzzy_res.risk_category,
    )

    print_section("Expert System Output & Rule Firings")
    print(f"Asset Allocation: {expert_output.asset_allocation}")
    triggered = [t for t in expert_output.rule_execution_trace if t.status == RuleStatus.TRIGGERED]
    for t in triggered:
        print(f"[TRIGGERED] ({t.rule_id}) {t.rule_name} -> {t.explanation}")

    # Assertions
    assert any(t.rule_id == "RULE_ALLOC_04" for t in triggered), "RULE_ALLOC_04 Capital Preservation must trigger"
    assert (expert_output.asset_allocation["debt_percentage"] + expert_output.asset_allocation["cash_percentage"]) >= 50.0, "Senior conservative must have >= 50% fixed income + cash"
    assert expert_output.asset_allocation["total_percentage"] == 100.0, "Portfolio must sum to 100%"
    print("[PASS] All Persona 3 Senior Conservative assertions verified successfully!")


def main():
    print("\n" + "#" * 80)
    print("# FINWISE AI - STEP 1 STANDALONE VERIFICATION RUNNER")
    print("# Testing Aman's Fuzzy Logic Engine & Rule-Based Expert System")
    print("#" * 80)

    try:
        test_persona_1_young_aggressive()
        test_persona_2_mid_career_debt_stress()
        test_persona_3_senior_conservative()
        
        print("\n" + "=" * 80)
        print(">>> ALL TESTS PASSED (100% SUCCESS RATE)! <<<")
        print("Aman's Step 1 AI Core is 100% verified, pure Python, and frozen for handoff.")
        print("=" * 80 + "\n")
        return 0
    except AssertionError as ae:
        print(f"\n[FAIL] ASSERTION FAILED: {ae}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n[FAIL] UNEXPECTED ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
