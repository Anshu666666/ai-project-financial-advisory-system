"""
Declarative Rules Catalog & Fact Schemas for Financial Expert System.
Defines facts, working memory representations, production rules, and trace objects.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class RuleStatus(str, Enum):
    TRIGGERED = "TRIGGERED"
    SKIPPED = "SKIPPED"


@dataclass
class UserFinancialProfile:
    """User input profile facts fed into Working Memory."""
    user_id: str
    age: int
    monthly_income: float
    monthly_expenses: float
    monthly_emi: float
    current_liquid_savings: float
    income_stability_score: float
    loss_tolerance_score: float
    investment_horizon_years: int
    financial_goal: str = "Wealth Accumulation"
    goal_target_amount: float = 10000000.0
    tax_regime: str = "new"  # 'old' or 'new'


@dataclass
class RuleTrace:
    """Audit trace item recorded when a production rule is evaluated."""
    rule_id: str
    rule_name: str
    status: RuleStatus
    condition: str
    priority: int
    explanation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "status": self.status.value,
            "condition": self.condition,
            "priority": self.priority,
            "explanation": self.explanation,
        }


@dataclass
class ProductionRule:
    """
    IF-THEN Production Rule with condition predicate, action execution, and priority.
    """
    rule_id: str
    name: str
    condition_description: str
    priority: int  # Lower number = higher priority
    condition: Callable[[Dict[str, Any]], bool]
    action: Callable[[Dict[str, Any], List[RuleTrace]], None]
