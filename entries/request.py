import sqlite3
import json
from models import Entry, Mood


def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            e.instructor_id,
            m.label mood_label
        FROM Entry e
        JOIN Mood m
            ON m.id = e.mood_id
        """)

        dataset = db_cursor.fetchall()

        entries = []

        for row in dataset:
            entry = Entry(row['id'],
                          row['date'],
                          row['concept'],
                          row['entry'],
                          row['mood_id'],
                          row['instructor_id'])

            mood = Mood(row['mood_id'], row['mood_label'])
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

    return json.dumps(entries)


def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            e.instructor_id
        FROM Entry e
        WHERE e.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'],
                      data['date'],
                      data['concept'],
                      data['entry'],
                      data['mood_id'],
                      data['instructor_id'])
    
    return json.dumps(entry.__dict__)

def get_entries_by_search(search_term):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            e.instructor_id
        FROM Entry e
        WHERE e.entry LIKE ?
        """, (f"%{search_term}%", ))

        dataset = db_cursor.fetchall()

        entries = []

        for row in dataset:
            entry = Entry(row['id'],
                          row['date'],
                          row['concept'],
                          row['entry'],
                          row['mood_id'],
                          row['instructor_id'])
            entries.append(entry.__dict__)

    return json.dumps(entries)


def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entry
        WHERE id = ?
        """, (id, ))