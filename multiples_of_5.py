# Enter "2" to practice multiples of 15 - 75.
import random

def quiz():
    intro = """
    15*2=30 15*3=45 15*4=60 15*5=75 15*6=90 15*7=105 15*8=120 15*9=135
    25*2=50 25*3=75 25*4=100 25*5=125 25*6=150 25*7=175 25*8=200 25*9=225
    35*2=70 35*3=105 35*4=140 35*5=175 35*6=210 35*7=245 35*8=280 35*9=315
    45*2=90 45*3=135 45*4=180 45*5=225 45*6=270 45*7=315 45*8=360 45*9=405
    55*2=110 55*3=165 55*4=220 55*5=275 55*6=330 55*7=385 55*8=440 55*9=495
    65*2=130 65*3=195 65*4=260 65*5=325 65*6=390 65*7=455 65*8=520 65*9=585
    75*2=150 75*3=225 75*4=300 75*5=375 75*6=450 75*7=525 75*8=600 75*9=675"""
    print("With the goal memorization of", intro, "\nyou will now be asked for those products at random. (Enter nothing or q to quit.)")

    response, responses, errors = 1, 0, 0
    while response:  # Until user enters nothing to quit,
        # generate the multiplication to ask user.
        int2to9 = random.randint(2, 9) # [2, 9]
        int3to15 = 10  
        while (5 * int3to15) % 10 == 0:  # Multiples of 10 are too easy.
            int3to15 = random.randint(3, 15)
        multiple_of_5 = 5 * int3to15  # <= multiple of 5 ending in "5" in range 15 to 75.
        answer = str(multiple_of_5 * int2to9)  # Correct answer is a multiple of 5 in range [25, 675].

        # Until valid response, keep asking for a response.
        while True:  
            response = input(str(multiple_of_5) + " * " + str(int2to9) + " = ? ").strip(". \t").upper()
            if response == 'Q':
                response = ""
            if not response or response.isnumeric():  # No response means game over.
                break  # Response is valid.

        # If no response, loop will exit.
        # If response is incorrect, feed back.
        if response and answer != response:
            errors += 1
            print("No, the correct answer is", answer)
        if response:
            responses += 1
    return responses, errors, ""
