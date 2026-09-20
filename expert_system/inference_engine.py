"""
Forward Chaining Inference Engine for FinWise AI Expert System.
Manages Working Memory, pattern matching, priority-based conflict resolution,
and rule execution audit trail.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from expert_system.knowledge_base import (
    build_default_rules,
    calculate_50_30_20_budget,
    calculate_asset_allocation,
    calculate_dti,
    calculate_emergency_fund,
    calculate_goal_sip,
    evaluate_tax_strategy,
)
from expert_system.rules_catalog import ProductionRule, RuleStatus, RuleTrace, UserFinancialProfile


@dataclass
class ExpertSystemOutput:
    """Consolidated deterministic output from the Expert System & Knowledge Base."""
    debt_analysis: Dict[str, Any]
    emergency_fund: Dict[str, Any]
    budget_breakdown: Dict[str, Any]
    asset_allocation: Dict[str, float]
    tax_optimization: Dict[str, Any]
    sip_calculation: Dict[str, Any]
    rule_execution_trace: List[RuleTrace]
    summary_verdict: str

    def to_dict(self) -> Dict[str, Any]:
        """Converts output to JSON-serializable dictionary matching API Contracts."""
        return {
            "debt_analysis": self.debt_analysis,
            "emergency_fund": self.emergency_fund,
            "budget_breakdown": self.budget_breakdown,
            "asset_allocation": self.asset_allocation,
            "tax_optimization": self.tax_optimization,
            "sip_calculation": self.sip_calculation,
            "rule_execution_trace": [t.to_dict() for t in self.rule_execution_trace],
            "summary_verdict": self.summary_verdict,
        }


class FinancialInferenceEngine:
    """
    Forward Chaining Production System Inference Engine.
    """

    def __init__(self, rules: Optional[List[ProductionRule]] = None):
        self.rules: List[ProductionRule] = rules if rules is not None else build_default_rules()
        # Sort rules by priority (conflict resolution: lower number = higher precedence)
        self.rules.sort(key=lambda r: r.priority)

    def run(
        self,
        profile: UserFinancialProfile,
        crisp_risk_score: float,
        risk_category: str,
    ) -> ExpertSystemOutput:
        """
        Executes the Forward Chaining cycle:
        1. Initialize Working Memory with base facts and derived calculations.
        2. Match antecedent conditions of production rules against working memory.
        3. Fire activated rules in priority order and record execution traces.
        4. Synthesize deterministic verdict.
        """
        # Step 1: Base Calculations & Fact Base Population
        dti_info = calculate_dti(profile.monthly_emi, profile.monthly_income)
        ef_info = calculate_emergency_fund(profile.monthly_expenses, profile.current_liquid_savings)
        budget_info = calculate_50_30_20_budget(
            profile.monthly_income, profile.monthly_expenses, profile.monthly_emi
        )
        asset_alloc = calculate_asset_allocation(
            crisp_risk_score=crisp_risk_score,
            risk_category=risk_category,
            investment_horizon_years=profile.investment_horizon_years,
            age=profile.age,
        )
        tax_info = evaluate_tax_strategy(profile.tax_regime, profile.monthly_income)
        sip_info = calculate_goal_sip(
            target_amount=profile.goal_target_amount,
            horizon_years=profile.investment_horizon_years,
        )

        # Populate Working Memory
        working_memory: Dict[str, Any] = {
            "profile": profile,
            "crisp_risk_score": crisp_risk_score,
            "risk_category": risk_category,
            "dti_analysis": dti_info,
            "emergency_fund": ef_info,
            "budget_breakdown": budget_info,
            "asset_allocation": asset_alloc,
            "tax_optimization": tax_info,
            "sip_calculation": sip_info,
        }

        # Step 2: Forward Chaining Rule Evaluation Loop
        traces: List[RuleTrace] = []

        for rule in self.rules:
            try:
                condition_met = rule.condition(working_memory)
                if condition_met:
                    rule.action(working_memory, traces)
                else:
                    traces.append(
                        RuleTrace(
                            rule_id=rule.rule_id,
                            rule_name=rule.name,
                            status=RuleStatus.SKIPPED,
                            condition=rule.condition_description,
                            priority=rule.priority,
                            explanation="Condition not satisfied by current Working Memory facts.",
                        )
                    )
            except Exception as e:
                traces.append(
                    RuleTrace(
                        rule_id=rule.rule_id,
                        rule_name=rule.name,
                        status=RuleStatus.SKIPPED,
                        condition=rule.condition_description,
                        priority=rule.priority,
                        explanation=f"Error evaluating rule: {str(e)}",
                    )
                )

        # Step 3: Synthesis of final deterministic advisory verdict
        verdict = self._synthesize_verdict(working_memory, traces)

        return ExpertSystemOutput(
            debt_analysis=dti_info,
            emergency_fund=ef_info,
            budget_breakdown=budget_info,
            asset_allocation=asset_alloc,
            tax_optimization=tax_info,
            sip_calculation=sip_info,
            rule_execution_trace=traces,
            summary_verdict=verdict,
        )

    def _synthesize_verdict(self, wm: Dict[str, Any], traces: List[RuleTrace]) -> str:
        triggered_rules = [t for t in traces if t.status == RuleStatus.TRIGGERED]
        profile: UserFinancialProfile = wm["profile"]
        alloc = wm["asset_allocation"]

        verdict_parts = [
            f"Evaluated financial profile for user '{profile.user_id}' (Age: {profile.age}).",
            f"Risk Category: {wm['risk_category']} (Score: {wm['crisp_risk_score']:.1f}/100).",
            f"Recommended Portfolio: {alloc['equity_percentage']}% Equity, {alloc['debt_percentage']}% Debt, {alloc['gold_percentage']}% Gold, {alloc['cash_percentage']}% Cash.",
            f"Rules Triggered ({len(triggered_rules)}): {', '.join([t.rule_name for t in triggered_rules]) if triggered_rules else 'Standard balanced allocation'}.",
        ]
        return " | ".join(verdict_parts)
