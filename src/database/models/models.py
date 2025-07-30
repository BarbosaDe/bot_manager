from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Optional


@dataclass
class Transaction:
    id: Optional[int] = None
    payment_id: Optional[int] = None
    payer_id: Optional[int] = None
    server_id: Optional[int] = None
    price: Optional[float] = None
    plan: Optional[int] = None
    created_at: Optional[str] = None
    status: Optional[str] = None


@dataclass
class Application:
    id: Optional[int] = None
    owner: Optional[int] = None
    application_id: Optional[int] = None


@dataclass
class Plan:
    id: Optional[int] = None
    name: Optional[int] = None
    price: Optional[float] = None
    max_ram: Optional[int] = None


@dataclass
class User:
    row_id: Optional[int] = None
    user_id: Optional[int] = None
    plan: Optional[Plan] = None
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    expired: Optional[bool] = None

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)

        if isinstance(self.expires_at, str):
            self.expires_at = datetime.fromisoformat(self.expires_at)

        if self.expires_at:
            self.expired = datetime.now(UTC) > self.expires_at
        else:
            self.expired = None
