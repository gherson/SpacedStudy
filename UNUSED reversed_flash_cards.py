# NO LONGER USED -- LOGIC ADDED TO spaced_repetition.py 2020-10-16.

# Enter "6" to practice with your flash cards in reverse. I.e., their back is given and you attempt to recall their front. 
# Level 6 cards are ignored. Other than that, cards.level isn't used.
# Created 2020-10-11 GHerson
import sqlite3
import time

def quiz():
    print("\nThe [yNq] printed after each prompt enumerate your choices. 'N', the default, means No. 'y', means Yes. 'p', when present, allows promotion of the card from a status of Show Back to Show Prompt. 'q' stands for Quit.")
    conn = sqlite3.connect("leitner_box.db")
    curs = conn.cursor()
    curs.execute("""SELECT c.* FROM cards AS c, subjects AS s 
    WHERE c.subject = s.subject AND c.level < 6
    ORDER BY c.subject, RANDOM()""")   
    cards = curs.fetchall()
    if len(cards) == 0:
        print("No cards found. You can use script 'flash card import.py' to import, e.g., vocabulary.txt, by setting the contents of .replit to: run=\"python 'flash card import.py'\". Then click the Run button")
        return 0, 0, ""

    # Present all cards in turn while tracking user's success.
    responses, errors, prior_subject = 0, 0, ""
    for card in cards:
        id, subject, front, back, game, level, last_tested = card
        if prior_subject != subject:
            print("\nBeginning subject", subject)
            # print("\nInstructions for subject", subject +":", instructions[13:].strip())
        response = input("Attempt recollection of "+ back +"'s prompt and press Enter: ")
        if response == 'Q':
            break
        print(front)
        response = input("Was your recollection accurate? [pyNq]: ").upper()
        if response == 'Q':
            break
        elif response == 'P':
            pass
        elif response == 'Y':
            pass
        prior_subject = subject
        responses += 1
    print("Recall testing complete. Good work!\n")
    return 0, errors, ""  # 0 for responses so this training is kept "off the record", ie, not databased.
