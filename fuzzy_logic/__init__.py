"""
Fuzzy Logic Module for FinWise AI.
Provides Mamdani Fuzzy Risk Evaluator and Membership Function Primitives.
"""

from fuzzy_logic.membership import (
    LinguisticVariables,
    fuzzify_age,
    fuzzify_horizon,
    fuzzify_income_stability,
    fuzzify_loss_tolerance,
    trapmf,
    trimf,
)
from fuzzy_logic.risk_evaluator import FuzzyRiskEvaluator, FuzzyRiskResult
from fuzzy_logic.rules import FuzzyRule, RULE_BASE, evaluate_rule_base

__all__ = [
    "trimf",
    "trapmf",
    "LinguisticVariables",
    "fuzzify_age",
    "fuzzify_income_stability",
    "fuzzify_loss_tolerance",
    "fuzzify_horizon",
    "FuzzyRule",
    "RULE_BASE",
    "evaluate_rule_base",
    "FuzzyRiskEvaluator",
    "FuzzyRiskResult",
]
