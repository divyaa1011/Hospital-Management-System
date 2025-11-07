"""Flask routes: simple CRUD, batch average, scraper endpoint."""

from flask import Blueprint, request, jsonify
import logging

from . import crud
from .exceptions import PatientNotFound
from .emailer import send_email_background
from .batch_calc import average_age_threaded
from .scraper import fetch_page_title
from .config import Config

api_blueprint = Blueprint("api", __name__)
logger = logging.getLogger(__name__)

@api_blueprint.errorhandler(PatientNotFound)
def handle_not_found(e):
    return jsonify({"error": str(e)}), 404

@api_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# CRUD endpoints
@api_blueprint.route("/patients", methods=["GET"])
def list_patients():
    patients = crud.get_all_patients()
    return jsonify([p.to_dict() for p in patients])

@api_blueprint.route("/patients/<int:pid>", methods=["GET"])
def get_patient(pid):
    patient = crud.get_patient(pid)
    return jsonify(patient.to_dict())

@api_blueprint.route("/patients", methods=["POST"])
def create_patient():
    data = request.get_json(force=True)
    for field in ("name", "age", "disease"):
        if field not in data:
            return jsonify({"error": f"missing {field}"}), 400
    patient = crud.create_patient(data)

    # send email in background
    if Config.TO_EMAIL:
        subject = "New patient registered"
        body = f"Patient {patient.name} (id={patient.id}) was created."
        send_email_background(Config.TO_EMAIL, subject, body)
    else:
        logger.info("TO_EMAIL not configured; skipping email")

    return jsonify(patient.to_dict()), 201

@api_blueprint.route("/patients/<int:pid>", methods=["PUT"])
def update_patient(pid):
    data = request.get_json(force=True)
    patient = crud.update_patient(pid, data)
    return jsonify(patient.to_dict())

@api_blueprint.route("/patients/<int:pid>", methods=["DELETE"])
def delete_patient(pid):
    crud.delete_patient(pid)
    return jsonify({"message": "deleted"}), 200

# Batch average endpoint (threaded)
@api_blueprint.route("/patients/average-age", methods=["GET"])
def average_age():
    # optional query param batch_size
    try:
        batch_size = int(request.args.get("batch_size", Config.BATCH_SIZE))
    except Exception:
        batch_size = Config.BATCH_SIZE
    patients = crud.get_all_patients()
    avg = average_age_threaded(patients, batch_size=batch_size)
    return jsonify({"average_age": avg})

# Scraper endpoint
@api_blueprint.route("/scrape", methods=["GET"])
def scrape():
    url = request.args.get("url", "https://www.who.int")
    data = fetch_page_title(url)
    return jsonify(data)
