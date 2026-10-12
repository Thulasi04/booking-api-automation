import json
from pathlib import Path

import pytest
from playwright.sync_api import Playwright

from clients.booking_client import BookingClient

BASE_URL = "https://restful-booker.herokuapp.com"
DATA_FILE = Path(__file__).parent / "test_data" / "booking.json"


@pytest.fixture(scope="session")
def api_context(playwright: Playwright):
    """Create one API request context for the test session."""
    context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={"Accept": "application/json"}
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def auth_token(api_context):
    """Create a RESTful Booker token for protected requests."""
    response = api_context.post(
        "/auth",
        data={"username": "admin", "password": "password123"}
    )
    assert response.status == 200, (
        f"Authentication failed: {response.status} {response.text()}"
    )

    body = response.json()
    token = body.get("token")
    assert token, f"No token returned: {body}"
    return token


@pytest.fixture
def booking_api(api_context):
    return BookingClient(api_context)


@pytest.fixture
def booking_data():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def created_booking(booking_api, booking_data, auth_token):
    """Create a booking and remove it after the test."""
    response = booking_api.create_booking(booking_data)
    assert response.status == 200, (
        f"Booking creation failed: {response.status} {response.text()}"
    )
    booking_id = response.json()["bookingid"]

    yield booking_id

    # Cleanup: the public demo API may occasionally be unavailable.
    try:
        booking_api.delete_booking(booking_id, auth_token)
    except Exception:
        pass
