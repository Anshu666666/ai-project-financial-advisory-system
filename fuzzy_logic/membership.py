"""
Fuzzy Logic Membership Functions & Linguistic Variable Definitions.
Pure Python implementation of Triangular and Trapezoidal membership functions.
Designed for deterministic evaluation and transparent explainability in the viva.
"""

from typing import Dict, Tuple


def trimf(x: float, params: Tuple[float, float, float]) -> float:
    """
    Triangular Membership Function:
    params = (a, b, c) where a <= b <= c
    """
    a, b, c = params
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a) if b != a else 1.0
    elif b < x < c:
        return (c - x) / (c - b) if c != b else 1.0
    return 0.0


def trapmf(x: float, params: Tuple[float, float, float, float]) -> float:
    """
    Trapezoidal Membership Function:
    params = (a, b, c, d) where a <= b <= c <= d
    Correctly handles left shoulder (a == b) and right shoulder (c == d).
    """
    a, b, c, d = params
    if a == b and x <= b:
        return 1.0
    if c == d and x >= c:
        return 1.0
    if x <= a or x >= d:
        return 0.0
    elif a < x < b:
        return (x - a) / (b - a) if b != a else 1.0
    elif b <= x <= c:
        return 1.0
    elif c < x < d:
        return (d - x) / (d - c) if d != c else 1.0
    return 0.0


class LinguisticVariables:
    """
    Linguistic variables and universe parameters for the Financial Risk Evaluator.
    """

    # 1. Age (Universe: 18 - 80+ years)
    AGE_YOUNG = (18.0, 18.0, 26.0, 36.0)     # Left shoulder trapezoid
    AGE_MIDDLE = (28.0, 42.0, 56.0)          # Triangular
    AGE_SENIOR = (48.0, 60.0, 80.0, 80.0)    # Right shoulder trapezoid

    # 2. Income Stability (Universe: 0 - 100 score)
    INCOME_UNSTABLE = (0.0, 0.0, 25.0, 45.0)  # Left shoulder
    INCOME_MODERATE = (35.0, 55.0, 75.0)      # Triangular
    INCOME_STABLE = (65.0, 85.0, 100.0, 100.0)# Right shoulder

    # 3. Loss Tolerance (Universe: 0 - 100 score)
    LOSS_LOW = (0.0, 0.0, 20.0, 40.0)         # Left shoulder
    LOSS_MEDIUM = (30.0, 50.0, 70.0)          # Triangular
    LOSS_HIGH = (60.0, 80.0, 100.0, 100.0)    # Right shoulder

    # 4. Investment Horizon (Universe: 0 - 30+ years)
    HORIZON_SHORT = (0.0, 0.0, 2.0, 4.0)      # Left shoulder
    HORIZON_MEDIUM = (3.0, 7.0, 12.0)         # Triangular
    HORIZON_LONG = (8.0, 15.0, 30.0, 30.0)    # Right shoulder

    # Output: Risk Score Universe (0 - 100)
    RISK_CONSERVATIVE = (0.0, 0.0, 25.0, 40.0) # Left shoulder
    RISK_MODERATE = (30.0, 50.0, 70.0)          # Triangular
    RISK_AGGRESSIVE = (60.0, 75.0, 100.0, 100.0)# Right shoulder


def fuzzify_age(age: float) -> Dict[str, float]:
    """Calculate fuzzy membership degrees for Age."""
    return {
        "young": trapmf(age, LinguisticVariables.AGE_YOUNG),
        "middle": trimf(age, LinguisticVariables.AGE_MIDDLE),
        "senior": trapmf(age, LinguisticVariables.AGE_SENIOR),
    }


def fuzzify_income_stability(stability: float) -> Dict[str, float]:
    """Calculate fuzzy membership degrees for Income Stability."""
    return {
        "unstable": trapmf(stability, LinguisticVariables.INCOME_UNSTABLE),
        "moderate": trimf(stability, LinguisticVariables.INCOME_MODERATE),
        "stable": trapmf(stability, LinguisticVariables.INCOME_STABLE),
    }


def fuzzify_loss_tolerance(tolerance: float) -> Dict[str, float]:
    """Calculate fuzzy membership degrees for Loss Tolerance."""
    return {
        "low": trapmf(tolerance, LinguisticVariables.LOSS_LOW),
        "medium": trimf(tolerance, LinguisticVariables.LOSS_MEDIUM),
        "high": trapmf(tolerance, LinguisticVariables.LOSS_HIGH),
    }


def fuzzify_horizon(years: float) -> Dict[str, float]:
    """Calculate fuzzy membership degrees for Investment Horizon."""
    return {
        "short": trapmf(years, LinguisticVariables.HORIZON_SHORT),
        "medium": trimf(years, LinguisticVariables.HORIZON_MEDIUM),
        "long": trapmf(years, LinguisticVariables.HORIZON_LONG),
    }
