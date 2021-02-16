# Enter "1" to practice 15% tipping.
# todo Disallow decoy_offset's too low to distinguish from 15% (due to int() rounding).
import random
import math
import time

def quiz():
    DECOY_OFFSET = 0.2  # Lower is closer to 15% and thus harder to distinguish.

    print("Hints: To be 15%, the numerator must of course be middling between 10% and 20% of the denominator. And numerator and denominator must be the same multiple of 3 and 20, respectively. That also means that the sum of the numerator's digits must be divisible by 3, and the portion of the denominator before the '0' must be even.")

    response, responses, errors = "", 0, 0
    while response != 'q':  # Until user quits.
        # Generate the fraction to present.
        rand = random.randint(1,50) # [1, 50]
        # Multiples of 3 and 20 (15/100 reduces to 3/20).
        numerator = 3 * rand
        denominator = 20 * rand
        # Half the time, replace numerator w/a decoy.
        if int(str(time.time())[-1]) % 2 == 0:
            if rand % 2 == 0:  # And half of decoys to go
                numerator *= 1 + DECOY_OFFSET  # over 15%,
            else:
                numerator *= 1 - DECOY_OFFSET  # & half, under.
            numerator = int(numerator)  # Ints throughout.

        # Until valid response, keep asking user if given fraction represents 15%.
        while True:  
            response = input(str(numerator) + "/" + str(denominator) + " == 15%? (Ynq): ").lower()
            if not response:
                response = "y"  # default
            if response in 'ynq' and len(response) == 1:
                break  # Response is valid.
        # If response incorrect, feed back.
        if math.isclose(0.15, numerator/denominator):
            if response == "n":  # False negative.
                errors += 1
                print("Incorrect")
        else:
            if response == "y":  # False positive.
                errors += 1
                print("No,", str(round(100*numerator/denominator,3)) + "%")
        if response != "q":
            responses += 1
    return responses, errors, DECOY_OFFSET
