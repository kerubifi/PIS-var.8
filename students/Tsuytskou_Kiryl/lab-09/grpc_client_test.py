import sys
sys.path.append('./services/listing_service')
import grpc
import listing_pb2
import listing_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = listing_pb2_grpc.ListingServiceStub(channel)

        print("=== Test 1: Creating a valid listing ===")
        try:
            response = stub.CreateListing(listing_pb2.CreateListingRequest(
                seller_id="seller-1",
                title="Adult Bicycle",
                description="Good condition, 2023 model",
                price_amount=150.00,
                price_currency="USD",
                category_name="Sports"
            ))
            print(f"? Created listing: ID={response.listing.id}, Status={response.listing.status}")
            listing_id = response.listing.id
        except grpc.RpcError as e:
            print(f"? Error: {e.details()}")
            return

        print("\n=== Test 2: Getting listing by ID ===")
        try:
            response = stub.GetListing(listing_pb2.GetListingRequest(id=listing_id))
            print(f"? Retrieved: {response.listing.title} - {response.listing.status}")
        except grpc.RpcError as e:
            print(f"? Error: {e.details()}")

        print("\n=== Test 3: Approving listing ===")
        try:
            response = stub.ApproveListing(listing_pb2.ApproveListingRequest(
                listing_id=listing_id,
                moderator_id="mod-1"
            ))
            print(f"? Approved: {response.success}")
        except grpc.RpcError as e:
            print(f"? Error: {e.details()}")

        print("\n=== Test 4: Checking status after approval ===")
        try:
            response = stub.GetListing(listing_pb2.GetListingRequest(id=listing_id))
            print(f"? Status: {response.listing.status}")
        except grpc.RpcError as e:
            print(f"? Error: {e.details()}")

        print("\n=== Test 5: Creating listing with short title (error) ===")
        try:
            stub.CreateListing(listing_pb2.CreateListingRequest(
                seller_id="seller-1",
                title="Hi",  # less than 5 characters
                description="Test",
                price_amount=100.0,
                price_currency="USD",
                category_name="Test"
            ))
        except grpc.RpcError as e:
            print(f"? Error (expected): {e.details()}")

        print("\n=== Test 6: Streaming new listings ===")
        print("Receiving stream of listings:")
        try:
            for listing in stub.StreamNewListings(listing_pb2.Empty()):
                print(f"  ?? New listing: {listing.title} - {listing.price_amount} USD")
        except grpc.RpcError as e:
            print(f"? Error: {e.details()}")

if __name__ == '__main__':
    run()
