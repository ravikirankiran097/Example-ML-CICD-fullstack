from flask_restful import fields


class EnvelopeData(fields.Raw):
    def format(self, value: dict):
        return {"data": value}
