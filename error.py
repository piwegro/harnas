from dataclasses import dataclass
from flask import make_response, jsonify, Response


@dataclass
class Error:
    message: str

    @classmethod
    def from_exception(cls, e: Exception) -> "Error":
        return cls(str(e))

    def __str__(self):
        return self.message

    def to_json(self, status_code: int) -> Response:
        response_object = {
            'error': self.message
        }

        json_response = jsonify(response_object)
        response = make_response(json_response, status_code)
        response.headers['Content-Type'] = 'application/json'

        return response
