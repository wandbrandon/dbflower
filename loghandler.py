import sqlite3
dbfile = sqlite3.connect("flowers2019.db")
db = dbfile.cursor()

#create index for sightings
db.execute('''
            CREATE INDEX sightdex
            ON sightings (name, person, location, sighted)
            ''')

#create log table
db.execute('''
            CREATE TABLE data_log (
                timestamp DATETIME NOT NULL
                        DEFAULT CURRENT_TIMESTAMP, 
                action VARCHAR(255) NOT NULL,
                on_table VARCHAR(255) NOT NULL,
                oldname VARCHAR(255),
                newname VARCHAR(255) NOT NULL,
                user VARCHAR(255) NOT NULL
            );
            ''')

#create the trigger logging
db.execute('''
            CREATE TRIGGER upflower 
            AFTER UPDATE ON flowers
            BEGIN
                INSERT INTO data_log (action, on_table, oldname, newname, user)
                VALUES("Update", "Flowers", OLD.comname, NEW.comname, "test");
            END;
            ''')

db.execute('''
            CREATE TRIGGER insightings 
            AFTER INSERT ON sightings
	    BEGIN
                INSERT INTO data_log (action, on_table, oldname, newname, user)
                VALUES("Insert", "Sightings", NULL, NEW.name, "test");
	    END;
            ''')
