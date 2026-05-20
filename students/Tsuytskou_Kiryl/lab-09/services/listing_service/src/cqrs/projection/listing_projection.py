from src.cqrs.read_model.listing_view import ListingView


class ListingProjectionHandler:
    """Отвечает за обновление Read Model (проекции)"""

    def __init__(self, read_repository):
        self.read_repo = read_repository

    def on_listing_created(self, listing_aggregate):
        view = ListingView.from_listing(listing_aggregate)
        self.read_repo.save(view)

    def on_listing_approved(self, listing_aggregate):
        self.read_repo.update_status(listing_aggregate.id, "ACTIVE")

    def on_listing_rejected(self, listing_aggregate):
        self.read_repo.update_status(listing_aggregate.id, "REJECTED")

    def on_listing_sold(self, listing_aggregate):
        self.read_repo.update_status(listing_aggregate.id, "SOLD")

    def on_listing_archived(self, listing_aggregate):
        self.read_repo.update_status(listing_aggregate.id, "ARCHIVED")

    def on_category_updated(self, category_name, old_name, listing_ids):
        for listing_id in listing_ids:
            self.read_repo.update_category(listing_id, category_name)
