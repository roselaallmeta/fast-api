from dataclasses import Field
from decimal import Decimal
import decimal
from enum import Enum
from typing import Optional
from fastapi import FastAPI, File
from pydantic import BaseModel
from datetime import datetime


class StatusEnum(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


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
    JPY = "JPY"
    ALL = "ALL"
    GBP = "GBP"
    CHF = "CHF"
    CAD = "CAD"
    AUD = "AUD"
    CNY = "CNY"
    SEK = "SEK"
    NZD = "NZD"
    KRW = "KRW"
    SGD = "SGD"
    NOK = "NOK"
    INR = "INR"


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


class Venture(BaseModel):
    name: str
    created_at: datetime
    phone_number: str
    email: str
    description: str
    industries: IndustryEnum
    created_at: datetime
    funding_stage: FundingStageEnum
    description: str
    founders_name: str
    email: str
    website_url: str
    funding_goal: decimal.Decimal
    total_funding: decimal.Decimal
    valuation: decimal.Decimal
    is_active: bool


class User(BaseModel):
    name: str
    role: UserRoleEnum
    email: str
    gender: GenderEnum


class UserProfile(BaseModel):
    email: str
    phone_number: str
    created_at: datetime
    updated_at: datetime
    last_login: datetime
    is_active: bool


class Investment(BaseModel):
    user_id: int
    venture_id: int
    title: str
    amount: decimal.Decimal
    investment_type: InvestmentTypeEnum
    equity_percent: decimal.Decimal
    currency: CurrencyEnum
    invested_on: datetime
    description: str


class PitchDecks(BaseModel):  # inseroje ne db
    title: str
    file_url: str
    description: str
    created_at: datetime
    updated_at: datetime


class Team(BaseModel):  # inseroje ne db
    number_of_members: int
    names: str
    roles: str
    startup_before: bool


class Document(BaseModel):
    title: str
    size: int
    issue_date: datetime
    expiry_date: datetime
    content_type: str
    uploaded_by: str
    uploaded_at: datetime
    description: str
    status: StatusEnum


class BankingDetails(BaseModel):
    user_id: int
    account_number: str
    bic: str
    iban: str
    bank_name: str
    bank_country: str
    currency: CurrencyEnum
    balance: decimal.Decimal
    is_bank_verified: bool
