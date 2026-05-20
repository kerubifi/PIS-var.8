from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteListingCommand:
    listing_id: str
