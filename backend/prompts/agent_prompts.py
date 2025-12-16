"""
AI Agent System Prompts Loader
Extracts and provides system prompts for all 4 negotiation agents
"""

import os
import re
from pathlib import Path

# Path to the markdown file with agent prompts
PROMPTS_FILE = Path(__file__).parent.parent.parent / "docs" / "AI_AGENT_SYSTEM_PROMPTS.md"

def load_agent_prompts() -> dict[str, str]:
    """
    Load all agent system prompts from the markdown documentation file.
    Returns a dictionary mapping agent_id to system prompt.
    """
    if not PROMPTS_FILE.exists():
        raise FileNotFoundError(f"Agent prompts file not found: {PROMPTS_FILE}")

    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract the system prompts (content between ```markdown and ``` markers)
    prompts = {}

    # Agent 1: Anne-Lise Berg (Owner)
    owner_match = re.search(
        r'## Agent 1:.*?```markdown\n(.*?)```',
        content,
        re.DOTALL
    )
    if owner_match:
        prompts["anne-lise-berg"] = owner_match.group(1).strip()

    # Agent 2: Bjørn Eriksen (Supplier 1)
    supplier1_match = re.search(
        r'## Agent 2:.*?```markdown\n(.*?)```',
        content,
        re.DOTALL
    )
    if supplier1_match:
        prompts["bjorn-eriksen"] = supplier1_match.group(1).strip()

    # Agent 3: Kari Andersen (Supplier 2)
    supplier2_match = re.search(
        r'## Agent 3:.*?```markdown\n(.*?)```',
        content,
        re.DOTALL
    )
    if supplier2_match:
        prompts["kari-andersen"] = supplier2_match.group(1).strip()

    # Agent 4: Per Johansen (Supplier 3)
    supplier3_match = re.search(
        r'## Agent 4:.*?```markdown\n(.*?)```',
        content,
        re.DOTALL
    )
    if supplier3_match:
        prompts["per-johansen"] = supplier3_match.group(1).strip()

    if len(prompts) != 4:
        raise ValueError(f"Expected 4 agent prompts, found {len(prompts)}")

    return prompts


# Load prompts once at module import
try:
    AGENT_PROMPTS = load_agent_prompts()
except Exception as e:
    print(f"WARNING: Could not load agent prompts: {e}")
    # Fallback to empty prompts (for testing purposes)
    AGENT_PROMPTS = {
        "anne-lise-berg": "",
        "bjorn-eriksen": "",
        "kari-andersen": "",
        "per-johansen": "",
    }


def get_agent_prompt(agent_id: str) -> str:
    """
    Get the system prompt for a specific agent.

    Args:
        agent_id: One of "anne-lise-berg", "bjorn-eriksen", "kari-andersen", "per-johansen"

    Returns:
        The system prompt for the agent

    Raises:
        ValueError: If agent_id is invalid
    """
    if agent_id not in AGENT_PROMPTS:
        raise ValueError(
            f"Invalid agent_id: {agent_id}. "
            f"Must be one of: {list(AGENT_PROMPTS.keys())}"
        )

    return AGENT_PROMPTS[agent_id]


def get_agent_name(agent_id: str) -> str:
    """Get the display name for an agent."""
    names = {
        "anne-lise-berg": "Anne-Lise Berg",
        "bjorn-eriksen": "Bjørn Eriksen",
        "kari-andersen": "Kari Andersen",
        "per-johansen": "Per Johansen",
    }
    return names.get(agent_id, "Unknown Agent")


def get_agent_type(agent_id: str) -> str:
    """Get the agent type (owner or supplier)."""
    if agent_id == "anne-lise-berg":
        return "owner"
    return "supplier"


# Export all functions
__all__ = [
    "AGENT_PROMPTS",
    "get_agent_prompt",
    "get_agent_name",
    "get_agent_type",
]


# Test the loader when run directly
if __name__ == "__main__":
    print("Testing agent prompts loader...")
    print(f"\nFound {len(AGENT_PROMPTS)} agents:")
    for agent_id in AGENT_PROMPTS.keys():
        prompt = get_agent_prompt(agent_id)
        name = get_agent_name(agent_id)
        agent_type = get_agent_type(agent_id)
        print(f"\n- {agent_id}: {name} ({agent_type})")
        print(f"  Prompt length: {len(prompt)} characters")
        print(f"  First 100 chars: {prompt[:100]}...")
