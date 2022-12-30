from marshmallow import Schema, fields, EXCLUDE


class RatesSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    date_from = fields.Date(format="%Y-%m-%d", required=True)
    date_to = fields.Date(format="%Y-%m-%d", required=True)
    origin = fields.String(required=True)
    destination = fields.String(required=True)
