from .timemachine import TimeMachine
from .stmarket import StockMarket

# TOOLS = [
#     [
#         {
#             "type": "function",
#             "function": {
#                 "name": "go_tomorrow",
#                 "description": "If you think you dont have something to do today , call this function wait for the next trade date",
#                 "parameters": {},
#             },
#         },
#     ]
# ]

tools = [
    {
        "type": "function",
        "function": {
            "name": "go_tomorrow",
            "description": "wait until tomorrow",
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

tc = TimeMachine()
sm = StockMarket()


def go_tomorrow():
    tc.go_tomorrow()
