# 👥 Parallel Work Division Plan for Team of 4

To ensure that all 4 team members can work **concurrently without blocking one another or having Git merge conflicts**, the project is partitioned into 4 decoupled subsystems connected through strictly defined [API Contracts](file:///c:/Users/anshu/OneDrive/Desktop/ai-project-financial-advisory-system/docs/API_CONTRACTS.md).

---

## 🧭 Team Responsibility Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                          FINWISE AI SYSTEM                             │
├──────────────────┬──────────────────┬──────────────────┬───────────────┤
│  ARYAN           │ ANSHUMAN         │ ZAID             │ AMAN          │
│  (Person 1: UI)  │ (Person 2: Back) │ (Person 3: Agent)│ (Person 4: ES)│
├──────────────────┼──────────────────┼──────────────────┼───────────────┤
│ • UI/UX Research │ • Base Scaffolding│ • OpenRouter API │ • Rule Engine │
│ • Theme & Palettes│ • FastAPI Server │ • Search Provider│ • Knowledge   │
│ • Component Libs │ • Session State  │ • PydanticAI /   │   Base Rules  │
│ • Onboarding UI  │ • DB & History   │   Agent Loop     │ • Fuzzy Logic │
│ • Allocation Pie │ • API Endpoints  │ • Live Retrieval │ • Heuristic   │
│ • Chat Assistant │ • Mock Provider  │ • Prompt Grounding│  Goal Search │
└──────────────────┴──────────────────┴──────────────────┴───────────────┘
```

---

## 👤 Aryan (Person 1): Frontend & UI/UX Specialist

### Role Summary
Owns the entire client-facing web application, ensuring a modern, responsive, and intuitive financial advisory experience.

### ⚠️ Mandatory Phase 0: UI/UX Research & Mock Themes (Before Writing Code)
Before writing frontend code, Aryan must complete these steps:
1. **Research Modern Agent UI Patterns**:
   - Study conversational agent interfaces: streaming chat bubbles, expandable reasoning/rule-trace accordions, clickable citation pills/badges, and interactive disclaimer banners.
   - Explore modern component libraries & design systems (e.g., 21st.dev, Magic UI, Aceternity UI, shadcn agent patterns).
2. **Select Design Tokens & Themes**:
   - Curate a distinct color palette: Modern Fintech Dark Mode (e.g., Deep Slate `#0B0F19`, Emerald Green Accent `#10B981`, Indigo Accent `#6366F1`) or clean Light Mode.
   - Select modern typography from Google Fonts (*Outfit*, *Plus Jakarta Sans*, or *Inter*).
   - Mock/wireframe the 3 core views before coding:
     1. Financial Onboarding Form (Multi-step wizard).
     2. Interactive Dashboard (Asset allocation doughnut chart, 50/30/20 budget bars, fired expert rules card).
     3. Financial Advisory Chat Assistant (with rule grounding citations).

### Assigned Files / Modules
- `frontend/`
  - `index.html` (Semantic HTML5 layout, meta tags, Google Fonts)
  - `css/styles.css` (Tailwind / Custom CSS with modern dark/light styling, glassmorphism)
  - `js/api.js` (Fetch calls to Person 2's FastAPI endpoints)
  - `js/charts.js` (Chart.js / ApexCharts for asset allocation pie chart, budget bar chart)
  - `js/chat.js` (Streaming or asynchronous financial chat UI with citation bubbles)
  - `js/onboarding.js` (Multi-step form for income, expenses, debts, goals, risk tolerance)

### Work Execution (Non-Cyclical Flow)
- **Phase 1 (While backend is built)**: Completes UI/UX research, curates design tokens/themes, and builds the visual HTML/CSS component structures (forms, chart containers, chat window, rule accordion).
- **Phase 2 (Once Anshuman hands off the live backend)**: Connects `api.js` directly to the live backend. No throwaway mock adapters needed.
- **Done Once**: Once connected and styled, Aryan's work is complete. No circling back.

### Milestones & Deliverables
1. **Milestone 1**: UI/UX research, component curation (21st.dev/Magic UI patterns), and design theme selection.
2. **Milestone 2**: HTML5/CSS layout for Onboarding Questionnaire and Dashboard cards.
3. **Milestone 3**: Connect directly to Anshuman's live FastAPI endpoints (charts, rule display, and chat).
4. **Milestone 4**: Final visual polish, responsive testing, and PDF/Print plan export.

---

## 👤 Anshuman (Person 2): Core Backend & API Orchestrator Lead

### Role Summary
Builds the server infrastructure, coordinates requests between the Frontend (Aryan), the Expert System (Aman), and the LLM Agent (Zaid), and manages data persistence.

### Assigned Files / Modules
- `backend/`
  - `main.py` (FastAPI app entry point, CORS configuration, health checks)
  - `routers/advisory.py` (Endpoint for `/evaluate`, `/chat`, `/history`)
  - `services/orchestrator.py` (Directly wires Aman's engine and Zaid's agent)
  - `models/database.py` (SQLite setup via SQLAlchemy for sessions and chat history)
  - `schemas.py` (Pydantic request/response models matching API Contracts)
  - `requirements.txt` (Server dependencies: fastapi, uvicorn, pydantic, etc.)

### Work Execution (Non-Cyclical Flow)
- **Zero Mock Waste**: Anshuman does not write throwaway mock stubs.
- **Input**: Receives completed, verified Python functions from Aman (`evaluate_financial_profile`) and Zaid (`generate_advisory_report`).
- **Direct Build**: Implements the Pydantic schemas, SQLite session models, and connects Aman's logic + Zaid's agent directly into `services/orchestrator.py`.
- **Hand-off**: Launches the live FastAPI server and delivers the verified REST API to Aryan.
- **Done Once**: Once the live API passes Swagger tests (`/docs`), backend is complete. No circling back.

### Milestones & Deliverables
1. **Milestone 1**: Set up project environment, `requirements.txt`, and Pydantic validation schemas.
2. **Milestone 2**: Build SQLite database models for storing user profiles, advice history, and chat sessions.
3. **Milestone 3**: Wire Aman's finished engine and Zaid's finished agent inside `services/orchestrator.py`.
4. **Milestone 4**: Verify all endpoints via FastAPI Swagger UI (`http://localhost:8000/docs`) and deliver live API to Aryan.

---

## 👤 Zaid (Person 3): LLM & Web Search Intelligent Agent

### Role Summary
Builds the Intelligent Agent module (Perception-Reasoning-Action), integrating LLM API calls with real-time web search for financial news and market benchmarks.

### Assigned Files / Modules
- `backend/agent/`
  - `financial_agent.py` (Agent loop: built with PydanticAI / lightweight tool-calling agent)
  - `search_tools.py` (DuckDuckGo search / financial market data tool wrapper)
  - `prompt_templates.py` (System prompts, persona definition, citation instructions)
  - `openrouter_client.py` (OpenRouter API client supporting models like Llama 3.3, DeepSeek, Claude, Gemini)
  - `test_agent_standalone.py` (Local CLI test script to verify agent search + prompt)

### Work Execution (Non-Cyclical Flow)
- **Input**: Takes Aman's completed expert rule output structure.
- **Direct Build**: Builds the OpenRouter client, DuckDuckGo search tool, and PydanticAI agent loop. Grounds the prompts so the LLM strictly explains Aman's real numbers with web citations.
- **Verification**: Tests the agent completely in `test_agent_standalone.py`.
- **Hand-off**: Hands the completed, tested `generate_advisory_report` and `handle_user_chat` functions to Anshuman.
- **Done Once**: Frozen and handed off. Zaid never touches or circles back to this code.

### Milestones & Deliverables
1. **Milestone 1**: Set up `openrouter_client.py` using OpenRouter's OpenAI-compatible endpoint (`https://openrouter.ai/api/v1`).
2. **Milestone 2**: Build `search_tools.py` using `duckduckgo-search` to fetch live inflation, interest rates, and market index trends.
3. **Milestone 3**: Implement the PydanticAI agent loop that ingests Aman's expert system allocation numbers and returns formatted reports with citations.
4. **Milestone 4**: Implement follow-up chat handler, run `test_agent_standalone.py`, and hand off finished module to Anshuman.

---

## 👤 Aman (Person 4): AI Expert System & Fuzzy Risk Engine (Syllabus Core)

### Role Summary
Builds the academic core of the project: the rule-based forward-chaining expert system, financial knowledge base, explanation facility, and fuzzy logic risk assessor.

### Assigned Files / Modules
- `backend/expert_system/`
  - `rules.py` (Financial production rules: emergency fund, 50-30-20, debt payoff, asset allocation)
  - `engine.py` (Forward-chaining inference engine + working memory)
  - `explanation.py` (Explanation facility generating human-readable rule audit trail)
  - `goal_search.py` (Heuristic goal optimizer: budget allocation search across competing goals)
- `backend/fuzzy_logic/`
  - `membership.py` (Triangular/Trapezoidal membership functions for Age, Horizon, Risk)
  - `risk_evaluator.py` (Mamdani fuzzy inference engine mapping inputs $\rightarrow$ crisp risk score)
  - `test_expert_standalone.py` (Local CLI test script to verify rules and fuzzy scoring)

### Work Execution (Non-Cyclical Flow)
- **Zero Dependencies**: Aman has zero dependencies on any teammate. Starts Day 1.
- **Direct Build**: Writes pure mathematical and rule-based Python logic for fuzzy risk assessment and forward chaining.
- **Verification**: Tests all calculations, rule firings, and explanations in `test_expert_standalone.py`.
- **Hand-off**: Hands the completed, tested `evaluate_financial_profile` function to Zaid and Anshuman.
- **Done Once**: Frozen and handed off. Aman never touches or circles back to this code.

### Milestones & Deliverables
1. **Milestone 1**: Implement fuzzy membership functions and the Mamdani risk evaluation system in `fuzzy_logic/`.
2. **Milestone 2**: Implement the Knowledge Base (`rules.py`) with 8–10 financial production rules.
3. **Milestone 3**: Build the Forward-Chaining Inference Engine (`engine.py`) and Explanation Facility (`explanation.py`).
4. **Milestone 4**: Validate via `test_expert_standalone.py` and hand off finished module to Zaid and Anshuman.

---

## ⚡ Strictly Non-Cyclical (Linear Assembly Line) Roadmap

This model eliminates all circular dependencies. **Each person finishes their work once, tests it, and hands it downstream.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       STRICT NON-CYCLICAL PIPELINE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [STEP 1] Aman (Starts Day 1, Zero Dependencies)                            │
│           Writes Fuzzy Logic + Expert System Rule Engine in Pure Python.    │
│           Verifies in test_expert_standalone.py.                            │
│           ★ COMPLETED & FROZEN -> Hands off to Zaid & Anshuman              │
│                                │                                            │
│                                ▼                                            │
│  [STEP 2] Zaid (Builds directly on Aman's real output)                      │
│           Builds OpenRouter client + DuckDuckGo search + PydanticAI agent.  │
│           Verifies in test_agent_standalone.py.                             │
│           ★ COMPLETED & FROZEN -> Hands off to Anshuman                     │
│                                │                                            │
│                                ▼                                            │
│  [STEP 3] Anshuman (Wires Aman's + Zaid's finished modules)                 │
│           Writes FastAPI endpoints, SQLite session store & Orchestrator.    │
│           Verifies live via Swagger docs (http://localhost:8000/docs).      │
│           ★ COMPLETED & FROZEN -> Delivers live API to Aryan                │
│                                │                                            │
│                                ▼                                            │
│  [STEP 4] Aryan (Builds UI directly against real, live API)                 │
│           (Researched UI/UX & built layout cards while Steps 1-3 ran).      │
│           Connects frontend fetch directly to Anshuman's live backend.      │
│           ★ COMPLETED -> Entire application works end-to-end!               │
│                                │                                            │
│                                ▼                                            │
│  [STEP 5] All 4 Members (Joint Finalization)                                │
│           Prepare viva presentation slides using docs/SYLLABUS_MAPPING.md.  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Why This Guarantees Zero Circling Back:
1. **No Throwaway Mocks**: Anshuman doesn't write mock endpoints only to rewrite them later. He writes the real orchestrator directly using Aman's and Zaid's completed modules.
2. **No Rewiring in Frontend**: Aryan doesn't build a mock frontend only to rewire it later. He designs the visual layouts and then hooks them directly to the real, running backend.
3. **Pure Forward Progress**: Once Aman finishes Step 1, he is done. Once Zaid finishes Step 2, he is done. Once Anshuman finishes Step 3, he is done. Once Aryan finishes Step 4, the product is done.
