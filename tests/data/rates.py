import json


class RatesRequestBuilder:
    request = """{
        "date_from": "2016-01-01",
        "date_to": "2016-01-01",
        "origin": "",
        "destination": ""
    }"""

    def __init__(self):
        self.rates_request = json.loads(self.request)

    @staticmethod
    def a_rates_request():
        return RatesRequestBuilder()

    def with_date_from(self, date_from):
        self.rates_request["date_from"] = date_from
        return self

    def with_date_to(self, date_to):
        self.rates_request["date_to"] = date_to
        return self

    def with_origin(self, origin):
        self.rates_request["origin"] = origin
        return self

    def with_destination(self, destination):
        self.rates_request["destination"] = destination
        return self

    def build(self):
        return self.rates_request


class RatesRequestInvalidData:
    DATE_FROM_INVALID = RatesRequestBuilder.a_rates_request().with_date_from("10-10-2016").build()
    DATE_TO_INVALID = RatesRequestBuilder.a_rates_request().with_date_to("10-10-2016").build()
    DATE_FROM_MISSING = RatesRequestBuilder.a_rates_request().with_date_from(None).build()
    DATE_TO_MISSING = RatesRequestBuilder.a_rates_request().with_date_to(None).build()
    ORIGIN_MISSING = RatesRequestBuilder.a_rates_request().with_origin(None).build()
    DESTINATION_MISSING = RatesRequestBuilder.a_rates_request().with_destination(None).build()
