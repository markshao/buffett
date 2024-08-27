import pytest
from src.agent.agent import BUFFET_SYSTEM_PROMPT, BuffetAgent


def test_agent_llm():
    agent = BuffetAgent()
    messages = [
        {"role": "system", "content": BUFFET_SYSTEM_PROMPT},
        {"role": "user", "content": "what to do next"},
    ]
    resp = agent._llm.request_llm(messages=messages)
    print(1)
