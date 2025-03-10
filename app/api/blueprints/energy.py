from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete
from sqlalchemy.sql import func
from sqlalchemy import and_
from datetime import datetime, timedelta
from ...models import *
from ... import db
from ...routes import check_authentication

energy_blueprint = Blueprint("energy", __name__, url_prefix="/energy")


@energy_blueprint.route("/", methods=["GET"])
@check_authentication
def get_energy_usage():
    # Query parameters
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")
    time_period = request.args.get("timePeriod", "hourly")

    # Validate required fields
    if not start_date or not end_date:
        return jsonify({"Error": "Missing required fields: startDate, endDate"}), 400

    # Convert to date format
    try:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = end_datetime.replace(hour=0, minute=0, second=0)
    except ValueError:
        return jsonify({"Error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Check if start_date before end_date
    if start_datetime > end_datetime:
        return jsonify({"Error": "startDate cannot be after endDate"}), 400

    # Validate time_period
    allowed_periods = {"hourly", "daily", "weekly", "monthly"}
    if time_period not in allowed_periods:
        return jsonify({"Error": f"Invalid time_period. Must be one of {allowed_periods}"}), 400

    # Define grouping logic and generate all time periods
    all_timestamps = []
    format_string = ""

    if time_period == "hourly":
        time_group = func.date_format(EnergyRecords.datetime, "%Y-%m-%d %H:00:00")
        format_string = "%Y-%m-%d %H:00:00"
        delta = timedelta(hours=1)
        current = start_datetime.replace(minute=0, second=0, microsecond=0)
        
        while current < end_datetime:
            all_timestamps.append(current.strftime(format_string))
            current += delta
    
    elif time_period == "daily":
        time_group = func.date_format(EnergyRecords.datetime, "%Y-%m-%d")
        format_string = "%Y-%m-%d"
        delta = timedelta(days=1)
        current = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

        while current < end_datetime:
            all_timestamps.append(current.strftime(format_string))
            current += delta
    
    elif time_period == "weekly":
        time_group = func.date_format(func.date_sub(
            EnergyRecords.datetime, text(f"INTERVAL (DAYOFWEEK(datetime) - 1) DAY")
        ), "%Y-%m-%d")
        format_string = "%Y-%m-%d"
        current = start_datetime - timedelta(days=start_datetime.weekday())
        current = current.replace(hour=0, minute=0, second=0, microsecond=0)
        delta = timedelta(days=7)
        
        while current < end_datetime:
            all_timestamps.append(current.strftime(format_string))
            current += delta
    
    elif time_period == "monthly":
        time_group = func.date_format(EnergyRecords.datetime, "%Y-%m")
        format_string = "%Y-%m"
        current = start_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        while current < end_datetime:
            all_timestamps.append(current.strftime(format_string))
            if current.month == 12: current = current.replace(year=current.year + 1, month=1)
            else: current = current.replace(month=current.month + 1)

    # Query database for actual data
    statement = (
        select(
            time_group.label("time_period"),
            func.sum(EnergyRecords.energyUse).label("energy_use"),
            func.sum(EnergyRecords.energyGeneration).label("energy_generation"),
        )
        .where(
            and_(EnergyRecords.datetime >= start_datetime, EnergyRecords.datetime <= end_datetime)
        )
        .group_by("time_period")
        .order_by("time_period")
    )

    with db.engine.connect() as conn:
        results = conn.execute(statement).fetchall()

    res_dict = {}
    for result in results:
        time_str, energy_usage, energy_generation = result
        res_dict[time_str] = {
            "energyUse": round(energy_usage, 3) if energy_usage is not None else None,
            "energyGeneration": round(energy_generation, 3) if energy_generation is not None else None
        }

    response = []
    for timestamp in all_timestamps:
        if timestamp in res_dict:
            response.append({
                "datetime": timestamp,
                "energyUse": res_dict[timestamp]["energyUse"],
                "energyGeneration": res_dict[timestamp]["energyGeneration"]
            })
        else:
            response.append({
                "datetime": timestamp,
                "energyUse": None,
                "energyGeneration": None
            })

    return jsonify(response), 200

# Check with: curl -X GET "http://localhost:5000/api/energy/?startDate=2025-01-01&endDate=2025-01-02"
