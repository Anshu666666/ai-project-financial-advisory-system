"""
================================================================================
FINWISE AI – INTELLIGENT AGENT FORMALIZATION (PEAS MODEL)
Author: Zaid (Intelligent Agent & Web Search Lead)
================================================================================
Academic formalization of FinWise AI as a Utility-Based Intelligent Agent,
strictly aligned with University AI Course Syllabus Unit 1 (Intelligent Agents).
================================================================================
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class PEASSpecification:
    """
    Formal PEAS Description of FinWise AI Utility-Based Intelligent Agent.
    """

    agent_type: str = "Utility-Based Intelligent Agent"
    
    # Performance Measure (P)
    performance_measure: List[str] = field(default_factory=lambda: [
        "Financial goal attainment probability within user time horizon",
        "Deterministic portfolio risk-adjusted return (Sharpe heuristic)",
        "Minimization of high-interest debt exposure (DTI < 40%)",
        "Adequacy of emergency cash buffer (>= 6 months)",
        "Strict adherence to budget boundary constraints (50/30/20 rule)",
        "Zero mathematical hallucination rate via Expert System grounding",
    ])

    # Environment (E)
    environment: List[str] = field(default_factory=lambda: [
        "User financial telemetry (income, obligations, assets, goals)",
        "Macroeconomic benchmarks (central bank repo rates, CPI inflation)",
        "Financial market index trends and valuation benchmarks (PE ratio)",
        "Tax policies and regulatory compliance guardrails",
    ])

    # Actuators (A)
    actuators: List[str] = field(default_factory=lambda: [
        "Comprehensive Markdown Advisory Report generator",
        "Deterministic 100% Asset Allocation vector (Equity, Debt, Gold, Cash)",
        "Rule violation warnings and severity alerts",
        "Conversational follow-up Q&A handler with web citations",
        "Structured JSON payloads for client UI rendering",
    ])

    # Sensors (S)
    sensors: List[str] = field(default_factory=lambda: [
        "Client questionnaire / onboarding form payload sensor",
        "DuckDuckGo Real-Time Financial Web Search sensor",
        "Fuzzy Logic Membership perception engine",
        "Working Memory Fact extractor",
    ])

    # Agent Architecture Properties
    properties: Dict[str, str] = field(default_factory=lambda: {
        "Accessibility": "Partially Observable (User preferences & market volatility)",
        "Determinism": "Stochastic Environment / Deterministic Reasoning Core",
        "Episodic vs. Sequential": "Sequential (Decisions in Month 1 impact Year 5)",
        "Static vs. Dynamic": "Dynamic (Market conditions and benchmark rates change)",
        "Discrete vs. Continuous": "Hybrid (Discrete rule firings + Continuous monetary variables)",
        "Single vs. Multi-Agent": "Multi-Agent / Hybrid Architecture (Fuzzy Engine + Expert System + LLM Agent)",
    })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_type": self.agent_type,
            "performance_measure": self.performance_measure,
            "environment": self.environment,
            "actuators": self.actuators,
            "sensors": self.sensors,
            "properties": self.properties,
        }


def get_peas_model() -> PEASSpecification:
    """Returns the formal PEAS model instance."""
    return PEASSpecification()
