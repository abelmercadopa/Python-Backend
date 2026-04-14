from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__)


VALID_STATUSES = {"pending", "completed"}
VALID_PRIORITIES = {"low", "medium", "high"}


def parse_due_date(date_str: str | None):
    if not date_str:
        return None
    try:
        parsed_date = datetime.fromisoformat(date_str)
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
        return parsed_date
    except ValueError:
        return None


def validate_priority(priority: str) -> bool:
    return priority in VALID_PRIORITIES


def validate_status(status: str) -> bool:
    return status in VALID_STATUSES


@tasks_bp.get("")
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())
    status = request.args.get("status")
    priority = request.args.get("priority")

    query = Task.query.filter_by(user_id=user_id)

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)

    tasks = query.order_by(Task.id.desc()).all()
    return jsonify([task.to_dict() for task in tasks]), 200


@tasks_bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id: int):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    return jsonify(task.to_dict()), 200


@tasks_bp.post("")
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se enviaron datos JSON"}), 400

    title = data.get("title")
    description = data.get("description")
    priority = data.get("priority", "medium")
    due_date_str = data.get("due_date")
    due_date = parse_due_date(due_date_str)

    if not title:
        return jsonify({"error": "El título es obligatorio"}), 400

    if not validate_priority(priority):
        return jsonify({"error": "priority debe ser low, medium o high"}), 400

    if due_date_str and due_date is None:
        return jsonify({"error": "Formato de due_date inválido. Use ISO 8601"}), 400

    task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        user_id=user_id,
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Tarea creada correctamente", "task": task.to_dict()}), 201


@tasks_bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id: int):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos JSON"}), 400

    if "priority" in data and not validate_priority(data["priority"]):
        return jsonify({"error": "priority debe ser low, medium o high"}), 400

    if "status" in data and not validate_status(data["status"]):
        return jsonify({"error": "status debe ser pending o completed"}), 400

    due_date = task.due_date
    if "due_date" in data:
        due_date = parse_due_date(data.get("due_date"))
        if data.get("due_date") and due_date is None:
            return jsonify({"error": "Formato de due_date inválido. Use ISO 8601"}), 400

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.priority = data.get("priority", task.priority)
    task.status = data.get("status", task.status)
    task.due_date = due_date

    if task.status == "completed" and task.completed_at is None:
        task.completed_at = datetime.now(timezone.utc)
    elif task.status == "pending":
        task.completed_at = None

    db.session.commit()

    return jsonify({"message": "Tarea actualizada correctamente", "task": task.to_dict()}), 200


@tasks_bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id: int):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Tarea eliminada correctamente"}), 200


@tasks_bp.patch("/<int:task_id>/complete")
@jwt_required()
def complete_task(task_id: int):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    task.status = "completed"
    task.completed_at = datetime.now(timezone.utc)

    db.session.commit()

    return jsonify({"message": "Tarea completada correctamente", "task": task.to_dict()}), 200


@tasks_bp.get("/summary")
@jwt_required()
def task_summary():
    user_id = int(get_jwt_identity())
    tasks = Task.query.filter_by(user_id=user_id).all()

    total = len(tasks)
    completed = sum(1 for task in tasks if task.status == "completed")
    pending = sum(1 for task in tasks if task.status == "pending")
    overdue = sum(1 for task in tasks if task.is_overdue())

    completion_rate = round((completed / total) * 100, 2) if total else 0

    return jsonify(
        {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "overdue_tasks": overdue,
            "completion_rate": completion_rate,
        }
    ), 200
