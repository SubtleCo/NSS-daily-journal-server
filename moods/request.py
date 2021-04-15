import sqlite3
import json
from models import Mood


def get_all_moods():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                id,
                label
            FROM mood
            """)

        dataset = db_cursor.fetchall()
        moods = []
        for row in dataset:
            mood = Mood(row['id'], row['label'])
            moods.append(mood.__dict__)

        return json.dumps(moods)