from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import date
from enum import Enum


class ProposalType(str, Enum):
    fresh = "Fresh"
    renewal = "Renewal"
    expanded = "Expanded"


class ClosedStatus(str, Enum):
    yes = "Yes"
    no = "No"


class RequirementType(str, Enum):
    sfp = "Standard Fire & Peril Policy"
    marine = "Marine Policy"
    ear = "Erection All Risk Policy"
    car = "Contractors All Risk Policy"
    iar = "Industrial All Risk Policy"
    do_policy = "D&O Policy"
    others = "Any Others"


class EnquiryCreate(BaseModel):
    date_referred: date
    contact_person: str = Field(..., min_length=1, max_length=200)
    company_name: str = Field(..., min_length=1, max_length=300)
    phone: str = Field(..., pattern=r"^\d{10}$")
    email: Optional[EmailStr] = None
    requirement: RequirementType
    premium_potential: Optional[float] = Field(None, ge=0)
    type_of_proposal: Optional[ProposalType] = None
    expiry_date_existing_policy: Optional[date] = None
    cre_rm_accountable: str = Field(..., min_length=1, max_length=200)
    quote_planned_date: Optional[date] = None
    quote_actual_date: Optional[date] = None
    quote_submitted: ClosedStatus = ClosedStatus.no
    closure_planned_date: Optional[date] = None
    closure_actual_date: Optional[date] = None
    business_closed: ClosedStatus = ClosedStatus.no
    reason_not_closed: Optional[str] = Field(None, max_length=500)
    fy: str = "2025-26"
    branch: str = "Ahmedabad"

    model_config = {"use_enum_values": True}

    @model_validator(mode="after")
    def compute_brokerage(self):
        # tentative_brokerage is derived, not stored from user input
        return self

    @property
    def tentative_brokerage_12pct(self) -> float:
        if self.premium_potential:
            return round(self.premium_potential * 0.12, 2)
        return 0.0


class EnquiryUpdate(BaseModel):
    date_referred: Optional[date] = None
    contact_person: Optional[str] = Field(None, min_length=1, max_length=200)
    company_name: Optional[str] = Field(None, min_length=1, max_length=300)
    phone: Optional[str] = Field(None, pattern=r"^\d{10}$")
    email: Optional[EmailStr] = None
    requirement: Optional[RequirementType] = None
    premium_potential: Optional[float] = Field(None, ge=0)
    type_of_proposal: Optional[ProposalType] = None
    expiry_date_existing_policy: Optional[date] = None
    cre_rm_accountable: Optional[str] = Field(None, min_length=1, max_length=200)
    quote_planned_date: Optional[date] = None
    quote_actual_date: Optional[date] = None
    quote_submitted: Optional[ClosedStatus] = None
    closure_planned_date: Optional[date] = None
    closure_actual_date: Optional[date] = None
    business_closed: Optional[ClosedStatus] = None
    reason_not_closed: Optional[str] = Field(None, max_length=500)

    model_config = {"use_enum_values": True}


class EnquiryOut(BaseModel):
    id: str = Field(alias="_id")
    enquiry_no: int
    date_referred: Optional[date] = None
    contact_person: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    requirement: Optional[str] = None
    premium_potential: Optional[float] = None
    tentative_brokerage_12pct: Optional[float] = None
    type_of_proposal: Optional[str] = None
    expiry_date_existing_policy: Optional[date] = None
    cre_rm_accountable: Optional[str] = None
    quote_planned_date: Optional[date] = None
    quote_actual_date: Optional[date] = None
    quote_submitted: Optional[str] = None
    closure_planned_date: Optional[date] = None
    closure_actual_date: Optional[date] = None
    business_closed: Optional[str] = None
    reason_not_closed: Optional[str] = None
    fy: Optional[str] = None
    branch: Optional[str] = None

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}
