"""Pydantic schemas: what the API accepts and returns.
Models = database shape. Schemas = API shape. Keep them separate."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ClaimCreate(BaseModel):
    policy_number: str = Field(examples=["POL-100234"])
    loss_date: datetime
    loss_type: str = Field(examples=["collision"])
    description: str
    amount: float = Field(gt=0)


class ClaimOut(BaseModel):
    id: UUID
    policy_number: str
    loss_date: datetime
    loss_type: str
    description: str
    amount: float
    status: str
    version: int

    class Config:
        from_attributes = True


class DecisionCreate(BaseModel):
    action: str = Field(pattern="^(approve|deny|request_info|refer)$")
    rationale: str = Field(min_length=10)  # mandatory rationale, enforced here
    recorded_by: str
