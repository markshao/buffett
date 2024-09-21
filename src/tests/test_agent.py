import pytest
from dotenv import load_dotenv
import os

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(env_path)

from agent.context.prompt import PromptBuilder
from agent.agent import BuffetAgent

str_tools = [
    {
        "type": "function",
        "function": {
            "name": "WaitNextTradeDay",
            "description": "wait for the next trade day",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]

@pytest.mark.skip(reason="need apikey")
def test_agent_llm(cfg):
    agent = BuffetAgent(cfg)
    messages = [
        {"role": "system", "content": PromptBuilder.SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "today is weekend , what to do",
        },
    ]

    resp = agent.llm.invoke_with_tools(messages=messages, tools=str_tools)
    print(1)
