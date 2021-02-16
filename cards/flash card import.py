# Code to allow a user to import from named file the textual
# content s/he would like to memorize
# into level 0 of their simulated Leitner box.
# To run, temorarily change .replit to specify:
# run="python 'cards/flash card import.py'"
# Created 2020-10-08 GHerson

# import sys; print(sys.version); quit()  # => 3.8.5
import sqlite3
import time
import os

# Print database status, # of cards, and optionally, the cards themselves.
def db_status(tables_to_dump=[]): 
    print("The tables extant:")
    c.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
    tables = c.fetchall()
    print(tables)

    c.execute("""SELECT COUNT(*) FROM cards""")
    card_count = c.fetchall()
    print("Card count:", card_count)

    for table in tables_to_dump: 
        print("All records of `" + table + "`:")
        c.execute("SELECT * FROM `" + table + "`")
        dump = c.fetchall()
        for record in dump:
            print(record)
    print()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

conn = sqlite3.connect("leitner_box.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS cards
(id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, front TEXT, back TEXT, game TEXT, level INTEGER, last_tested INTEGER, FOREIGN KEY(subject) REFERENCES subjects(subject))''')

c.execute('''CREATE TABLE IF NOT EXISTS subjects
(subject TEXT PRIMARY KEY, instructions TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS log_of_tests
(date INTEGER, card_id INTEGER, success INTEGER)''') 

# SQL scrap pile. N.B. conn.commit() is required.
# c.execute("INSERT OR REPLACE INTO subjects (subject, instructions) VALUES (?, ?)", ("adjectives", "Instructions: Do you know a few, less-common words close in meaning to the following given words?")) 
# c.execute("INSERT OR REPLACE INTO subjects (subject, instructions) VALUES (?, ?)", ("vocabulary", "Instructions: Recall the meaning of each presented word.")) 
# conn.commit()
# db_status(["subjects"]); quit()
# c.execute("DELETE FROM cards WHERE front='Confusing'"); conn.commit(); quit()
# sqlite3.sqlite3_enable_load_extension(db,1)
# c.execute("SELECT load_extension('libsqlitefunctions.so')")
# c.execute("select cos(radians(45))"); print(c.fetchall()); 
# c.execute("SELECT exp(2,2), strftime('%s','now')"); print(c.fetchall()); quit()
# c.execute("ALTER TABLE cards ADD column game TEXT");
# c.execute("DELETE FROM cards WHERE subject='temp'");
# c.execute("SELECT COUNT(*) FROM cards WHERE subject='adjectives'"); 
# print(c.fetchall())
# quit()
# c.execute("UPDATE cards SET game='f2b' WHERE subject='purchasing'"); 
# c.execute("INSERT INTO subjects (subject, instructions) VALUES (?, ?)", 
#             ('vocabulary', instructions:='Instructions:  Recall the meaning of each presented word.')); 
# db_status(["subjects"]); quit()
# c.execute("INSERT INTO log_of_tests VALUES (" + str(int(time.time())) + ", 1, 1)")
# Use with caution: c.execute('''DROP TABLE cards'''); quit()
# conn.commit(); db_status(['cards']); quit()

print("This script is for importing simulated flash cards into your simulated Leitner Box (for you to then utilize spaced repetition to memorize). The flash cards must be in a file with a line of instructions. Then alternate between a flush left 'card front' and an indented 'card back', with no blank lines. (Lines that begin with '#' are ignored.) See vocabulary.txt for an example.")
input_file = input("Please name the /cards file to import: ")

f = open("cards/"+ input_file, encoding="utf8")
subject = os.path.splitext(input_file)[0]  # <= the filename sans extension.
confirm = input("Should the subject of these cards be '" + subject + "'? [Yn]: ").upper()
if confirm and confirm[0] == 'N':
    subject = input("Please provide the subject: ").strip()

b2f_yn = input("Should the first presentation of these cards be their back side, to recall their front side? [Yn]").upper()
if b2f_yn == 'Y':
    first_game = 'b2f'
else:
    first_game = 'f2b'

print("File '" + input_file + "' will first be sanity checked, then the results shown, before continuing with import, with your permission.")
input("Specifically, the named file's format is checked, and card backs that are shorter than their front or prompt are printed. \nPress Enter to continue.")

front, lines, warnings = None, 0, 0
while line := f.readline():  # Walrus operator returns value assigned.
    # print("line:'" + line + "'")  # \r and \n will be stripped.
    if line[0] == "#":  # Skip comments.
        continue
    assert line.strip(" \r\n\t"), "Blank lines are not permitted (because strictness mitigates misunderstanding)."
    if front:  # Then the `line` just read is the card back corresponding to the current `front`.
        assert not line[0].strip(" \r\n\t"), "'" + line[:-1] + "', the back side of card '" + front + "', does not begin with whitespace as required."
        line = line.strip(" \r\n\t")
        if len(line) < len(front) and not is_number(line):
            warnings += 1
            print("Warning: back of card\t", line, "\tis smaller than its prompt\n", front)
        front = None
    else:  # `line` is (the instructions or) a card front.
        card = "Card "
        if lines == 0:
            assert line.startswith("Instructions: "), "'" + line + "' does not start with 'Instructions: '"
            card += "instructions "
        else:
            card += "front "
            front = line.strip(" \r\n\t")
        assert line[0].strip(" \r\n\t"), card + "'" + line[:-1] + "' begins with whitespace."
    lines += 1
# Sanity check complete.

confirm = input(str(lines) + " lines and " + str(warnings) + " warnings. Continue with database import with subject '" + subject + "'? [y/N]: ").upper()
if not confirm or confirm[0] != "Y":
    print("Quitting as requested\nwith current database status:")
    db_status()
    quit()

# Proceeding with import of named file. Inserts will be to cards table, at level 0.
f.seek(0)  # Reset file pointer to top.
front, line, first_line = None, None, True
while line := f.readline():  
    if line[0] == "#":
        continue
    line = line.strip(" \r\n\t")
    if first_line:
        print("Replacing instructions '" + line + "' in/to subjects table.")
        c.execute("INSERT OR REPLACE INTO subjects (subject, instructions) VALUES (?, ?)", (subject, line))  
        first_line = False
    elif front and line:  # Then `line` is the card back.
        print("Inserting line '" + line + "' into cards.")
        c.execute("INSERT INTO cards (subject, front, back, game, level) VALUES (?, ?, ?, ?, 0)", (subject, front, line, first_game)) 
        front = None  # Reset.
    elif not front:
        front = line  # Start new card.

print("Import complete.")
db_status(["cards"])
commit = input("Commit? [yN]: ").upper()
if commit and commit[0] == 'Y':
    conn.commit()
db_status()