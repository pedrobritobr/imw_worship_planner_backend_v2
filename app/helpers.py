import pandas as pd
from datetime import datetime
import pytz
import Levenshtein

def normalize_df(df):
    df["planner_selectedDate"] = pd.to_datetime(df["planner_selectedDate"]).dt.date
    df["planner_activities"] = df["planner_activities"].apply(
        lambda activities: [
            {**activity, "duration": int(activity["duration"])} for activity in activities
        ]
    )

    tz = pytz.timezone('America/Sao_Paulo')
    df["tsIngestion"] = pd.to_datetime(datetime.now(tz))

    df['planner_selectedDate'] = df['planner_selectedDate'].astype(str)
    df['tsIngestion'] = df['tsIngestion'].astype(str)

    return df

def capitalize_words(text):
    words = text.split()
    capitalized_words = [word.capitalize() if len(word) > 2 else word for word in words]
    return ' '.join(capitalized_words)

def deduplicate_by_similarity(strings, threshold=2):
    result = []
    for s in strings:
        if not any(Levenshtein.distance(s, r) <= threshold for r in result):
            result.append(s)
    return result

def nested_planner(planner):
    return {
        "id": planner["planner_id"],
        "activities": planner["planner_activities"],
        "selectedDate": planner["planner_selectedDate"],
        "ministerSelected": planner["planner_ministerSelected"],
        "worshipTitle": planner["planner_worshipTitle"],
        "churchName": planner["planner_churchName"],
        "creator": {
            "name": planner["user_name"],
            "email": planner["user_email"],
            "church": planner["user_church"]
        }
    }
