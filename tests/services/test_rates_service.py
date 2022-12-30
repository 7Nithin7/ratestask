import pytest
from app.services.rates_service import rates_service


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (
            {"date_from": "2016-01-01", "date_to": "2016-01-01", "origin": "DEBRV", "destination": "CNLYG"},
            [{"average_price": 1050, "day": "2016-01-01"}],
        ),
        (
            {"date_from": "2016-01-01", "date_to": "2016-01-02", "origin": "DEBRV", "destination": "china_east_main"},
            [{"average_price": 1040, "day": "2016-01-01"}, {"average_price": 1060, "day": "2016-01-02"}],
        ),
        (
            {"date_from": "2016-01-01", "date_to": "2016-01-02", "origin": "north_europe_main", "destination": "CNLYG"},
            [
                {"average_price": 1009.1666666666666, "day": "2016-01-01"},
                {"average_price": 1025, "day": "2016-01-02"},
            ],
        ),
        (
            {
                "date_from": "2016-01-01",
                "date_to": "2016-01-01",
                "origin": "northern_europe",
                "destination": "china_east_main",
            },
            [{"average_price": 1016.1111111111111, "day": "2016-01-01"}],
        ),
        (
            {"date_from": "2016-01-02", "date_to": "2016-01-02", "origin": "GBSOU", "destination": "CNLYG"},
            [{"average_price": None, "day": "2016-01-02"}],
        ),
    ],
)
def test_get_rates(setup_test_data, input, expected_output):
    # When
    result = rates_service.get_rates(**input)

    # Then
    assert result == expected_output
