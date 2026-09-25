"""
================================================================================
FINWISE AI – STEP 3 BACKEND STANDALONE VERIFICATION SUITE
Author: Anshuman (Core Backend & API Orchestration Lead)
================================================================================
Verifies all Step 3 backend criteria using FastAPI TestClient:
- Health check & diagnostics endpoint
- Input validation (catches negative incomes, invalid ages, and malformed schemas)
- Complete evaluation pipeline execution (Aman's Fuzzy + Expert System + Zaid's Agent)
- SQLite database persistence of sessions and profiles
- Contextual chat follow-up grounded in active session plan
- Session history retrieval and session listing
================================================================================
"""

import sys
from pathlib import Path
from starlette.testclient import TestClient

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app

client = TestClient(app)


def print_test_row(test_num: int, total: int, name: str, status: str, detail: str = ""):
    dots = "." * max(2, 54 - len(name) - len(str(test_num)) - len(str(total)))
    print(f"[{test_num}/{total}] {name} {dots} [{status}] {detail}")


def run_backend_verification():
    print("\n" + "#" * 80)
    print("# FINWISE AI – STEP 3 BACKEND & API ORCHESTRATION VERIFICATION")
    print("# Lead: Anshuman (Core Backend & API Lead)")
    print("#" * 80)

    total_tests = 8
    passed_tests = 0

    # -------------------------------------------------------------------------
    # Test 1: Health Check Endpoint
    # -------------------------------------------------------------------------
    try:
        res = client.get("/api/v1/health")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        data = res.json()
        assert data["database_connected"] is True
        assert data["status"] in ("healthy", "degraded")
        print_test_row(1, total_tests, "GET /api/v1/health diagnostic endpoint", "PASS", f"(Status: {data['status']})")
        passed_tests += 1
    except Exception as e:
        print_test_row(1, total_tests, "GET /api/v1/health diagnostic endpoint", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 2: Input Validation (Invalid Age & Negative Income)
    # -------------------------------------------------------------------------
    try:
        bad_payload = {
            "user_name": "Test User",
            "age": 12,  # Invalid: below 18
            "monthly_income": -50000.0,  # Invalid: negative
            "monthly_expenses": 20000.0,
        }
        res = client.post("/api/v1/advisory/evaluate", json=bad_payload)
        assert res.status_code == 422, f"Expected 422 Validation Error, got {res.status_code}"
        print_test_row(2, total_tests, "POST /api/v1/advisory/evaluate input validation", "PASS", "(Correctly rejected invalid data)")
        passed_tests += 1
    except Exception as e:
        print_test_row(2, total_tests, "POST /api/v1/advisory/evaluate input validation", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 3: Valid Financial Profile Evaluation (Full Pipeline)
    # -------------------------------------------------------------------------
    valid_payload = {
        "user_name": "Aarav Sharma",
        "age": 24,
        "monthly_income": 65000.0,
        "monthly_expenses": 32000.0,
        "current_savings": 45000.0,
        "total_debt": 120000.0,
        "monthly_emi": 5000.0,
        "debt_interest_rate": 11.5,
        "investment_horizon_years": 5,
        "loss_tolerance": "medium",
        "income_stability": "stable",
        "primary_goal": "wealth_creation",
        "goal_target_amount": 2500000.0,
        "tax_regime": "new",
        "notes": "Interested in tech stocks and building an emergency buffer.",
    }

    session_id = None
    try:
        res = client.post("/api/v1/advisory/evaluate", json=valid_payload)
        assert res.status_code == 200, f"Expected 200 OK, got {res.status_code}: {res.text}"
        data = res.json()

        assert data["status"] == "success"
        assert "session_id" in data
        assert data["session_id"].startswith("sess_")
        session_id = data["session_id"]

        # Validate Fuzzy assessment preservation
        assert data["fuzzy_risk_assessment"]["crisp_score"] > 0
        assert data["fuzzy_risk_assessment"]["category"] in ("Conservative", "Moderate", "Aggressive")

        # Validate Expert System deterministic allocation
        alloc = data["expert_system_plan"]["recommended_allocation"]
        assert alloc["total_percentage"] == 100.0
        assert alloc["equity_percentage"] + alloc["debt_bonds_percentage"] + alloc["gold_commodities_percentage"] + alloc["liquid_cash_percentage"] == 100.0

        # Validate Actionable rules
        rules = data["expert_system_plan"]["actionable_rules_fired"]
        assert len(rules) > 0

        # Validate Report text
        assert len(data["comprehensive_advisory_report"]) > 100

        print_test_row(
            3,
            total_tests,
            "POST /api/v1/advisory/evaluate complete pipeline",
            "PASS",
            f"(Session: {session_id}, Risk: {data['fuzzy_risk_assessment']['category']})",
        )
        passed_tests += 1
    except Exception as e:
        print_test_row(3, total_tests, "POST /api/v1/advisory/evaluate complete pipeline", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 4: SQLite Database Session Persistence
    # -------------------------------------------------------------------------
    try:
        assert session_id is not None, "Cannot test persistence without session_id"
        res = client.get(f"/api/v1/advisory/history/{session_id}")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        hist_data = res.json()
        assert hist_data["session_id"] == session_id
        assert hist_data["user_name"] == "Aarav Sharma"
        assert "expert_plan" in hist_data
        print_test_row(4, total_tests, "GET /api/v1/advisory/history/{session_id}", "PASS", "(Session loaded from SQLite)")
        passed_tests += 1
    except Exception as e:
        print_test_row(4, total_tests, "GET /api/v1/advisory/history/{session_id}", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 5: Contextual Chat Follow-Up Grounded in Plan
    # -------------------------------------------------------------------------
    try:
        assert session_id is not None
        chat_payload = {
            "session_id": session_id,
            "message": "Should I invest in crypto or pay off my 11.5% debt first?",
        }
        res = client.post("/api/v1/advisory/chat", json=chat_payload)
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        chat_data = res.json()
        assert chat_data["status"] == "success"
        assert len(chat_data["reply"]) > 20
        assert chat_data["session_id"] == session_id
        print_test_row(5, total_tests, "POST /api/v1/advisory/chat grounded reply", "PASS")
        passed_tests += 1
    except Exception as e:
        print_test_row(5, total_tests, "POST /api/v1/advisory/chat grounded reply", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 6: Chat Message Persistence in Database
    # -------------------------------------------------------------------------
    try:
        assert session_id is not None
        res = client.get(f"/api/v1/advisory/history/{session_id}")
        assert res.status_code == 200
        hist_data = res.json()
        assert len(hist_data["chat_history"]) >= 2  # 1 user + 1 assistant
        roles = [m["role"] for m in hist_data["chat_history"]]
        assert "user" in roles
        assert "assistant" in roles
        print_test_row(6, total_tests, "Conversational chat memory in SQLite", "PASS", f"({len(hist_data['chat_history'])} messages stored)")
        passed_tests += 1
    except Exception as e:
        print_test_row(6, total_tests, "Conversational chat memory in SQLite", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 7: Chat on Invalid Session (Error Handling)
    # -------------------------------------------------------------------------
    try:
        bad_chat = {
            "session_id": "sess_non_existent_12345",
            "message": "Hello advisor?",
        }
        res = client.post("/api/v1/advisory/chat", json=bad_chat)
        assert res.status_code == 404, f"Expected 404 Not Found, got {res.status_code}"
        print_test_row(7, total_tests, "POST /api/v1/advisory/chat 404 for unknown session", "PASS")
        passed_tests += 1
    except Exception as e:
        print_test_row(7, total_tests, "POST /api/v1/advisory/chat 404 for unknown session", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Test 8: Sessions Listing Endpoint
    # -------------------------------------------------------------------------
    try:
        res = client.get("/api/v1/advisory/sessions")
        assert res.status_code == 200
        sessions_list = res.json()
        assert len(sessions_list) >= 1
        assert any(s["session_id"] == session_id for s in sessions_list)
        print_test_row(8, total_tests, "GET /api/v1/advisory/sessions dashboard listing", "PASS", f"({len(sessions_list)} sessions listed)")
        passed_tests += 1
    except Exception as e:
        print_test_row(8, total_tests, "GET /api/v1/advisory/sessions dashboard listing", "FAIL", str(e))

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    if passed_tests == total_tests:
        print(f">>> STEP 3 STATUS: ALL {total_tests}/{total_tests} BACKEND TESTS PASSED (100% SUCCESS RATE)! <<<")
        print("Anshuman's backend is fully verified, live, and ready for Aryan's UI!")
    else:
        print(f">>> STEP 3 STATUS: {passed_tests}/{total_tests} TESTS PASSED <<<")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_backend_verification()
