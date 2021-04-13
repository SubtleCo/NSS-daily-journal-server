CREATE TABLE 'Entries' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'date' TEXT NOT NULL,
    'concept' TEXT NOT NULL,
    'entry' TEXT NOT NULL,
    'mood_id' INTEGER NOT NULL,
    'instructor_id' INTEGER NOT NULL,
    FOREIGN KEY('mood_id') REFERENCES 'Moods'('id'),
    FOREIGN KEY('instructor_id') REFERENCES 'Instructors'('id')
);
CREATE TABLE 'Moods' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'label' TEXT NOT NULL UNIQUE
);
CREATE TABLE 'Tags' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'subject' TEXT NOT NULL
);
CREATE TABLE 'Instructors' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'first_name' TEXT NOT NULL,
    'last_name' TEXT NOT NULL
);
CREATE TABLE 'entry_tags' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'entry_id' INTEGER NOT NULL,
    'tag_id' INTEGER NOT NULL,
    FOREIGN KEY('entry_id') REFERENCES 'Entries'('id'),
    FOREIGN KEY('tag_id') REFERENCES 'Tags'('id')
);

INSERT INTO 'entry_tags'
VALUES (null,2,2),
    (null,3,1),
    (null,2,4),
    (null,4,3),
    (null,4,1),
    (null,6,5),
    (null,7,5),
    (null,1,5),
    (null,4,5);

SELECT * FROM 'entry_tags'
