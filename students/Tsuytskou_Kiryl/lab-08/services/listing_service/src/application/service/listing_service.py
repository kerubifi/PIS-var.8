class ListingService:
    def __init__(self, create_handler, delete_handler, get_handler):
        self.create_handler = create_handler
        self.delete_handler = delete_handler
        self.get_handler = get_handler

    def create_listing(self, command):
        return self.create_handler.handle(command)

    def delete_listing(self, command):
        return self.delete_handler.handle(command)

    def get_listing(self, query):
        return self.get_handler.handle(query)
