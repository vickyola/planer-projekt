from flask import Flask, request, render_template, jsonify
from datetime import datetime, timedelta
import json
import logging

import pandas as pd


from planer import (
    load_tasks,
    save_tasks,
    create_new_task,
    update_task,
    delete_task,
    move_task_to_slot,
    get_tasks_for_week,
    generate_weekly_statistics,
)


app = Flask(__name__)


@app.route("/")
def home():
    return "Flask läuft!"


@app.route("/planer", methods=["GET"])
def planer_view():
    try:
        week_offset = int(request.args.get("week_offset", 0))
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        week_dates = [(start_of_week + timedelta(days=i)).strftime("%d.%m.%Y") for i in range(7)]

        all_tasks = load_tasks()
        all_tasks["Datum"] = pd.to_datetime(all_tasks["Datum"]).dt.strftime("%d.%m.%Y")
        week_tasks = all_tasks[all_tasks["Datum"].isin(week_dates)].copy()

        week_tasks["PartitionKey"] = week_tasks["Datum"]
        tasks = week_tasks.to_dict(orient="records")

        return render_template(
            "tabs/planer.html",
            title="Wochenplaner",
            code_key="dein_code_key",
            base_route="/",
            tasks=tasks,
            week_dates=week_dates,
            week_offset=week_offset,
        )
    except Exception as e:
        logging.exception("Fehler beim Rendern der Planer-Ansicht")
        return f"Fehler beim Rendern: {e}", 500


@app.route("/api/move-task", methods=["POST"])
def move_task():
    try:
        req_data = request.get_json()
        task_id = req_data["taskId"]
        new_date = req_data["newDate"]
        new_slot = req_data["newSlot"]

        task = move_task_to_slot(task_id, new_date, new_slot)
        if not task:
            return f"Kein Task mit ID {task_id} gefunden.", 400

        return f"Task erfolgreich verschoben: {task}", 200
    except Exception as e:
        logging.exception("Fehler beim Verschieben des Tasks")
        return f"Fehler: {e}", 500

@app.route("/api/update-task", methods=["POST"])
def update_task_view():
    try:
        data = request.get_json()
        task = update_task(data)
        if not task:
            return "Fehler: Task nicht gefunden.", 404
        return "OK", 200
    except Exception as e:
        logging.exception("Update-Fehler")
        return f"Fehler: {e}", 500


@app.route("/api/create-task", methods=["POST"])
def create_task():
    try:
        data = request.get_json()
        task = create_new_task(data)
        if not task:
            return "Fehler: Task konnte nicht erstellt werden.", 404
        return "OK", 200
    except Exception as e:
        logging.exception("Fehler beim Erstellen eines Tasks")
        return f"Fehler: {e}", 500

@app.route("/api/delete-task", methods=["POST"])
def delete_task_id():
    try:
        data = request.get_json()
        task_id = data.get("taskId")
        if not task_id:
            return "Fehlende taskId", 400

        success = delete_task(task_id)
        if not success:
            return "Fehler: Task konnte nicht gelöscht werden.", 404
        return "OK", 200
    except Exception as e:
        logging.exception("Fehler beim Löschen eines Tasks")
        return f"Fehler: {e}", 500


@app.route("/api/taskstat/week", methods=["POST"])
def weekly_stats():
    try:
        data = request.get_json()
        week_dates_raw = data.get("week_dates")

        if not isinstance(week_dates_raw, list):
            return "Fehler: Ungültige oder fehlende 'week_dates'", 400

        # Konvertiere zu YYYY-MM-DD
        week_dates = [
            datetime.strptime(d, "%d.%m.%Y").strftime("%Y-%m-%d")
            for d in week_dates_raw
        ]

        print("Konvertierte Week-Dates:", week_dates)

        df = get_tasks_for_week(week_dates)
        if df.empty:
            return "Keine Tasks gefunden.", 404

        stats = generate_weekly_statistics(df)
        return jsonify(stats), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Fehler: {e}", 500



if __name__ == "__main__":
    app.run(debug=True)