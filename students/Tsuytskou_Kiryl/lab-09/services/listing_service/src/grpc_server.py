
import grpc
from concurrent import futures
import time
import uuid
from datetime import datetime
import sys
sys.path.append('..')
import listing_pb2
import listing_pb2_grpc

class ListingServiceServicer(listing_pb2_grpc.ListingServiceServicer):
    def __init__(self, listing_repository):
        self.repository = listing_repository

    def CreateListing(self, request, context):
        # Validation
        if len(request.title) < 5:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'Title must be at least 5 characters')
        if len(request.description) > 5000:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'Description too long (max 5000 chars)')
        if request.price_amount < 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'Price cannot be negative')

        listing_id = str(uuid.uuid4())[:8]

        listing = listing_pb2.Listing(
            id=listing_id,
            seller_id=request.seller_id,
            title=request.title,
            description=request.description,
            price_amount=request.price_amount,
            price_currency=request.price_currency,
            category_name=request.category_name,
            status='PENDING_MODERATION',
            created_at=datetime.now().isoformat()
        )

        self.repository.save(listing)

        return listing_pb2.CreateListingResponse(listing=listing)

    def GetListing(self, request, context):
        listing = self.repository.find_by_id(request.id)
        if not listing:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Listing not found')
        return listing_pb2.GetListingResponse(listing=listing)

    def ApproveListing(self, request, context):
        listing = self.repository.find_by_id(request.listing_id)
        if not listing:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Listing not found')

        if listing.status != 'PENDING_MODERATION':
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, 'Only pending listings can be approved')

        listing.status = 'ACTIVE'
        self.repository.save(listing)

        return listing_pb2.ApproveListingResponse(success=True)

    def RejectListing(self, request, context):
        listing = self.repository.find_by_id(request.listing_id)
        if not listing:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Listing not found')

        if listing.status != 'PENDING_MODERATION':
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, 'Only pending listings can be rejected')

        listing.status = 'REJECTED'
        self.repository.save(listing)

        return listing_pb2.RejectListingResponse(success=True)

    def ListListings(self, request, context):
        listings = self.repository.find_all()

        if request.status:
            listings = [l for l in listings if l.status == request.status]
        if request.category:
            listings = [l for l in listings if l.category_name == request.category]

        start = request.offset
        end = start + request.limit
        paginated = listings[start:end]

        return listing_pb2.ListListingsResponse(
            listings=paginated,
            total_count=len(listings)
        )

    def StreamNewListings(self, request, context):
        '''Server-side streaming of new listings'''
        for i in range(10):
            if context.is_active():
                time.sleep(2)
                yield listing_pb2.Listing(
                    id=f'stream-{i}',
                    seller_id='stream_seller',
                    title=f'New Listing {i}',
                    description='This is a streamed listing',
                    price_amount=float(i * 10),
                    price_currency='USD',
                    category_name='General',
                    status='PENDING_MODERATION',
                    created_at=datetime.now().isoformat()
                )
            else:
                break

def serve():
    # Simple in-memory repository for demonstration
    class InMemoryRepository:
        def __init__(self):
            self._listings = {}
        def save(self, listing):
            self._listings[listing.id] = listing
        def find_by_id(self, listing_id):
            return self._listings.get(listing_id)
        def find_all(self):
            return list(self._listings.values())

    repository = InMemoryRepository()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    listing_pb2_grpc.add_ListingServiceServicer_to_server(
        ListingServiceServicer(repository), server
    )
    server.add_insecure_port('0.0.0.0:50051')
    print(' [gRPC] Listing Service started on port 50051...')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

