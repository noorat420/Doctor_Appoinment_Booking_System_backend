from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from route_handlers.auth_routehandler import AuthController
from route_handlers.patient_routehandler import PatientController
from route_handlers.doctor_routehandler import DoctorController
from route_handlers.appointment_routehandler import AppointmentController
from route_handlers.availability_routehandler import AvailabilityController

from utils.decorators import role_required


def register_routes(app):

    # ---------------- HEALTH ----------------
    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "ok"}

    # ---------------- AUTH ----------------
    @app.route("/auth/register", methods=["POST"])
    def register():
        data = request.get_json()
        return AuthController.register(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
            invitation_code=data.get("invitation_code")
        )

    @app.route("/auth/login", methods=["POST"])
    def login():
        data = request.get_json()
        return AuthController.login(
            email=data.get("email"),
            password=data.get("password")
        )

    @app.route("/auth/me", methods=["GET"])
    @jwt_required()
    def me():
        user_id = int(get_jwt_identity())
        return AuthController.get_current_user(user_id)

    # ---------------- DOCTOR ----------------
    @app.route("/doctor/dashboard", methods=["GET"])
    @jwt_required()
    @role_required("doctor")
    def doctor_dashboard():
        return DoctorController.get_dashboard()

    @app.route("/doctor/profile", methods=["GET"])
    @jwt_required()
    @role_required("doctor")
    def get_doctor_profile():
        user_id = int(get_jwt_identity())
        return DoctorController.get_profile(user_id)

    @app.route("/doctor/profile", methods=["POST"])
    @jwt_required()
    @role_required("doctor")
    def update_doctor_profile():
        user_id = int(get_jwt_identity())
        data = request.get_json()
        return DoctorController.update_profile(
            user_id=user_id,
            designation=data.get("designation"),
            specialization=data.get("specialization")
        )

    @app.route("/doctor/account", methods=["DELETE"])
    @jwt_required()
    @role_required("doctor")
    def delete_doctor_account():
        user_id = int(get_jwt_identity())
        return DoctorController.delete_account(user_id)

    # ---------------- PATIENT ----------------
    @app.route("/patient/dashboard", methods=["GET"])
    @jwt_required()
    @role_required("patient")
    def patient_dashboard():
        return PatientController.get_dashboard()

    @app.route("/patient/doctors", methods=["GET"])
    @jwt_required()
    @role_required("patient")
    def list_doctors():
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)
        return PatientController.list_doctors(page=page, limit=limit)

    @app.route("/patient/doctors/<int:doctor_id>/availability", methods=["GET"])
    @jwt_required()
    @role_required("patient")
    def doctor_availability(doctor_id):
        return PatientController.get_doctor_availability(doctor_id)

    # ---------------- AVAILABILITY ----------------
    @app.route("/doctor/availability", methods=["POST"])
    @jwt_required()
    @role_required("doctor")
    def create_availability():
        user_id = int(get_jwt_identity())
        data = request.get_json()
        return AvailabilityController.create_slot(
            user_id=user_id,
            date_str=data.get("date"),
            start_time_str=data.get("start_time"),
            end_time_str=data.get("end_time")
        )

    # ---------------- APPOINTMENTS ----------------
    @app.route("/appointments", methods=["POST"])
    @jwt_required()
    @role_required("patient")
    def book_appointment():
        patient_id = int(get_jwt_identity())
        data = request.get_json()
        return AppointmentController.book_appointment(
            patient_id=patient_id,
            slot_id=data.get("slot_id")
        )

    @app.route("/appointments/my", methods=["GET"])
    @jwt_required()
    @role_required("patient")
    def my_appointments():
        patient_id = int(get_jwt_identity())
        return AppointmentController.get_patient_appointments(patient_id)

    @app.route("/appointments/doctor", methods=["GET"])
    @jwt_required()
    @role_required("doctor")
    def doctor_appointments():
        user_id = int(get_jwt_identity())
        return AppointmentController.get_doctor_appointments(user_id)

    @app.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
    @jwt_required()
    def cancel_appointment(appointment_id):
        user_id = int(get_jwt_identity())
        claims = get_jwt()
        return AppointmentController.cancel_appointment(
            appointment_id=appointment_id,
            user_id=user_id,
            role=claims.get("role")
        )
