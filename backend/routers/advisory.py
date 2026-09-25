"""
================================================================================
FINWISE AI – ADVISORY REST ROUTER
Author: Anshuman (Core Backend & API Orchestration Lead)
================================================================================
Exposes production REST endpoints for financial profile evaluation, interactive
chat advisory, and historical session retrieval.
================================================================================
"""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, status

import backend.models.database as db
from backend.schemas import (
    ChatMessageItem,
    ChatRequest,
    ChatResponse,
    EvaluateRequest,
    EvaluateResponse,
    SessionDetailResponse,
    SessionListItem,
)
from backend.services.orchestrator import chat_with_advisor, evaluate_financial_profile

logger = logging.getLogger("finwise.router")

router = APIRouter(prefix="/advisory", tags=["Financial Advisory & Planning"])


@router.post(
    "/evaluate",
    response_model=EvaluateResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate Financial Profile & Synthesize Advisory Plan",
    description="Executes Fuzzy Risk Inference, Rule-Based Expert System checks, live Web Search, and PydanticAI Advisory Report synthesis.",
)
async def evaluate_profile_endpoint(request: EvaluateRequest) -> EvaluateResponse:
    try:
        response = await evaluate_financial_profile(request)
        return response
    except Exception as e:
        logger.error(f"Error during profile evaluation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Financial evaluation failed: {str(e)}",
        )


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Interactive Advisory Chat Follow-Up",
    description="Answers user queries grounded strictly in their evaluated financial plan and expert rules.",
)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    try:
        response = await chat_with_advisor(request)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error during advisory chat: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Advisory chat query failed: {str(e)}",
        )


@router.get(
    "/history/{session_id}",
    response_model=SessionDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Session History & Saved Advisory Plan",
)
async def get_session_history_endpoint(session_id: str) -> SessionDetailResponse:
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID '{session_id}' not found.",
        )

    chat_messages = db.get_chat_history(session_id)
    formatted_messages = [
        ChatMessageItem(
            id=m["id"],
            session_id=m["session_id"],
            role=m["role"],
            message=m["message"],
            timestamp=m["timestamp"],
        )
        for m in chat_messages
    ]

    return SessionDetailResponse(
        session_id=session["session_id"],
        created_at=session["created_at"],
        user_name=session["user_name"],
        profile=session["profile"],
        fuzzy_assessment=session["fuzzy_assessment"],
        expert_plan=session["expert_plan"],
        advisory_report=session["advisory_report"],
        chat_history=formatted_messages,
    )


@router.get(
    "/sessions",
    response_model=List[SessionListItem],
    status_code=status.HTTP_200_OK,
    summary="List Recent Financial Evaluation Sessions",
)
async def list_sessions_endpoint() -> List[SessionListItem]:
    try:
        sessions = db.list_sessions(limit=50)
        return [
            SessionListItem(
                session_id=s["session_id"],
                user_name=s["user_name"],
                risk_category=s["risk_category"],
                created_at=s["created_at"],
            )
            for s in sessions
        ]
    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sessions list.",
        )
