from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from sqlalchemy import or_

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos JSON"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "username, email y password son obligatorios"}), 400

    existing_user = User.query.filter(
        or_(User.username == username, User.email == email)
    ).first()

    if existing_user:
        return jsonify({"error": "El usuario o correo ya existe"}), 409

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            "message": "Usuario registrado correctamente",
            "user": user.to_dict(),
        }
    ), 201


@auth_bp.post("/login")
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email y password son obligatorios"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify(
        {
            "message": "Login exitoso",
            "access_token": access_token,
            "user": user.to_dict(),
        }
    ), 200
