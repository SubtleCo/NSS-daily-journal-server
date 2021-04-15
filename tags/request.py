import sqlite3
import json
from models import Entry, Mood, Tag

def get_all_tags():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            id,
            subject
        FROM tag
        """)

        dataset = db_cursor.fetchall()

        tags = []

        for row in dataset:
            tag = Tag(row['id'], row['subject'])
            tags.append(tag.__dict__)

    return json.dumps(tags)