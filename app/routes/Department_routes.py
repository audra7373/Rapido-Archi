from flask import Blueprint, request, jsonify
from app.services.departments_service import DepartmentService

department_bp = Blueprint("departments", __name__, url_prefix="/departments")


@department_bp.route("/", methods=["GET"])
def list_departments():
    departments = DepartmentService.get_all()
    return jsonify(departments)


@department_bp.route("/", methods=["POST"])
def create_department():
    data = request.json
    department = DepartmentService.create(
        name=data["name"],
        target_path=data["target_path"]
    )
    return jsonify(department), 201


@department_bp.route("/<int:dept_id>", methods=["DELETE"])
def delete_department(dept_id):
    success = DepartmentService.delete(dept_id)
    if not success:
        return jsonify({"error": "Department not found"}), 404
    return jsonify({"message": "Deleted"})