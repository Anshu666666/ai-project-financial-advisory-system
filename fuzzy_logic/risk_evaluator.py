"""
Fuzzy Logic Risk Evaluator using Mamdani Inference and Centroid Defuzzification.
Pure Python implementation designed for deterministic risk scoring and full explainability.
"""

from dataclasses import dataclass
from typing import Any, Dict
from fuzzy_logic.membership import (
    LinguisticVariables,
    fuzzify_age,
    fuzzify_horizon,
    fuzzify_income_stability,
    fuzzify_loss_tolerance,
    trapmf,
    trimf,
)
from fuzzy_logic.rules import evaluate_rule_base


@dataclass
class FuzzyRiskResult:
    """Represents the complete result of a Fuzzy Risk Evaluation."""
    crisp_risk_score: float
    risk_category: str
    membership_breakdown: Dict[str, Dict[str, float]]
    rule_firing_strengths: Dict[str, float]
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary conforming to API contracts."""
        return {
            "crisp_risk_score": round(self.crisp_risk_score, 2),
            "risk_category": self.risk_category,
            "membership_breakdown": self.membership_breakdown,
            "rule_firing_strengths": {
                k: round(v, 3) for k, v in self.rule_firing_strengths.items()
            },
            "rationale": self.rationale,
        }


class FuzzyRiskEvaluator:
    """
    Evaluates investor risk appetite using Mamdani Fuzzy Inference System (FIS).
    """

    def __init__(self, discretization_steps: int = 100):
        self.steps = discretization_steps

    def evaluate(
        self,
        age: float,
        income_stability: float,
        loss_tolerance: float,
        investment_horizon_years: float,
    ) -> FuzzyRiskResult:
        """
        Executes end-to-end Mamdani FIS:
        1. Fuzzification of numerical inputs into linguistic membership degrees.
        2. Fuzzy Rule Inference to obtain consequent firing strengths (alphas).
        3. Aggregation of fuzzy consequents.
        4. Centroid (Center of Gravity) Defuzzification to generate crisp risk score [0 - 100].
        """
        # Step 1: Fuzzification
        age_mems = fuzzify_age(age)
        inc_mems = fuzzify_income_stability(income_stability)
        loss_mems = fuzzify_loss_tolerance(loss_tolerance)
        horiz_mems = fuzzify_horizon(investment_horizon_years)

        # Step 2: Rule Base Evaluation (T-norm Min & S-norm Max)
        alphas = evaluate_rule_base(age_mems, inc_mems, loss_mems, horiz_mems)

        # Step 3 & 4: Centroid Defuzzification across y in [0, 100]
        numerator = 0.0
        denominator = 0.0

        for i in range(self.steps + 1):
            y = (100.0 / self.steps) * i

            # Membership of y in each risk output set
            mu_cons = trapmf(y, LinguisticVariables.RISK_CONSERVATIVE)
            mu_mod = trimf(y, LinguisticVariables.RISK_MODERATE)
            mu_agg = trapmf(y, LinguisticVariables.RISK_AGGRESSIVE)

            # Mamdani implication (Min clipping)
            clip_cons = min(alphas["conservative"], mu_cons)
            clip_mod = min(alphas["moderate"], mu_mod)
            clip_agg = min(alphas["aggressive"], mu_agg)

            # Fuzzy Aggregation (Max operator)
            mu_agg_y = max(clip_cons, clip_mod, clip_agg)

            numerator += y * mu_agg_y
            denominator += mu_agg_y

        # Compute Crisp Risk Score
        if denominator > 0.0001:
            crisp_score = numerator / denominator
        else:
            crisp_score = 50.0

        # Categorize
        if crisp_score < 35.0:
            category = "Conservative"
        elif crisp_score <= 70.0:
            category = "Moderate"
        else:
            category = "Aggressive"

        # Generate Human-Readable Rationale
        rationale = self._generate_rationale(
            age=age,
            category=category,
            alphas=alphas,
            horizon=investment_horizon_years,
        )

        return FuzzyRiskResult(
            crisp_risk_score=crisp_score,
            risk_category=category,
            membership_breakdown={
                "age_memberships": {k: round(v, 3) for k, v in age_mems.items()},
                "income_stability_memberships": {k: round(v, 3) for k, v in inc_mems.items()},
                "loss_tolerance_memberships": {k: round(v, 3) for k, v in loss_mems.items()},
                "horizon_memberships": {k: round(v, 3) for k, v in horiz_mems.items()},
            },
            rule_firing_strengths=alphas,
            rationale=rationale,
        )

    def _generate_rationale(
        self,
        age: float,
        category: str,
        alphas: Dict[str, float],
        horizon: float,
    ) -> str:
        """Constructs transparent audit rationale for viva evaluation."""
        primary_consequent = max(alphas, key=alphas.get)
        strength = alphas[primary_consequent]

        return (
            f"Fuzzy Mamdani Inference evaluated profile for Age {int(age)} with a {horizon}-year horizon. "
            f"Primary fuzzy set '{primary_consequent}' fired with strength {strength:.2f}, "
            f"yielding a Centroid defuzzified risk score classified as '{category}'."
        )
