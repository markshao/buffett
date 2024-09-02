import pytest
from src.agent.agent import BUFFET_SYSTEM_PROMPT, BuffetAgent
from src.agent.tools import WaitNextTradeDay, GetStockPriceOfToday, ListTheStocksToWatch

str_tools = [
    {
        "type": "function",
        "function": {
            "name": "WaitNextTradeDay",
            "description": "wait for the next trade day",
            "parameters": {
                "type": "object",
                "properties": {
                    # "location": {
                    #     "type": "string",
                    #     "description": "The city and state, e.g. San Francisco, CA",
                    # }
                },
                "required": [],
            },
        },
    },
]


def test_agent_llm():
    agent = BuffetAgent()
    messages = [
        {"role": "system", "content": BUFFET_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "today is weekend , what to do",
        },
    ]

    # tools = [WaitNextTradeDay, GetStockPriceOfToday, ListTheStocksToWatch]
    resp = agent._llm.invoke_with_tools(messages=messages, tools=str_tools)
    print(1)
