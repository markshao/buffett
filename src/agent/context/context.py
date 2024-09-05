from enum import Enum
from typing import List

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


class TransType(Enum):
    THINK = "think"
    FUNCTION_CALL = "function call"


class Transaction(BaseModel):
    type: TransType
    log: str


class TransactionCtx(BaseModel):
    transactions: List[Transaction] = Field(default=[])

    def clear(self):
        self.transactions.clear()


class StockAccountCtx(BaseModel):
    interested_stock_list: List[str] = Field(default=[])
    total_available_money: float = Field(default=100000.0)
    stock_holding: dict = Field(default={})


class AgentContext(BaseModel):
    transCtx: TransactionCtx = Field(
        default=TransactionCtx(), alias="transaction history of today"
    )
    stockActCtx: StockAccountCtx = Field(
        default=StockAccountCtx(),
        alias="personal account status and interested stock list",
    )

    llm_logs: List[BaseMessage] = Field(default=[], exclude=True)
