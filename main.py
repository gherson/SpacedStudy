""" Quizzes to better your Elevate EPQ. Stay sharp! 👍
Tracks your improvement progress in db.
Created 2020-09-06 GHerson 

Todo:
* Ask for fraction from value in enter_the_fraction game. 2020-10-05
* Improve reporting. 2020-10-06"""

import time
from replit import db

try:
    if "count" not in db:  # Then this is 1st use of db.
        db["count"] = 0
        db["sum"] = 0
except TypeError:
    quit("!Please retry after creating a repl.it account (necessary for database access)!")

# To add a new game, mention in the input() prompt and add an ELIF.
ask_for_game_choice = True 
while ask_for_game_choice: 
    ask_for_game_choice = False 
    choice = input("Practice \n1) 15% tipping, \n2) multiples of 5, \n3) fractions of single digits, \n4) multiples you specify, \n5) flash cards? ")
    if choice == "1":
        game_name = "fifteen_percent"
        import fifteen_percent as game
    elif choice == "2":
        game_name = "multiples_of_5"
        import multiples_of_5 as game
    elif choice == "3":
        game_name = "enter_the_fraction"
        import enter_the_fraction as game
    elif choice == "4":
        game_name = "multiples"
        import multiples as game
    elif choice == "5":
        game_name = "spaced_repetition"
        import spaced_repetition as game
    # elif choice == "6":
    #     game_name = "reversed_flash_cards"
    #     import reversed_flash_cards as game
    else:
        ask_for_game_choice = True   # Response was invalid.
    # if "|1|2".find("|" + choice) >= 0
responses, errors, detail = game.quiz()
print("responses, errors, detail =", responses, errors, detail)

# Player exited.
if responses:  
    percent_correct = 100.*(responses - errors)/responses
    if responses > 3:  # To exclude manual code testing, only save non-trivial training.
        # To enable quick averaging.
        db["count"] += 1
        db["sum"] += percent_correct

        # Assign, eg, db['1600570367'] = ['enter_the_fraction', 75.0, 4, '']
        db[int(time.time())] = game_name, percent_correct, responses, detail  # The key is: seconds since the epoch.

        # Print, eg, "84.615% correct in this 4th training session. Your average % correct: 80.944)"
        print(str(round(percent_correct,3)) + "% correct in this", str(db["count"]+1) + "th training session. Your average % correct:", str(round(db["sum"]/db["count"],3)) + ')')
    else:
        print("(Fewer than 4 responses made so training details won't be saved.)")
        print(str(round(percent_correct,3)) + "% correct")

show_db = input("Print the database? (y/N): ").upper()
if show_db == 'Y':
    for key in db:
        print("db['" + key + "']:", db[key])

