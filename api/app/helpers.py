import pandas as pd
from datetime import datetime
import pytz

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
