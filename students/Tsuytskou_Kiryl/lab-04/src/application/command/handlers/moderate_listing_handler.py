from src.application.command.moderate_listing_command import ModerateListingCommand

class ModerateListingHandler:
    def __init__(self, listing_repository):
        self.repository = listing_repository

    def handle(self, command: ModerateListingCommand) -> None:
        listing = self.repository.find_by_id(command.listing_id)
        if not listing:
            raise ValueError(f"Объявление с ID {command.listing_id} не найдено")

        if command.approved:
            listing.approve()
        else:
            listing.reject(command.rejection_reason or "Отклонено модератором")

        self.repository.save(listing)
