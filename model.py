from dataclasses import Field
from decimal import Decimal
import decimal
from enum import Enum
from typing import Optional
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, FilePath, HttpUrl, field_validator
from datetime import datetime


class StatusEnum(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ProfileStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    deactivated = "deactivated"


class VentureStatusEnum(str, Enum):
    active = "active"
    archived = "archived"
    banned = "banned"


class InvestmentTypeEnum(str, Enum):
    equity = "equity"
    loan = "loan"
    grant = "grant"


class IndustryEnum(str, Enum):
    technology = "technology"
    finance = "finance"
    healthcare = "healthcare"
    education = "education"
    energy = "energy"
    real_estate = "real_estate"
    transportation = "transportation"
    retail = "retail"
    other = "other"
    media = "media"


class FundingStageEnum(str, Enum):
    pre_seed = "pre_seed"
    seed = "seed"
    series_a = "series_a"
    series_b = "series_b"
    series_c = "series_c"
    series_d_plus = "series_d_plus"
    venture_round = "venture_round"
    private_equity = "private_equity"
    debt_financing = "debt_financing"
    grant = "grant"
    ipo = "ipo"
    acquired = "acquired"


class CurrencyEnum(str, Enum):
    USD = "USD"
    EUR = "EUR"
    ALL = "ALL"


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class UserRoleEnum(str, Enum):
    founder = "founder"
    investor = "investor"
    guest = "guest"
    institution = "institution"
    admin = "admin"
    business = "business"


class User(BaseModel):
    id: Optional[int] = None
    name: str
    role: UserRoleEnum
    email: str
    password: str
    created_at: Optional[datetime] = None


class UserProfile(BaseModel):
    id: Optional[int] = None
    user_id: int
    phone_number: str
    created_at: Optional[datetime] = None
    gender: GenderEnum
    updated_at: Optional[datetime] = None
    status: ProfileStatusEnum
    industry: IndustryEnum
    description: str


class UserLogin(BaseModel):
    id: Optional[int] = None
    email: str
    password: str


class Venture(BaseModel):
    name: str
    created_at: Optional[datetime] = None
    phone_number: str
    email: str
    description: str
    industries: IndustryEnum
    funding_stage: FundingStageEnum
    website_url: str
    funding_goal: decimal.Decimal
    total_funding: decimal.Decimal
    valuation: decimal.Decimal
    status: VentureStatusEnum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class VentureTeam(BaseModel):
    venture_id: int
    team_id: int
    created_at: Optional[datetime] = None


class VentureMembers(BaseModel):
    member_id: int
    venture_id: int
    name: str


class Investment(BaseModel):
    user_id: int
    venture_id: int
    name: str
    amount: decimal.Decimal
    investment_type: InvestmentTypeEnum
    equity_percent: decimal.Decimal
    currency: CurrencyEnum
    invested_on: Optional[datetime] = None
    description: str


class PitchDecks(BaseModel):  # inseroje ne db
    venture_id: int
    title: str
    file_url: str
    description: str
    created_at: datetime
    updated_at: datetime


class Team(BaseModel):
    name: str
    created_at: Optional[datetime] = None


class TeamMembers(BaseModel):
    team_id: int
    member_id: int
    created_at: Optional[datetime] = None


class Document(BaseModel):
    user_id: int
    title: str
    add_document: str
    issue_date: datetime
    expiry_date: datetime
    content_type: str
    uploaded_by: str
    description: str
    uploaded_at: datetime
    status: StatusEnum


class BankingDetails(BaseModel):
    user_id: int
    account_number: str
    iban: str
    bic: str
    bank_name: str
    bank_country: str
    currency: CurrencyEnum
    balance: decimal.Decimal
    is_bank_verified: bool


class UpdateVenture(Venture):
    pass
