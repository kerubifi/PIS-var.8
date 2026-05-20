from src.application.port.in_.moderate_listing_use_case import ModerateListingUseCase


class ListingController:
    """Incoming adapter (REST imitation)"""

    def __init__(self, moderate_use_case: ModerateListingUseCase):
        self.moderate_use_case = moderate_use_case

    def handle_moderate(self, listing_id: str, moderator_id: str, approved: bool, rejection_reason: str = None):
        return self.moderate_use_case.moderate_listing(listing_id, moderator_id, approved, rejection_reason)
