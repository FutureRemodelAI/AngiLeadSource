from flask import jsonify
from pydantic import ValidationError
from src.http_status import HTTPStatusCodes


class BadRequestException(Exception):
    def __init__(self, message="Bad request"):
        self.message = message
        super().__init__(self.message)

    @classmethod
    def from_validation_error(cls, e: ValidationError):
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return cls("; ".join(errors))

    def to_response(self):
        return jsonify({
            "data": {},
            "message": self.message,
            "status": "FAILED",
            "status_code": HTTPStatusCodes.BAD_REQUEST
        }), HTTPStatusCodes.BAD_REQUEST


class NotFoundException(Exception):
    def __init__(self, message="Not found"):
        self.message = message
        super().__init__(self.message)

    def to_response(self):
        return jsonify({
            "data": {},
            "message": self.message,
            "status": "FAILED",
            "status_code": HTTPStatusCodes.NOT_FOUND
        }), HTTPStatusCodes.NOT_FOUND


class ForbiddenException(Exception):
    def __init__(self, message="Unauthorized"):
        self.message = message
        super().__init__(self.message)

    def to_response(self):
        return jsonify({
            "data": {},
            "message": self.message,
            "status": "FAILED",
            "status_code": HTTPStatusCodes.FORBIDDEN
        }), HTTPStatusCodes.FORBIDDEN


class TokenExpireException(Exception):
    def __init__(self, message="Token Expired"):
        self.message = message
        super().__init__(self.message)

    def to_response(self):
        return jsonify({
            "data": {},
            "message": self.message,
            "status": "FAILED",
            "status_code": HTTPStatusCodes.UNAUTHORIZED
        }), HTTPStatusCodes.UNAUTHORIZED


class ConflictException(Exception):
    def __init__(self, message="Resource already exists"):
        self.message = message
        super().__init__(self.message)

    def to_response(self):
        return jsonify({
            "data": {},
            "message": self.message,
            "status": "FAILED",
            "status_code": HTTPStatusCodes.CONFLICT
        }), HTTPStatusCodes.CONFLICT
