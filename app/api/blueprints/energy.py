from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete
from sqlalchemy import and_
from datetime import datetime
from ...models import *
from ... import db

energy_blueprint = Blueprint("energy", __name__, url_prefix="/energy")


@energy_blueprint.route("/", methods=["GET"])
def energy_handler():
    if request.method == "GET":
        return get_energy_usage()
    return jsonify({"Error": "Invalid"}), 500


# GET - retrieve energy_records from db based on a date range (startDate, endDate)
def get_energy_usage():
    # Query parameters
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")

    # Validate required fields
    if not start_date or not end_date:
        return jsonify({"Error": "Missing required fields: startDate, endDate"}), 400

    # Convert to date format
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"Error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Check if start_date before end_date
    if start_date > end_date:
        return jsonify({"Error": "startDate cannot be after endDate"}), 400

    # Query the database and order results by date then hour
    statement = (
        select(EnergyRecords)
        .where(and_(EnergyRecords.date >= start_date, EnergyRecords.date <= end_date))
        .order_by(EnergyRecords.date, EnergyRecords.hour)
    )

    with db.engine.connect() as conn:
        results = conn.execute(statement).fetchall()

    if not results:
        return jsonify({"Error": "No records found for the given date range"}), 404

    energy_usage = [record.energyUse for record in results]
    energy_generation = [record.energyUse for record in results]
    

    response = {
        "energyUsage": energy_usage,
        "energyGeneration": energy_generation,
    }

    return jsonify(response), 200


# Check with: curl -X GET "http://localhost:5000/api/energy/?startDate=2025-01-01&endDate=2025-01-02"
