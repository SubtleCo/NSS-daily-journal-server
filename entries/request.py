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

            db_cursor.execute("""
                SELECT * FROM entry_tag
                WHERE entry_id = ?
            """, (row['id'],))

            tag_entries = db_cursor.fetchall()

            entry.tags = []
            
            for tag_entry in tag_entries:
                db_cursor.execute("""
                    SELECT subject
                    FROM tag
                    WHERE id = ?
                """, (tag_entry['tag_id'],))
                tag = db_cursor.fetchone()
                entry.tags.append(tag['subject'])

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
            e.instructor_id,
            m.label mood_label
        FROM Entry e
        JOIN Mood m
        WHERE e.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'],
                      data['date'],
                      data['concept'],
                      data['entry'],
                      data['mood_id'],
                      data['instructor_id'])

        mood = Mood(data['mood_id'], data['mood_label'])
        entry.mood = mood.__dict__
    
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

def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO entry (concept, date, entry, mood_id, instructor_id)
        VALUES (?, ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['date'], new_entry['entry'], new_entry['moodId'], 1))

        id = db_cursor.lastrowid
        new_entry['id'] = id

        for tag in new_entry["tags"]:
            db_cursor.execute("""
            INSERT INTO entry_tag (entry_id, tag_id)
            VALUES (?,?)
            """, (id, tag['id']))

    return json.dumps(new_entry)

def update_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            UPDATE entry
                SET
                    concept = ?,
                    entry = ?,
                    mood_id = ?
            WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], new_entry['moodId'], new_entry['id']))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entry
        WHERE id = ?
        """, (id, ))