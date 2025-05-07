from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from src.custom_exception import BadRequestException
from src.http_status import HTTPStatusCodes
from src.model.models import Lead
from src.schema.lead_schema import LeadSchema, GetLeadSchema

app = Blueprint('angi', __name__)


@app.route('/angi-webhook', methods=['POST'])
def angi_webhook():
    try:
        payload = request.get_json()
        validated_data = LeadSchema(**payload).dict()
        lead = Lead.create_lead(validated_data)
        return jsonify({
            "data": {
                "id": lead.id
            },
            "message": "Lead received successfully",
            "status": "SUCCESS",
            "status_code": HTTPStatusCodes.CREATED
        }), 200
    except ValidationError as e:
        raise BadRequestException.from_validation_error(e)


@app.route('/leads', methods=['GET'])
def get_leads():
    try:
        response = Lead.get_all_leads()
        return jsonify({
            "data": {
                "leads": response
            },
            "message": "Lead fetched successfully",
            "status": "SUCCESS",
            "status_code": HTTPStatusCodes.OK
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead_by_id(lead_id):
    try:
        if not lead_id:
            raise BadRequestException("Lead ID is required")
        response = Lead.get_lead_by_id(lead_id)
        if response:
            return jsonify({
                "data": {
                    "lead": response
                },
                "message": "Lead fetched successfully",
                "status": "SUCCESS",
                "status_code": HTTPStatusCodes.OK
            }), 200
        else:
            return jsonify({
                "data": {},
                "message": "Lead not found",
                "status": "FAILED",
                "status_code": HTTPStatusCodes.NOT_FOUND
            }), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_lead/<int:lead_id>", methods=['PUT'])
def update_lead(lead_id):
    try:
        payload = request.get_json()
        validated_data = GetLeadSchema(**payload).dict()
        lead = Lead.update_lead(lead_id, validated_data)
        if lead:
            return jsonify({
                "data": "Lead updated successfully!",
                "message": "Lead updated successfully",
                "status": "SUCCESS",
                "status_code": HTTPStatusCodes.OK
            }), 200
        else:
            return jsonify({
                "data": {},
                "message": "Lead not found",
                "status": "FAILED",
                "status_code": HTTPStatusCodes.NOT_FOUND
            }), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete_lead/<int:lead_id>", methods=['DELETE'])
def delete_lead(lead_id):
    try:
        lead = Lead.delete_lead(lead_id)
        if lead:
            return jsonify({
                "data": "Lead deleted successfully!",
                "message": "Lead deleted successfully",
                "status": "SUCCESS",
                "status_code": HTTPStatusCodes.OK
            }), 200
        else:
            return jsonify({
                "data": {},
                "message": "Lead not found",
                "status": "FAILED",
                "status_code": HTTPStatusCodes.NOT_FOUND
            }), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
