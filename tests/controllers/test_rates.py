import pytest
from tests.data.rates import RatesRequestBuilder, RatesRequestInvalidData
from unittest.mock import MagicMock, patch
from app.services.rates_service import RatesService


@patch.object(RatesService, "get_rates", MagicMock(return_value=[{"average_price": 1000, "day": "2016-01-01"}]))
def test_get_rates(flask_client):
    # Given
    data = RatesRequestBuilder.a_rates_request().build()

    # When
    response = flask_client.get("/rates", query_string=data)

    # Then
    assert response.status_code == 200
    assert response.json == [{"average_price": 1000, "day": "2016-01-01"}]


@pytest.mark.parametrize(
    "data, output",
    [
        (RatesRequestInvalidData.DATE_FROM_INVALID, {"date_from": ["Not a valid date."]}),
        (RatesRequestInvalidData.DATE_TO_INVALID, {"date_to": ["Not a valid date."]}),
        (RatesRequestInvalidData.DATE_FROM_MISSING, {"date_from": ["Missing data for required field."]}),
        (RatesRequestInvalidData.DATE_TO_MISSING, {"date_to": ["Missing data for required field."]}),
        (RatesRequestInvalidData.ORIGIN_MISSING, {"origin": ["Missing data for required field."]}),
        (RatesRequestInvalidData.DESTINATION_MISSING, {"destination": ["Missing data for required field."]}),
    ],
)
def test_get_rates_validation(flask_client, data, output):
    # When
    response = flask_client.get("/rates", query_string=data)

    # Then
    assert response.status_code == 400
    assert response.json == output
