# 🎓 Academic Syllabus Alignment & Viva Defense Guide

This document provides a **1-to-1 mapping** between the project components and your university **Artificial Intelligence course syllabus**. Use this directly in your project report, presentation slides, and during the final viva/evaluation.

---

## 📊 Syllabus Coverage Matrix

| Syllabus Topic | Concepts Covered | How It Is Implemented in FinWise AI | Key File / Component |
| :--- | :--- | :--- | :--- |
| **1. Intelligent Agents** | • Agent Structure<br>• PEAS Model<br>• Perception-Reasoning-Action Cycle<br>• Agent Classification (Utility-Based Agent) | The system acts as a **Utility-Based Intelligent Agent**: it perceives user financial telemetry, reasons over risk/return utility, searches the web environment for market indicators, and acts by generating optimized advisory strategies. | `agent/financial_agent.py`<br>`agent/peas_model.py` |
| **2. Expert Systems** | • Conventional vs. Expert Systems<br>• Structure of ES (KB + Inference Engine + User Interface)<br>• Knowledge Engineer Role<br>• Explanation Facility | Implements a **Rule-Based Expert System** using production rules (`IF-THEN`). Contains a dedicated **Explanation Facility** that outputs the exact rationale for why specific budget cuts or equity limits were mandated. | `expert_system/engine.py`<br>`expert_system/rules.py` |
| **3. Knowledge Representation** | • Production Systems<br>• Frame Systems<br>• Propositional & Predicate Logic | Financial profiles are structured as **Frames** (slots: income, liabilities, goals, risk appetite). Domain expertise is encoded as formal **Production Rules** over these frames. | `expert_system/frames.py`<br>`schemas.py` |
| **4. Fuzzy Logic** | • Crisp vs. Fuzzy Logic<br>• Membership Functions (Triangular/Trapezoidal)<br>• Fuzzy Inference (Mamdani)<br>• Defuzzification | Replaces arbitrary binary risk scores with **Fuzzy Risk Profiling**. Takes continuous inputs (Age, Time Horizon, Volatility Tolerance) and computes degree of membership in *Conservative*, *Moderate*, or *Aggressive* categories. | `fuzzy_logic/risk_evaluator.py`<br>`fuzzy_logic/membership.py` |
| **5. Search Techniques** | • Heuristic Search<br>• Goal Search Strategies<br>• State Space Exploration | Implements a **Heuristic Goal-Seeking Optimizer** to determine the optimal monthly investment split across competing goals (e.g. Retirement vs. Home Down Payment vs. Debt Avalanche). | `expert_system/goal_search.py` |
| **6. Neural Networks & Modern AI** | • Deep Neural Representations<br>• Transformer Architectures<br>• Pre-trained Foundation Models | Uses pre-trained Transformer LLMs (Deep Neural Networks) with retrieval grounding to convert structured rules, live web search indices, and user queries into articulate natural language recommendations. | `agent/llm_client.py` |

---

## 🧠 Detailed Academic Deep Dive

### 1. Intelligent Agent Formalization (PEAS Model)
When professors ask you to define the Agent formally:
- **Performance Measure (P)**: Maximizing financial goal attainment, portfolio Sharpe/safety ratio, minimizing high-interest debt risk, adherence to safety rules.
- **Environment (E)**: User profile, market inflation, interest rates, live stock index metrics, real-time economic news via web search.
- **Actuators (A)**: Advisory report, interactive asset allocation charts, rule violation warnings, risk profile recommendations.
- **Sensors (S)**: User input questionnaires, Web Search APIs (DuckDuckGo/Tavily), financial market data feeds.
- **Agent Type**: **Utility-based Agent** (trades off risk vs. return to maximize user financial utility).

### 2. Expert System Architecture vs. Conventional Software
| Component | Conventional Program | FinWise Expert System |
| :--- | :--- | :--- |
| **Knowledge Handling** | Hardcoded in spaghetti conditional code | Separated cleanly into an independent **Knowledge Base** (`rules.py`) |
| **Reasoning Mechanism** | Rigid procedural execution | Generalized **Inference Engine** (`engine.py`) using forward-chaining |
| **Transparency** | Silent return values | Built-in **Explanation Facility** explaining *why* rule $R_i$ fired |

### 3. Fuzzy Logic vs. Crisp Logic in Risk Profiling
- **Traditional Crisp Approach**: 
  - *If Age > 45, Risk = Low.* (Flawed: A 44-year-old and 46-year-old get completely different results).
- **FinWise Fuzzy Approach**:
  - A 45-year-old belongs $\mu = 0.5$ to *Young* and $\mu = 0.5$ to *Middle-Aged*.
  - Degree of truth smoothly transitions across membership functions, resulting in continuous, nuanced risk quantification.

---

## 🎯 Viva Q&A Cheat Sheet for the Team

**Q1: Why didn't you just use ChatGPT/Gemini directly with web browsing?**
> *Answer*: "Pure LLMs are non-deterministic, frequently hallucinate arithmetic calculations, and lack transparency. Furthermore, in high-stakes financial domains, regulatory compliance requires deterministic rule enforcement. Our hybrid architecture uses an Expert System and Fuzzy Logic to guarantee mathematical and rule-based safety, while the LLM acts as the communicative and synthesis layer."

**Q2: Which inference method does your Expert System use?**
> *Answer*: "It uses **Forward Chaining (Data-Driven Reasoning)**. It starts from known facts (user's monthly income, expenses, debts) and repeatedly fires matching production rules to infer new facts (emergency fund deficit, surplus investable cash, asset allocation restrictions)."

**Q3: How does your agent interact with the external world?**
> *Answer*: "It follows the classic Perception-Action cycle. When asked about current market conditions, it perceives the question, autonomously triggers a search tool action in its environment, digests the search results, and formulates the advisory response."
