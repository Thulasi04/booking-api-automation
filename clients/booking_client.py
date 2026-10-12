class BookingClient:
    """Reusable API methods for RESTful Booker."""

    def __init__(self, api_context):
        self.api = api_context

    def get_all_bookings(self, params=None):
        return self.api.get("/booking", params=params)

    def get_booking(self, booking_id):
        return self.api.get(f"/booking/{booking_id}")

    def create_booking(self, booking_data):
        return self.api.post("/booking", data=booking_data)

    def update_booking(self, booking_id, booking_data, token):
        return self.api.put(
            f"/booking/{booking_id}",
            data=booking_data,
            headers={"Cookie": f"token={token}"}
        )

    def partially_update_booking(self, booking_id, booking_data, token):
        return self.api.patch(
            f"/booking/{booking_id}",
            data=booking_data,
            headers={"Cookie": f"token={token}"}
        )

    def delete_booking(self, booking_id, token):
        return self.api.delete(
            f"/booking/{booking_id}",
            headers={"Cookie": f"token={token}"}
        )
