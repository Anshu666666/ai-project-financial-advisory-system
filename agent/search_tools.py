"""
================================================================================
FINWISE AI – REAL-TIME FINANCIAL WEB SEARCH TOOL
Author: Zaid (Intelligent Agent & Web Search Lead)
================================================================================
Queries DuckDuckGo live search for real-time financial indicators, benchmark rates,
and market trends. Zero hard-coded statistics. Zero fabricated search results.
================================================================================
"""

import os
import logging
import warnings
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from dotenv import load_dotenv
from agent.schemas import Citation

load_dotenv()

# Suppress runtime warnings from duckduckgo_search renaming
warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

logger = logging.getLogger("finwise.search")

DEFAULT_MAX_RESULTS = int(os.getenv("SEARCH_MAX_RESULTS", "5"))
DEFAULT_SEARCH_TIMEOUT = int(os.getenv("SEARCH_TIMEOUT", "15"))


class DuckDuckGoSearchTool:
    """
    Real-time DuckDuckGo Web Search Tool.
    Queries the live internet for current financial information and extracts structured citations.
    """

    def __init__(
        self,
        max_results: int = DEFAULT_MAX_RESULTS,
        timeout: int = DEFAULT_SEARCH_TIMEOUT,
    ):
        self.max_results = max_results
        self.timeout = timeout

    def search(
        self,
        query: str,
        max_results: Optional[int] = None,
    ) -> List[Citation]:
        """
        Executes a real search query on DuckDuckGo and returns structured Citations.
        
        Args:
            query: Live financial search query string
            max_results: Maximum results to retrieve
            
        Returns:
            List of Citation objects with real titles, snippets, and URLs.
            Returns empty list if search fails or returns no results (no fake data).
        """
        limit = max_results or self.max_results
        results: List[Citation] = []

        if DDGS is None:
            logger.error("duckduckgo_search is not installed. Live web search cannot execute.")
            return []

        clean_query = query.strip()
        if not clean_query:
            return []

        try:
            with DDGS(timeout=self.timeout) as ddgs:
                raw_results = list(ddgs.text(clean_query, max_results=limit))

                # If query was too specific and returned 0, try a simplified 3-word keyword search
                if not raw_results and len(clean_query.split()) > 3:
                    words = clean_query.split()
                    simplified = " ".join(words[:3])
                    try:
                        raw_results = list(ddgs.text(simplified, max_results=limit))
                    except Exception:
                        pass

                for item in raw_results:
                    title = item.get("title", "").strip()
                    body = item.get("body", "").strip()
                    href = item.get("href", item.get("url", "")).strip()

                    if not href or not (href.startswith("http://") or href.startswith("https://")):
                        continue

                    # Derive clean source name from domain or publisher
                    source_name = item.get("source", "")
                    if not source_name and title:
                        source_name = title[:40]
                    try:
                        domain = urlparse(href).netloc.replace("www.", "")
                        if domain:
                            source_name = f"{domain}" + (f" ({source_name})" if source_name and source_name != domain else "")
                    except Exception:
                        pass

                    results.append(
                        Citation(
                            title=title if title else "Live Web Result",
                            source=source_name if source_name else "Live Search",
                            url=href,
                            snippet=body,
                        )
                    )

            return results

        except Exception as e:
            logger.error(f"DuckDuckGo live search error for query '{clean_query}': {e}")
            return []

    def get_market_benchmarks(self, country: str = "India") -> Dict[str, Any]:
        """
        Dynamically queries live macroeconomic benchmarks for financial grounding.
        Executes a targeted search query to retrieve real data.
        
        Returns:
            Dict containing:
                - 'market_summary': str (derived strictly from search or explicitly unverified)
                - 'citations': List[Citation]
        """
        query = f"{country} RBI monetary policy repo rate"
        citations = self.search(query, max_results=self.max_results)

        if citations:
            market_summary = (
                f"Dynamic macroeconomic context retrieved from {len(citations)} live web sources covering "
                f"central bank policy, benchmark interest rates, and economic indicators."
            )
        else:
            market_summary = "Current macroeconomic benchmarks could not be verified from available live search sources."

        return {
            "market_summary": market_summary,
            "citations": citations,
        }

    def search_for_profile_context(
        self,
        profile: Dict[str, Any],
        risk_category: str,
    ) -> List[Citation]:
        """
        Dynamically generates and executes a targeted query tailored to the user's specific financial goal and horizon.
        """
        goal = profile.get("financial_goal", "Wealth Creation")
        horizon = profile.get("investment_horizon_years", 5)

        if risk_category.lower() == "aggressive":
            query = f"Nifty equity index fund returns {horizon} years"
        elif risk_category.lower() == "conservative":
            query = f"debt fund fixed deposit rates {horizon} years"
        else:
            query = f"balanced mutual fund allocation {goal}"

        return self.search(query, max_results=3)


# Singleton helper instance
search_tool = DuckDuckGoSearchTool()


def search_financial_market(query: str, max_results: Optional[int] = None) -> List[Citation]:
    """Convenience functional wrapper for DDG live search."""
    return search_tool.search(query, max_results=max_results)


def get_current_market_benchmarks(country: str = "India") -> Dict[str, Any]:
    """Convenience functional wrapper to fetch dynamic market benchmarks."""
    return search_tool.get_market_benchmarks(country=country)
