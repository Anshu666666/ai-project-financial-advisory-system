"""
Mamdani Fuzzy Rule Base for Financial Risk Appetite Evaluation.
Combines linguistic antecedents using T-norm (Min) operator to evaluate firing strengths.
"""

from typing import Dict, List


class FuzzyRule:
    """Represents a single Mamdani Fuzzy Production Rule."""

    def __init__(
        self,
        rule_id: str,
        age: str,
        income_stability: str,
        loss_tolerance: str,
        horizon: str,
        consequent: str,
        weight: float = 1.0,
    ):
        self.rule_id = rule_id
        self.age = age
        self.income_stability = income_stability
        self.loss_tolerance = loss_tolerance
        self.horizon = horizon
        self.consequent = consequent  # "conservative", "moderate", "aggressive"
        self.weight = weight

    def evaluate(
        self,
        age_mems: Dict[str, float],
        inc_mems: Dict[str, float],
        loss_mems: Dict[str, float],
        horiz_mems: Dict[str, float],
    ) -> float:
        """
        Evaluate firing strength (alpha) using Mamdani T-Norm (Min operator).
        """
        mu_age = age_mems.get(self.age, 0.0) if self.age != "any" else 1.0
        mu_inc = inc_mems.get(self.income_stability, 0.0) if self.income_stability != "any" else 1.0
        mu_loss = loss_mems.get(self.loss_tolerance, 0.0) if self.loss_tolerance != "any" else 1.0
        mu_horiz = horiz_mems.get(self.horizon, 0.0) if self.horizon != "any" else 1.0

        # T-Norm Min composition
        alpha = min(mu_age, mu_inc, mu_loss, mu_horiz) * self.weight
        return alpha


# Comprehensive Rule Base for Financial Risk Inference
RULE_BASE: List[FuzzyRule] = [
    # 1. Aggressive Risk Profiles (High loss tolerance + Long horizon + Young/Middle)
    FuzzyRule("FR01", age="young", income_stability="stable", loss_tolerance="high", horizon="long", consequent="aggressive"),
    FuzzyRule("FR02", age="young", income_stability="moderate", loss_tolerance="high", horizon="long", consequent="aggressive"),
    FuzzyRule("FR03", age="young", income_stability="stable", loss_tolerance="medium", horizon="long", consequent="aggressive"),
    FuzzyRule("FR04", age="middle", income_stability="stable", loss_tolerance="high", horizon="long", consequent="aggressive"),
    FuzzyRule("FR05", age="young", income_stability="stable", loss_tolerance="high", horizon="medium", consequent="aggressive"),
    FuzzyRule("FR06", age="middle", income_stability="moderate", loss_tolerance="high", horizon="long", consequent="aggressive"),

    # 2. Moderate Risk Profiles (Balanced characteristics)
    FuzzyRule("FR07", age="young", income_stability="moderate", loss_tolerance="medium", horizon="medium", consequent="moderate"),
    FuzzyRule("FR08", age="middle", income_stability="stable", loss_tolerance="medium", horizon="medium", consequent="moderate"),
    FuzzyRule("FR09", age="middle", income_stability="moderate", loss_tolerance="medium", horizon="medium", consequent="moderate"),
    FuzzyRule("FR10", age="young", income_stability="unstable", loss_tolerance="high", horizon="medium", consequent="moderate"),
    FuzzyRule("FR11", age="senior", income_stability="stable", loss_tolerance="medium", horizon="medium", consequent="moderate"),
    FuzzyRule("FR12", age="middle", income_stability="stable", loss_tolerance="low", horizon="long", consequent="moderate"),
    FuzzyRule("FR13", age="young", income_stability="stable", loss_tolerance="low", horizon="long", consequent="moderate"),
    FuzzyRule("FR14", age="any", income_stability="moderate", loss_tolerance="medium", horizon="long", consequent="moderate"),
    FuzzyRule("FR15", age="middle", income_stability="stable", loss_tolerance="high", horizon="short", consequent="moderate"),

    # 3. Conservative Risk Profiles (Low loss tolerance / Short horizon / Unstable income / Senior)
    FuzzyRule("FR16", age="senior", income_stability="any", loss_tolerance="low", horizon="any", consequent="conservative"),
    FuzzyRule("FR17", age="any", income_stability="unstable", loss_tolerance="low", horizon="any", consequent="conservative"),
    FuzzyRule("FR18", age="any", income_stability="any", loss_tolerance="low", horizon="short", consequent="conservative"),
    FuzzyRule("FR19", age="senior", income_stability="unstable", loss_tolerance="any", horizon="short", consequent="conservative"),
    FuzzyRule("FR20", age="young", income_stability="unstable", loss_tolerance="low", horizon="short", consequent="conservative"),
    FuzzyRule("FR21", age="any", income_stability="any", loss_tolerance="any", horizon="short", consequent="conservative", weight=0.8),
    FuzzyRule("FR22", age="senior", income_stability="moderate", loss_tolerance="low", horizon="medium", consequent="conservative"),
]


def evaluate_rule_base(
    age_mems: Dict[str, float],
    inc_mems: Dict[str, float],
    loss_mems: Dict[str, float],
    horiz_mems: Dict[str, float],
) -> Dict[str, float]:
    """
    Evaluates all fuzzy rules and aggregates firing strengths for each consequent
    using S-Norm (Max operator).
    Returns max alpha for 'conservative', 'moderate', 'aggressive'.
    """
    consequent_alphas: Dict[str, float] = {
        "conservative": 0.0,
        "moderate": 0.0,
        "aggressive": 0.0,
    }

    for rule in RULE_BASE:
        alpha = rule.evaluate(age_mems, inc_mems, loss_mems, horiz_mems)
        if alpha > 0.0:
            consequent_alphas[rule.consequent] = max(consequent_alphas[rule.consequent], alpha)

    return consequent_alphas
