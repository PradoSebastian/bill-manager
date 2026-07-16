import logging
from datetime import datetime

from pydantic import BaseModel

logger = logging.getLogger(__name__)

class Bill(BaseModel):
    description: str
    type: str
    destiny: str
    amount: float
    date: datetime
    month: str
    
    def equals_by_amount_and_date(self, other: 'Bill') -> bool:
        """Checks if two bills are equal based on amount and date."""
        return self.amount == other.amount and self.date == other.date