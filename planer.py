import pandas as pd
from datetime import datetime, timedelta
import random
import os


TASKS_CSV = "tasks.csv"

# Initialisiere CSV falls nicht vorhanden
def init_tasks_file():
    if not os.path.exists(TASKS_CSV):
        df = pd.DataFrame(columns=[
            "ID", "Datum", "Uhrzeit", "slot", "Verantwortliche",
            "Kategorie", "Prioritaet", "Inhalt", "Status"
        ])
        df.to_csv(TASKS_CSV, index=False)
        return

# Lade Aufgaben
def load_tasks():
    return pd.read_csv(TASKS_CSV, dtype=str)

# Speichere Aufgaben
def save_tasks(df):
    df.to_csv(TASKS_CSV, index=False)


def generate_task_id(df):
    ids = df["ID"].dropna().tolist()
    nums = [int(i.split("-")[1]) for i in ids if i.startswith("task-")]
    max_id = max(nums) if nums else 0
    return f"task-{max_id + 1:05d}"


def create_new_task(data):
    df = load_tasks()

    task_id = generate_task_id(df)
    datum = data["Datum"]
    uhrzeit = data["Uhrzeit"]
    slot = datetime.strptime(uhrzeit, "%H:%M").strftime("%H%M")

    task = {
        "ID": task_id,
        "Datum": datum,
        "Uhrzeit": uhrzeit,
        "slot": slot,
        "Verantwortliche": data["Verantwortliche"],
        "Kategorie": data["Kategorie"],
        "Prioritaet": data["Prioritaet"],
        "Inhalt": data["Inhalt"],
        "Status": data["Status"],
    }

    df = df.append(task, ignore_index=True)
    save_tasks(df)

    return task


def delete_task(task_id):
    df = load_tasks()
    idx = df[df["ID"] == task_id].index

    if idx.empty:
        return None  # Kein Task mit dieser ID gefunden

    df = df.drop(index=idx[0])
    save_tasks(df)
    return True



def update_task(task_data):
    df = load_tasks()
    idx = df[df["ID"] == task_data["taskId"]].index

    if idx.empty:
        return None

    i = idx[0]
    for key in ["Inhalt", "Status", "Kategorie", "Prioritaet", "Verantwortliche"]:
        df.at[i, key] = task_data[key]

    save_tasks(df)
    return df.loc[i].to_dict()

def move_task_to_slot(task_id, new_date, new_slot):
    df = load_tasks()
    idx = df[df["ID"] == task_id].index

    if idx.empty:
        return None

    i = idx[0]
    df.at[i, "Datum"] = new_date
    df.at[i, "slot"] = new_slot
    df.at[i, "Uhrzeit"] = f"{new_slot[:2]}:{new_slot[2:]}"
    save_tasks(df)

    return df.loc[i].to_dict()


def generate_weekly_statistics(df):
    themen_counts = df["Kategorie"].value_counts().to_dict()

    # Beispielhafte Mindestanforderungen
    min_requirements = {
        "Arbeit": 5,
        "Haushalt": 3,
        "Freizeit": 4,
    }

    topic_load = {}
    for k, v in min_requirements.items():
        actual = themen_counts.get(k, 0)
        percent = min(100, round(actual / v * 100)) if v else 0
        topic_load[k] = {
            "actual": actual,
            "minimum": v,
            "percent": percent,
        }

    fulfilled = sum(1 for t in topic_load.values() if t["actual"] >= t["minimum"])
    total = len(min_requirements)

    return {
        "themenverteilung": themen_counts,
        "erfuellte_themen_prozent": round((fulfilled / total) * 100) if total else 0,
        "topic_load": topic_load,
        "details": {"erfuellt": fulfilled, "gesamt": total},
    }


def get_tasks_for_week(week_dates):
    df = load_tasks()
    print("Week filter:", week_dates)
    print("Available dates in tasks:", df["Datum"].unique())
    df_filtered = df[df["Datum"].isin(week_dates)]
    print("Gefundene Tasks:", len(df_filtered))
    return df_filtered


def get_week_dates(start_date=None):
    today = start_date or datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    return [(start_of_week + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]


def generate_example_tasks(n=20):
    verantwortliche = ["Anna", "Ben", "Clara", "David"]
    kategorien = ["Haushalt", "Arbeit", "Freizeit", "Bildung", "Wohnen", "Einkaufen"]
    prioritaeten = ["hoch", "mittel", "niedrig"]
    inhalte = ["Bericht schreiben", "Zimmer aufräumen", "Mathe lernen", "Joggen im Park", "Reparatur erledigen"]
    status_werte = ["Geplant", "In Arbeit", "Erledigt"]

    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    data = []

    for i in range(n):
        day_offset = random.randint(0, 6)
        time_slot = random.choice(["08:00", "08:30", "09:00", "10:00", "12:00", "14:00", "16:00", "17:30"])
        dt = start_of_week + timedelta(days=day_offset)

        date_str = dt.strftime("%Y-%m-%d")
        slot = time_slot.replace(":", "")
        task = {
            "ID": f"task-{i+1:05d}",
            "Datum": date_str,
            "Uhrzeit": time_slot,
            "slot": slot,
            "Verantwortliche": random.choice(verantwortliche),
            "Kategorie": random.choice(kategorien),
            "Prioritaet": random.choice(prioritaeten),
            "Inhalt": random.choice(inhalte),
            "Status": random.choice(status_werte)
        }
        data.append(task)

    df = pd.DataFrame(data)
    df.to_csv("tasks.csv", index=False)
    print("Beispiel-Tasks gespeichert.")


# Direkt testen:
if __name__ == "__main__":
    generate_example_tasks(20)