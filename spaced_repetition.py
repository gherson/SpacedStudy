# Enter "5" to practice with your imported flash cards via spaced repetition.
# Level 0 cards not seen for 2^0 days will be presented, as will
# level 1 cards not seen for 2^1 days, level 2 cards not seen for 2^2 days, etc,
# up to level 5. At level 5, cards are either promoted to a harder game, retired if already at the hardest game, or demoted to 0 if recalled incorrectly.
# Cards correctly recalled go up a level while those that are not are set to level 0.

import sqlite3
import time
from colored import fg
import random
import sys

# Adapted from https://repl.it/@abdullahrajput9/QUIZ#main.py
def typewrite(text):
    color = random.randint(0,5)
    if color == 0:
        color = fg("blue")
    elif color == 1:
        color = fg("yellow")
    elif color == 2:
        color = fg("magenta")
    elif color == 3:
        color = fg("cyan")
    elif color == 4:
        color = fg("hot_pink_3a")
    elif color == 5:
        color = fg("red")
    # Typewrite text with the same color chosen at random.
    for char in (color + text):
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)
    # Restore white lettering and add a carriage return.
    sys.stdout.write(fg("white") + "\n")
    sys.stdout.flush()

def quiz():
    print("\nThe [yNq] printed after each prompt enumerate your choices. You can also simply enter the (case insensitive) answer. Finally, 'p', when present in the choices, allows you to 'promote' the card: For most subjects, for a gentler learning curve, you're shown a (virtual) card back and asked to recall the card's front. After doing that 5 times in a row, the card is automatically /promoted/ to the reverse presentation, where a streak of another 5 wins retires the card as learned.\n")
    conn = sqlite3.connect("leitner_box.db")
    curs = conn.cursor()
    """ Commented out until Sqlite has exp() enabled, i.e., an exponentiation-including function library is loaded.
    cards = curs.execute(""SELECT c.* FROM cards AS c 
        WHERE c.level < 6 AND (
            c.last_tested IS NULL OR 
            (c.last_tested < (strftime('%s','now') - (2**c.level * 86400))))"")"""
    # Eg, for level 1 cards lasted tested exactly 2 days ago, the latter part of this SELECT is equivalent to
    #            c.last_tested < (NOW - (2**c.level * sec in a day)"), or
    # NOW - (2 * sec in a day) <  NOW - (2**1 * sec in a day).
    # This evaluates to false, as the two sides of the inequality are equal (by 2 == 2**1).  

    curs.execute("""SELECT s.instructions, c.id, c.subject, c.front, c.back, c.game, c.level, c.last_tested 
    FROM cards AS c, subjects AS s 
    WHERE c.subject = s.subject AND c.level < 6
    ORDER BY c.subject, c.level DESC, RANDOM()""")
    # We order by subject to present card families together, by level to retire cards asap, and randomly to lower tedium.
    cards = curs.fetchall()
    if len(cards) == 0:
        print("No cards found. You can use script 'flash card import.py' to import questions, e.g., vocabulary.txt, by setting the contents of .replit to: run=\"python 'flash card import.py'\". Then click the Run button")
        return 0, 0, ""

    # Filter out the cards whose time hasn't come. And decide subject_count.
    subject_counts, per_subject_card_count, prior_subject = dict(), 0, ""
    temp = list()
    for card in cards:
        instructions, id, subject, front, back, game, level, last_tested = card
        if subject != prior_subject:
            if prior_subject:
                subject_counts[prior_subject] = per_subject_card_count
                per_subject_card_count = 0
        prior_subject = subject
        # Skip if last_tested >= (NOW - (2**level * SECONDS_IN_A_DAY))
        # i.e., if last_tested and last_tested >= (time.time() - (2**level * 86400)).
        if not last_tested or last_tested < (time.time() - (2**level * 86400)):
            #print("(skipped card:", card, 'at time', int(time.time()), ')')  
            temp.append(card)
            per_subject_card_count += 1
        #else:
            #print("(non-skipped card:", card, 'at time', int(time.time()), ')')  
    cards = temp
    subject_counts[subject] = per_subject_card_count  # Last subject.
    print("Subject counts:", subject_counts)

    # The proportion of each subject to quiz.
    SHOW_TOTAL = 25
    fraction_to_show = SHOW_TOTAL / len(cards)  # <= 25/100: ask a quarter of each subject's cards (for 25 questions total).
    if len(cards) <= SHOW_TOTAL:
        print("I'll present all", str(len(cards), "cards collected"))
    else:
        print("I'll present", str(round(len(cards) * fraction_to_show)), "of the", str(len(cards)), "cards collected.")

    # Present remaining cards while tracking the player success.
    responses, response, errors, prior_subject = 0, "", 0, ""
    per_subject_card_count = 0
    for card in cards:
        instructions, id, subject, front, back, game, level, last_tested = card
        #print("subject, instructions:", subject, instructions)

        if prior_subject != subject:
            per_subject_card_count = 0
            typewrite("\nInstructions for subject "+ subject +": "+ instructions[13:] +"\n")  # Skip "Instructions: "
        elif per_subject_card_count > (subject_counts[subject] * fraction_to_show):  # Eg, 4 > (12 * 0.25)
            continue  # This subject's turn is over.
        per_subject_card_count += 1
        if game == 'f2b':
            response = input("What is "+ front +"? [q]: ").upper()
            followup_qn = "Was your recollection accurate? [yNhq]: "
            answer = back
        else:
            response = input(back +" is the answer. What is the question? [q]: ").upper()
            followup_qn = "Was your recollection accurate? [yNhp]: "
            answer = front
        if response == 'Q':
            print("Quitting...")
            break
        if response.lower().strip() == answer.lower().strip():
            print("Correct!")
            if level == 5 and game == 'b2f':  # Promote to 'f2b'.
                game = 'f2b'
                new_level = 0  # Start at bottom.
            else:
                new_level = level + 1 
        else:
            print(answer)
            response = input(followup_qn).upper()
            if response == 'H':
                print(instructions)
            elif response == 'P':  # 'P'romotion to harder game,
                game = 'f2b'
                new_level = 0  # while resetting the level.
            elif not response or response[0] != "Y":
                errors += 1
                new_level = 0  # Busted
            # 'Y' entered.
            elif level == 5 and game == 'b2f':  # Promote to 'f2b'.
                game = 'f2b'
                new_level = 0  # Start at bottom.
            else:
                new_level = level + 1  # Bested
        curs.execute("UPDATE cards SET game = ?, level = ?, last_tested = ? WHERE id = ?", (game, new_level, int(time.time()), id))  
        conn.commit()
        prior_subject = subject
        responses += 1
    if response != 'Q':
        print("Recall testing complete. Good work!\n")
    return responses, errors, ""
