from pydantic import BaseModel
from datetime import datetime


class TestInfoR(BaseModel):
    test_id: int
    inicio_test: datetime
    fin_test: datetime

    class Config:
        orm_mode = True
