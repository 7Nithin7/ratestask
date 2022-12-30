from flask import Blueprint, request
from app.models.rates import RatesSchema
from app.services.rates_service import rates_service

rates_api = Blueprint("rates_api", __name__)


@rates_api.route("/rates", methods=["GET"])
def get_rates():
    errors = RatesSchema().validate(request.args)
    if errors:
        return errors, 400
    return rates_service.get_rates(**request.args)
