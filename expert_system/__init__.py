"""
Rule-Based Expert System Module for FinWise AI.
Provides Forward Chaining Inference Engine, Production Rules, and Financial Knowledge Base.
"""

from expert_system.inference_engine import ExpertSystemOutput, FinancialInferenceEngine
from expert_system.knowledge_base import (
    build_default_rules,
    calculate_50_30_20_budget,
    calculate_asset_allocation,
    calculate_dti,
    calculate_emergency_fund,
    calculate_goal_sip,
    evaluate_tax_strategy,
)
from expert_system.rules_catalog import (
    ProductionRule,
    RuleStatus,
    RuleTrace,
    UserFinancialProfile,
)

__all__ = [
    "UserFinancialProfile",
    "RuleTrace",
    "RuleStatus",
    "ProductionRule",
    "FinancialInferenceEngine",
    "ExpertSystemOutput",
    "calculate_dti",
    "calculate_emergency_fund",
    "calculate_50_30_20_budget",
    "calculate_asset_allocation",
    "calculate_goal_sip",
    "evaluate_tax_strategy",
    "build_default_rules",
]
