from flask import Blueprint, request, jsonify
from app.services.rule_service import RuleService

rule_bp = Blueprint("rules", __name__, url_prefix="/rules")

@rule_bp.route("/", methods=["POST"])
def create_rule():
    data = request.json
    try:
        rule = RuleService.create(
            extension=data.get("extension"),
            keyword=data.get("keyword"),
            department_id=data["department_id"]
        )
        # SQLModel objects cannot be directly jsonify'ed sometimes, convert to dict
        return jsonify({
            "id": rule.id,
            "extension": rule.extension,
            "keyword": rule.keyword,
            "department_id": rule.department_id
        }), 201
    except ValueError as e:
         return jsonify({"error": str(e)}), 400
