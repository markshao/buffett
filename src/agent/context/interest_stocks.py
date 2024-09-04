from typing import List
from pydantic import BaseModel, Field


class InterestedStockList(BaseModel):
    interested_stock_list: List[str] = Field(default=[], alias="interested stock list")

    def get_json(self):
        return self.model_dump_json(by_alias=True)
