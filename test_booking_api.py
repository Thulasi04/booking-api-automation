import pytest

@pytest.mark.smoke
def test_get_all_bookings_returns_list(booking_api):
    response = booking_api.get_all_bookings()
    assert response.status == 200
    assert isinstance(response.json(), list)

def test_booking_ids_contain_bookingid_field(booking_api):
    response = booking_api.get_all_bookings()
    assert response.status == 200
    bookings = response.json()
    if bookings:
        assert "bookingid" in bookings[0]

def test_create_booking_returns_id(booking_api, booking_data, auth_token):
    response = booking_api.create_booking(booking_data)
    assert response.status == 200
    body = response.json()
    assert "bookingid" in body
    assert body["booking"]["firstname"] == booking_data["firstname"]
    assert body["booking"]["lastname"] == booking_data["lastname"]

    # Clean up the booking created by this test.
    booking_api.delete_booking(body["bookingid"], auth_token)


def test_get_created_booking_matches_test_data(
    booking_api, created_booking, booking_data
):
    response = booking_api.get_booking(created_booking)
    assert response.status == 200
    body = response.json()
    assert body["firstname"] == booking_data["firstname"]
    assert body["lastname"] == booking_data["lastname"]
    assert body["totalprice"] == booking_data["totalprice"]
    assert body["depositpaid"] == booking_data["depositpaid"]


def test_booking_has_expected_fields(booking_api, created_booking):
    response = booking_api.get_booking(created_booking)
    assert response.status == 200
    body = response.json()
    expected_fields = [
        "firstname", "lastname", "totalprice", "depositpaid", "bookingdates"
    ]
    for field in expected_fields:
        assert field in body


def test_booking_dates_match_test_data(
    booking_api, created_booking, booking_data
):
    response = booking_api.get_booking(created_booking)
    assert response.status == 200
    dates = response.json()["bookingdates"]
    assert dates["checkin"] == booking_data["bookingdates"]["checkin"]
    assert dates["checkout"] == booking_data["bookingdates"]["checkout"]


def test_update_booking(
    booking_api, created_booking, booking_data, auth_token
):
    updated_data = dict(booking_data)
    updated_data["firstname"] = "UpdatedName"
    response = booking_api.update_booking(
        created_booking, updated_data, auth_token
    )
    assert response.status == 200
    assert response.json()["firstname"] == "UpdatedName"


def test_partial_update_booking(booking_api, created_booking, auth_token):
    response = booking_api.partially_update_booking(
        created_booking, {"firstname": "PartialUpdate"}, auth_token
    )
    assert response.status == 200
    assert response.json()["firstname"] == "PartialUpdate"


def test_delete_booking(booking_api, api_context, booking_data, auth_token):
    create_response = booking_api.create_booking(booking_data)
    assert create_response.status == 200
    booking_id = create_response.json()["bookingid"]
    delete_response = booking_api.delete_booking(booking_id, auth_token)
    assert delete_response.status in (200, 201, 204)
    get_response = booking_api.get_booking(booking_id)
    assert get_response.status == 404


@pytest.mark.negative
def test_get_nonexistent_booking_returns_404(booking_api):
    response = booking_api.get_booking(999999999)
    assert response.status == 404

@pytest.mark.negative
def test_update_without_authentication_is_rejected(
    api_context, created_booking, booking_data
):
    response = api_context.put(
        f"/booking/{created_booking}",
        data=booking_data
    )
    assert response.status in (401, 403)

@pytest.mark.negative
def test_delete_without_authentication_is_rejected(
    api_context, created_booking
):
    response = api_context.delete(f"/booking/{created_booking}")
    assert response.status in (401, 403)

@pytest.mark.parametrize(
    "query_params",
    [
        {"firstname": "Thulasi"},
        {"lastname": "Kumar"},
        {"firstname": "Thulasi", "lastname": "Kumar"},
    ],
)
def test_filter_bookings_returns_list(booking_api, query_params):
    response = booking_api.get_all_bookings(params=query_params)
    assert response.status == 200
    assert isinstance(response.json(), list)
