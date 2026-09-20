"""
================================================================================
FINWISE AI – INTERACTIVE ADVISORY DEMO (STEP 1)
Author: Aman (AI Core Lead)
================================================================================
Run this script to test custom financial profiles or sample presets in real-time!
Usage:
    python demo_interactive.py
================================================================================
"""

import sys

# Windows UTF-8 console output
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


def print_banner():
    print("\n" + "=" * 80)
    print("       🚀 FINWISE AI – HYBRID INTELLIGENT FINANCIAL ADVISORY SYSTEM       ")
    print("                 AI Core: Fuzzy Logic + Expert System                     ")
    print("=" * 80)


def evaluate_and_display(profile: UserFinancialProfile):
    print("\n" + "=" * 80)
    print(f"📊 ADVISORY REPORT FOR: {profile.user_id.upper()}")
    print("=" * 80)
    
    print("\n[1] 📋 INPUT FINANCIAL PROFILE:")
    print(f"  • Age:                     {profile.age} years")
    print(f"  • Monthly Income:          INR {profile.monthly_income:,.2f}")
    print(f"  • Monthly Expenses:        INR {profile.monthly_expenses:,.2f}")
    print(f"  • Existing Monthly EMI:    INR {profile.monthly_emi:,.2f}")
    print(f"  • Current Liquid Savings:  INR {profile.current_liquid_savings:,.2f}")
    print(f"  • Income Stability Score:  {profile.income_stability_score:.0f} / 100")
    print(f"  • Loss Tolerance Score:    {profile.loss_tolerance_score:.0f} / 100")
    print(f"  • Investment Horizon:      {profile.investment_horizon_years} years")
    print(f"  • Target Financial Goal:   {profile.financial_goal} (INR {profile.goal_target_amount:,.2f})")
    print(f"  • Tax Regime:              {profile.tax_regime.upper()} Regime")

    # 1. Fuzzy Logic Evaluation
    evaluator = FuzzyRiskEvaluator()
    fuzzy_res = evaluator.evaluate(
        age=profile.age,
        income_stability=profile.income_stability_score,
        loss_tolerance=profile.loss_tolerance_score,
        investment_horizon_years=profile.investment_horizon_years,
    )

    print("\n[2] 🧠 FUZZY LOGIC RISK APPETITE (Mamdani Model & Centroid Defuzzification):")
    print(f"  • Crisp Risk Score:        {fuzzy_res.crisp_risk_score:.2f} / 100.0")
    print(f"  • Risk Appetite Category:  ✨ {fuzzy_res.risk_category.upper()} ✨")
    print(f"  • Fuzzy Firing Strengths:  {fuzzy_res.rule_firing_strengths}")
    print(f"  • AI Rationale:            {fuzzy_res.rationale}")

    # 2. Expert System Forward Chaining
    engine = FinancialInferenceEngine()
    expert_res = engine.run(
        profile=profile,
        crisp_risk_score=fuzzy_res.crisp_risk_score,
        risk_category=fuzzy_res.risk_category,
    )

    print("\n[3] 🏦 EXPERT SYSTEM FINANCIAL HEALTH CHECKS:")
    # DTI
    dti = expert_res.debt_analysis
    dti_icon = "🟢" if dti["dti_status"] == "Healthy" else ("🟡" if dti["dti_status"] == "Moderate" else "🔴")
    print(f"  • Debt-to-Income (DTI):    {dti_icon} {dti['dti_ratio']:.1f}% ({dti['dti_status']})")
    print(f"    ↳ {dti['recommendation']}")

    # Emergency Fund
    ef = expert_res.emergency_fund
    ef_icon = "🟢" if ef["status"] == "Adequate" else "🔴"
    print(f"  • Emergency Buffer:        {ef_icon} Current: INR {ef['current_fund']:,.0f} | Target (6 mo): INR {ef['target_fund']:,.0f}")
    print(f"    ↳ {ef['recommendation']}")

    # Budget
    b = expert_res.budget_breakdown
    print("\n[4] 💵 50/30/20 BUDGETING BREAKDOWN:")
    print(f"  • Needs Allocation (50% max):    INR {b['needs_allocation']:,.0f}")
    print(f"  • Wants Allocation (30% max):    INR {b['wants_allocation']:,.0f}")
    print(f"  • Savings Target   (20% min):    INR {b['savings_allocation']:,.0f}")
    print(f"  • Actual Net Investable Surplus: INR {b['investable_surplus']:,.0f} / month")

    # Asset Allocation
    alloc = expert_res.asset_allocation
    print("\n[5] 📈 RECOMMENDED ASSET ALLOCATION (Sums to 100%):")
    print(f"  ┌─────────────────────────┬────────────┐")
    print(f"  │ Asset Class             │ Allocation │")
    print(f"  ├─────────────────────────┼────────────┤")
    print(f"  │ Equity / Stocks         │ {alloc['equity_percentage']:>8.1f} % │")
    print(f"  │ Debt / Fixed Income     │ {alloc['debt_percentage']:>8.1f} % │")
    print(f"  │ Gold / Commodities      │ {alloc['gold_percentage']:>8.1f} % │")
    print(f"  │ Cash / Liquid Reserves  │ {alloc['cash_percentage']:>8.1f} % │")
    print(f"  ├─────────────────────────┼────────────┤")
    print(f"  │ TOTAL                   │ {alloc['total_percentage']:>8.1f} % │")
    print(f"  └─────────────────────────┴────────────┘")

    # Goal SIP
    sip = expert_res.sip_calculation
    print("\n[6] 🎯 GOAL-BASED SIP PLANNING:")
    print(f"  • Target Wealth:           INR {sip['target_amount']:,.0f} in {sip['horizon_years']} years")
    print(f"  • Required Monthly SIP:    INR {sip['monthly_sip_required']:,.0f} / month (at {sip['expected_cagr_percentage']}% CAGR)")
    print(f"  • Principal Investment:    INR {sip['total_principal_invested']:,.0f}")
    print(f"  • Projected Wealth Gain:   INR {sip['projected_wealth_gain']:,.0f}")

    # Tax Advisory
    print("\n[7] 📑 TAX STRATEGY OPTIMIZATION:")
    print(f"  • {expert_res.tax_optimization['advice']}")

    # Rule Execution Trace
    print("\n[8] 🔍 FORWARD-CHAINING RULE EXECUTION AUDIT TRAIL:")
    for t in expert_res.rule_execution_trace:
        status_tag = "🟢 TRIGGERED" if t.status == RuleStatus.TRIGGERED else "⚪ SKIPPED  "
        print(f"  [{status_tag}] ({t.rule_id}) {t.rule_name}")
        print(f"      Condition: {t.condition}")
        print(f"      Outcome:   {t.explanation}")

    print("\n" + "=" * 80 + "\n")


def run_custom_input():
    print("\n--- Enter Your Custom Financial Details ---")
    try:
        user_id = input("Enter your name / user ID [Aman]: ").strip() or "Aman"
        age = int(input("Enter your age (e.g. 23): ").strip() or "23")
        income = float(input("Enter gross monthly income in INR (e.g. 120000): ").strip() or "120000")
        expenses = float(input("Enter monthly living expenses in INR (e.g. 40000): ").strip() or "40000")
        emi = float(input("Enter total monthly EMI / debt in INR (e.g. 10000): ").strip() or "10000")
        savings = float(input("Enter current liquid savings in bank/FD in INR (e.g. 200000): ").strip() or "200000")
        stability = float(input("Income Stability score [0 - 100] (e.g. 85): ").strip() or "85")
        loss_tol = float(input("Risk / Loss Tolerance score [0 - 100] (e.g. 75): ").strip() or "75")
        horizon = int(input("Investment horizon in years (e.g. 10): ").strip() or "10")
        goal = input("Financial goal description [Wealth Growth]: ").strip() or "Wealth Growth"
        target_amt = float(input("Target goal amount in INR (e.g. 20000000): ").strip() or "20000000")
        regime = input("Tax Regime (new/old) [new]: ").strip().lower() or "new"

        profile = UserFinancialProfile(
            user_id=user_id,
            age=age,
            monthly_income=income,
            monthly_expenses=expenses,
            monthly_emi=emi,
            current_liquid_savings=savings,
            income_stability_score=stability,
            loss_tolerance_score=loss_tol,
            investment_horizon_years=horizon,
            financial_goal=goal,
            goal_target_amount=target_amt,
            tax_regime=regime,
        )
        evaluate_and_display(profile)
    except Exception as e:
        print(f"\n❌ Invalid input: {e}")


def main():
    print_banner()

    # Preset profiles
    presets = {
        "1": UserFinancialProfile(
            user_id="Aman_Aggressive_Saver",
            age=23,
            monthly_income=120000.0,
            monthly_expenses=35000.0,
            monthly_emi=0.0,
            current_liquid_savings=250000.0,
            income_stability_score=90.0,
            loss_tolerance_score=80.0,
            investment_horizon_years=12,
            financial_goal="Financial Freedom & Tech Fund",
            goal_target_amount=30000000.0,
            tax_regime="new",
        ),
        "2": UserFinancialProfile(
            user_id="Family_With_HomeLoan",
            age=38,
            monthly_income=200000.0,
            monthly_expenses=70000.0,
            monthly_emi=90000.0,  # 45% DTI
            current_liquid_savings=200000.0,  # Deficit
            income_stability_score=70.0,
            loss_tolerance_score=45.0,
            investment_horizon_years=7,
            financial_goal="Child Education & Home Loan Clearance",
            goal_target_amount=6000000.0,
            tax_regime="old",
        ),
        "3": UserFinancialProfile(
            user_id="PreRetiree_Conservative",
            age=57,
            monthly_income=250000.0,
            monthly_expenses=60000.0,
            monthly_emi=5000.0,
            current_liquid_savings=3000000.0,
            income_stability_score=85.0,
            loss_tolerance_score=15.0,
            investment_horizon_years=2,
            financial_goal="Retirement Capital Protection",
            goal_target_amount=20000000.0,
            tax_regime="new",
        ),
    }

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Run default demo directly
        evaluate_and_display(presets["1"])
        return 0

    print("Choose an option:")
    print("  [1] Run Preset 1: Young High-Growth Techie (Aggressive)")
    print("  [2] Run Preset 2: Family with Home Loan (High DTI & Emergency Deficit)")
    print("  [3] Run Preset 3: Pre-Retiree (Conservative Capital Preservation)")
    print("  [4] Enter Custom Financial Profile interactively")
    print("  [5] Run All Presets")
    print("  [0] Exit")

    choice = input("\nEnter choice (1-5, or press Enter for Preset 1): ").strip() or "1"

    if choice in presets:
        evaluate_and_display(presets[choice])
    elif choice == "4":
        run_custom_input()
    elif choice == "5":
        for p in presets.values():
            evaluate_and_display(p)
    elif choice == "0":
        print("Goodbye!")
    else:
        print("Invalid choice, running Preset 1 by default.")
        evaluate_and_display(presets["1"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
