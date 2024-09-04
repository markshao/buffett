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


def test_agent_llm():
    agent = BuffetAgent()
    messages = [
        {"role": "system", "content": PromptBuilder.SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "today is weekend , what to do",
        },
    ]

    resp = agent._llm.invoke_with_tools(messages=messages, tools=str_tools)
    print(1)
