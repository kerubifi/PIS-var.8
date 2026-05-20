from fastapi import FastAPI, HTTPException
from src.infrastructure.config.dependency_injection import container
from src.application.command.create_listing_command import CreateListingCommand
from src.application.command.moderate_listing_command import ModerateListingCommand
from src.application.query.get_listing_query import GetListingQuery
from src.application.query.get_active_listings_query import GetActiveListingsQuery

app = FastAPI(title="Listing Service", version="1.0")


@app.post("/api/listings")
def create_listing(seller_id: str, title: str, description: str, price_amount: float, category_name: str):
    command = CreateListingCommand(
        seller_id=seller_id,
        title=title,
        description=description,
        price_amount=price_amount,
        category_name=category_name
    )
    result = container.listing_service.create_listing(command)
    return {"listing_id": result.listing_id, "status": result.status}


@app.get("/api/listings/{listing_id}")
def get_listing(listing_id: str):
    query = GetListingQuery(listing_id=listing_id)
    try:
        result = container.listing_service.get_listing(query)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/listings/{listing_id}/approve")
def approve_listing(listing_id: str, moderator_id: str):
    command = ModerateListingCommand(
        listing_id=listing_id,
        moderator_id=moderator_id,
        approved=True
    )
    container.listing_service.moderate_listing(command)
    return {"status": "approved"}


@app.post("/api/listings/{listing_id}/reject")
def reject_listing(listing_id: str, moderator_id: str, rejection_reason: str = None):
    command = ModerateListingCommand(
        listing_id=listing_id,
        moderator_id=moderator_id,
        approved=False,
        rejection_reason=rejection_reason
    )
    container.listing_service.moderate_listing(command)
    return {"status": "rejected"}


@app.get("/api/listings")
def get_active_listings(limit: int = 10, offset: int = 0):
    query = GetActiveListingsQuery(limit=limit, offset=offset)
    return container.listing_service.get_active_listings(query)
