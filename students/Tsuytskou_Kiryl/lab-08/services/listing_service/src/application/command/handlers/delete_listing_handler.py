from src.application.command.delete_listing_command import DeleteListingCommand


class DeleteListingHandler:
    def __init__(self, listing_repository):
        self.repository = listing_repository

    def handle(self, command: DeleteListingCommand):
        listing = self.repository.find_by_id(command.listing_id)
        if not listing:
            raise ValueError("Объявление не найдено")
        self.repository.delete(command.listing_id)
        return command.listing_id
