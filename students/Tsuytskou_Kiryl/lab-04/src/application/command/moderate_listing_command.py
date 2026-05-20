from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ModerateListingCommand:
    listing_id: str
    moderator_id: str
    approved: bool
    rejection_reason: Optional[str] = None
