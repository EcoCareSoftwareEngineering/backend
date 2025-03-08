from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete
from sqlalchemy.sql import func
from sqlalchemy import and_
from datetime import datetime
from ...models import *
from ... import db
from ...routes import check_authentication

energy_blueprint = Blueprint("energy", __name__, url_prefix="/energy")


@energy_blueprint.route("/", methods=["GET"])
@check_authentication
def energy_handler():
    if request.method == "GET":
        return get_energy_usage()
    return jsonify({"Error": "Invalid"}), 500


# GET - retrieve energy_records from db based on a date range (startDate, endDate)
def get_energy_usage():
    # Query parameters
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")
    time_period = request.args.get("time_period", "hourly")

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

    # Validate time_period
    allowed_periods = {"hourly", "daily", "weekly", "monthly"}
    if time_period not in allowed_periods:
        return jsonify({"Error": f"Invalid time_period. Must be one of {allowed_periods}"}), 400

    # Define grouping logic for the time period
    if time_period == "hourly":
        time_group = func.date_format(EnergyRecords.datetime, "%Y-%m-%d %H:00:00")
    elif time_period == "daily":
        time_group = func.date_format(EnergyRecords.datetime, "%Y-%m-%d")
    elif time_period == "weekly":
        time_group = func.yearweek(EnergyRecords.datetime, 3)
    elif time_period == "monthly":
        time_group = func.date_format(EnergyRecords.datetime, "%Y-%m")

    # Query database
    statement = (
        select(
            time_group.label("time_period"),
            func.sum(EnergyRecords.energyUse).label("energy_use"),
            func.sum(EnergyRecords.energyGeneration).label("energy_generation"),
        )
        .where(
            and_(EnergyRecords.datetime >= start_date, EnergyRecords.datetime <= end_date)
        )
        .group_by("time_period")
        .order_by("time_period")
    )

    with db.engine.connect() as conn:
        results = conn.execute(statement).fetchall()

    if not results:
        return jsonify({"Error": "No records found for the given date range"}), 404

    response = []

    for result in results:
        ( time_period, energy_usage, energy_generation) = result
        response.append(
            {
                "datetime": time_period,
                "energyUse": round(energy_usage, 3),
                "energyGeneration": round(energy_generation, 3),
            }
        )

    return jsonify(response), 200


# Check with: curl -X GET "http://localhost:5000/api/energy/?startDate=2025-01-01&endDate=2025-01-02"
