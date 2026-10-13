
from typing import Literal
from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    title: str = Field(min_length=5, max_length=150)
    description: str = Field(min_length=10)
    severity: Literal["Low", "Medium", "High", "Critical"]
    product: str = Field(min_length=2)


class IncidentResponse(IncidentCreate):
    id: int
    status: Literal["Open", "Investigating", "Resolved"] = "Open"
