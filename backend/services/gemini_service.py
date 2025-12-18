"""
Gemini AI Service
Handles communication with Google Gemini AI for agent responses
"""

import google.generativeai as genai
from typing import List, Dict, Optional
from config import settings
from google.api_core.exceptions import ResourceExhausted


class GeminiService:
    """Service for interacting with Google Gemini AI"""

    def __init__(self):
        """Initialize Gemini service with API key and model configuration"""
        genai.configure(api_key=settings.GEMINI_API_KEY)

        self.generation_config = {
            "temperature": settings.GEMINI_TEMPERATURE,
            "max_output_tokens": settings.GEMINI_MAX_TOKENS,
        }

        model_name = "models/gemini-2.5-flash"
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config
        )

    async def chat_with_agent(
        self,
        agent_id: str,
        system_prompt: str,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        game_context: Optional[Dict] = None
    ) -> str:
        """
        Send a message to an AI agent and get response.
        """
        full_prompt = self._build_full_prompt(
            system_prompt=system_prompt,
            conversation_history=conversation_history,
            user_message=user_message,
            game_context=game_context
        )

        try:
            # Generate response from Gemini
            response = self.model.generate_content(full_prompt)

            if not response or not response.text:
                return "Beklager, jeg fikk ikke generert et svar. Vennligst prøv igjen."

            return response.text.strip()

        except ResourceExhausted as e:
            print(f"Gemini API Quota Exceeded for agent {agent_id}: {str(e)}")
            return "Beklager, den daglige kvoten for AI-kall er nådd. Prøv igjen i morgen."
        except Exception as e:
            print(f"Gemini API error for agent {agent_id}: {str(e)}")
            return f"Beklager, det oppstod en teknisk feil med AI-tjenesten. Vennligst prøv igjen om litt."

    def _build_full_prompt(
        self,
        system_prompt: str,
        conversation_history: List[Dict[str, str]],
        user_message: str,
        game_context: Optional[Dict] = None
    ) -> str:
        """
        Build the complete prompt including system instructions, context, and history.

        Args:
            system_prompt: The agent's system prompt (personality, rules, etc.)
            conversation_history: Previous messages in this conversation
            user_message: The current user message
            game_context: Current game state (budget, commitments, deadline, etc.)

        Returns:
            Complete formatted prompt for Gemini
        """
        prompt_parts = []

        # 1. System prompt (agent personality and rules)
        prompt_parts.append("# SYSTEM INSTRUCTIONS")
        prompt_parts.append(system_prompt)
        prompt_parts.append("")

        # 2. Game context (if provided)
        if game_context:
            prompt_parts.append("# CURRENT GAME STATE")
            prompt_parts.append(self._format_game_context(game_context))
            prompt_parts.append("")

        # 3. Conversation history
        if conversation_history:
            prompt_parts.append("# CONVERSATION HISTORY")
            for msg in conversation_history:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")

                if role == "user":
                    prompt_parts.append(f"BRUKER: {content}")
                elif role == "agent":
                    prompt_parts.append(f"DEG: {content}")
            prompt_parts.append("")

        # 4. Current user message
        prompt_parts.append("# CURRENT USER MESSAGE")
        prompt_parts.append(f"BRUKER: {user_message}")
        prompt_parts.append("")

        # 5. Response instruction
        prompt_parts.append("# YOUR RESPONSE")
        prompt_parts.append("Respond to the user's message above in Norwegian. Stay in character. Follow all rules in your system instructions.")
        prompt_parts.append("")
        prompt_parts.append("DEG:")

        return "\n".join(prompt_parts)

    def _format_game_context(self, game_context: Dict) -> str:
        """
        Format game context into readable text for the AI.

        Args:
            game_context: Dictionary with budget, commitments, deadline, etc.

        Returns:
            Formatted context string
        """
        context_parts = []

        # Budget information
        if "total_budget" in game_context:
            total = game_context.get("total_budget", 700_000_000)
            available = game_context.get("available_budget", 310_000_000)
            used = game_context.get("current_budget_used", 0)
            remaining = available - used

            context_parts.append(f"BUDSJETT:")
            context_parts.append(f"  - Totalt budsjett: {self._format_nok(total)}")
            context_parts.append(f"  - Tilgjengelig budsjett: {self._format_nok(available)}")
            context_parts.append(f"  - Brukt så langt: {self._format_nok(used)}")
            context_parts.append(f"  - Gjenstående: {self._format_nok(remaining)}")

        # Deadline
        if "deadline_date" in game_context:
            deadline = game_context.get("deadline_date")
            context_parts.append(f"\nFRIST: {deadline}")

        # Commitments made
        if "commitments" in game_context:
            commitments = game_context.get("commitments", [])
            if commitments:
                context_parts.append(f"\nAKSEPTERTE TILBUD:")
                for commitment in commitments:
                    wbs_id = commitment.get("wbs_id", "")
                    price = commitment.get("committed_price", 0)
                    duration = commitment.get("committed_duration_weeks", 0)
                    context_parts.append(f"  - {wbs_id}: {self._format_nok(price)}, {duration} uker")

        # WBS areas not yet committed
        if "uncommitted_wbs" in game_context:
            uncommitted = game_context.get("uncommitted_wbs", [])
            if uncommitted:
                context_parts.append(f"\nGJENSTÅENDE WBS-OMRÅDER:")
                for wbs in uncommitted:
                    context_parts.append(f"  - {wbs}")

        return "\n".join(context_parts)

    def _format_nok(self, amount: float) -> str:
        """
        Format amount as Norwegian Kroner.

        Args:
            amount: Amount in NOK

        Returns:
            Formatted string (e.g., "105 MNOK" or "105 000 000 NOK")
        """
        if amount >= 1_000_000:
            # Format as MNOK (millions)
            mnok = amount / 1_000_000
            if mnok == int(mnok):
                return f"{int(mnok)} MNOK"
            else:
                return f"{mnok:.1f} MNOK"
        else:
            # Format with space as thousand separator
            return f"{amount:,.0f} NOK".replace(",", " ")


# Global service instance
_gemini_service: Optional[GeminiService] = None


def get_gemini_service() -> GeminiService:
    """
    Get or create the global Gemini service instance.

    Returns:
        GeminiService instance
    """
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
