"""
================================================================================
FINWISE AI – OPENROUTER API CLIENT
Author: Zaid (Intelligent Agent & Web Search Lead)
================================================================================
Real OpenRouter LLM API client supporting configurable models (e.g. Gemini 2.0 Flash,
DeepSeek V3, Llama 3.3 70B, Claude 3.5 Sonnet) via OpenRouter's OpenAI-compatible API.
Zero fake responses. Zero silent fallbacks. Clear, structured error handling.
================================================================================
"""

import os
import logging
from typing import Any, Dict, List, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("finwise.openrouter")

# Configurable defaults from environment
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-3.7-flash")
DEFAULT_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_TIMEOUT = float(os.getenv("OPENROUTER_TIMEOUT", "60.0"))


class OpenRouterAuthError(RuntimeError):
    """Raised when the OpenRouter API key is missing or invalid."""
    pass


class OpenRouterAPIError(RuntimeError):
    """Raised when the OpenRouter API encounters an HTTP or server error."""
    pass


class OpenRouterClient:
    """
    Real OpenRouter API Client for FinWise AI Intelligent Agent.
    Executes actual network requests to OpenRouter's chat completions endpoint.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: Optional[str] = None,
        base_url: Optional[str] = None,
        site_url: str = "https://github.com/Anshu666666/ai-project-financial-advisory-system",
        site_name: str = "FinWise AI Financial Advisory",
        timeout: Optional[float] = None,
    ):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "") if api_key is None else api_key
        self.default_model = default_model or os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
        self.base_url = base_url or os.getenv("OPENROUTER_BASE_URL", DEFAULT_BASE_URL)
        self.site_url = site_url
        self.site_name = site_name
        self.timeout = timeout or float(os.getenv("OPENROUTER_TIMEOUT", str(DEFAULT_TIMEOUT)))

    @property
    def has_api_key(self) -> bool:
        """Checks if an API key is configured."""
        return bool(self.api_key and len(self.api_key.strip()) > 5 and not self.api_key.startswith("your_openrouter_api_key"))

    def _get_headers(self) -> Dict[str, str]:
        if not self.has_api_key:
            raise OpenRouterAuthError(
                "OPENROUTER_API_KEY is not configured. Please set OPENROUTER_API_KEY in your .env file or environment."
            )

        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key.strip()}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
        }

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1500,
    ) -> str:
        """
        Executes a REAL synchronous Chat Completion via the OpenRouter API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Optional model identifier override
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum output tokens
            
        Returns:
            Generated response string from the actual LLM.
            
        Raises:
            OpenRouterAuthError: If API key is missing or invalid.
            OpenRouterAPIError: If the remote API fails or returns an error.
        """
        if not self.has_api_key:
            raise OpenRouterAuthError(
                "OPENROUTER_API_KEY is missing. Configure a valid key in .env to perform live LLM requests."
            )

        target_model = model or self.default_model
        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        url = f"{self.base_url.rstrip('/')}/chat/completions"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    url,
                    headers=self._get_headers(),
                    json=payload,
                )

                if response.status_code == 401:
                    raise OpenRouterAuthError(
                        "OpenRouter authentication failed (401 Unauthorized). Please check your OPENROUTER_API_KEY."
                    )
                elif response.status_code == 429:
                    raise OpenRouterAPIError(
                        f"OpenRouter rate limit reached (429): {response.text}"
                    )

                response.raise_for_status()
                data = response.json()

                if "choices" not in data or len(data["choices"]) == 0:
                    raise OpenRouterAPIError(f"OpenRouter returned unexpected response format: {data}")

                content = data["choices"][0]["message"]["content"]
                if not content:
                    raise OpenRouterAPIError("OpenRouter returned empty content in response.")

                return content.strip()

        except httpx.HTTPStatusError as e:
            raise OpenRouterAPIError(
                f"OpenRouter API HTTP error [{e.response.status_code}]: {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            raise OpenRouterAPIError(
                f"OpenRouter network connection failed: {e}"
            ) from e

    async def chat_completion_async(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 2500,
    ) -> str:
        """
        Executes a REAL asynchronous Chat Completion via the OpenRouter API.
        """
        if not self.has_api_key:
            raise OpenRouterAuthError(
                "OPENROUTER_API_KEY is missing. Configure a valid key in .env to perform live LLM requests."
            )

        target_model = model or self.default_model
        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        url = f"{self.base_url.rstrip('/')}/chat/completions"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    headers=self._get_headers(),
                    json=payload,
                )

                if response.status_code == 401:
                    raise OpenRouterAuthError(
                        "OpenRouter authentication failed (401 Unauthorized). Check your OPENROUTER_API_KEY."
                    )
                elif response.status_code == 429:
                    raise OpenRouterAPIError(
                        f"OpenRouter rate limit reached (429): {response.text}"
                    )

                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()

        except httpx.HTTPStatusError as e:
            raise OpenRouterAPIError(
                f"OpenRouter async HTTP error [{e.response.status_code}]: {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            raise OpenRouterAPIError(
                f"OpenRouter async connection failed: {e}"
            ) from e
