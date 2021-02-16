# Enter "3" to practice recognition of simple fractions (1 digit top and bottom).

import random

def quiz():
    intro = """
    1/3 = 0.3333 
	2/3 = 0.6667 
	
	x ÷ 4 will have remainder 0 or .5 if x is even, else .25 or .75:
	5/4 = 1.25 
	6/4 = 1.5 
	7/4 = 1.75 
	9/4 = 2.25 
	10/4 = 2.5 
	11/4 = 2.75
	
	If /5, double numerator and prefix with dot for the decimal:
	1/5 = 0.2 
	2/5 = 0.4 
	3/5 = 0.6 
	4/5 = 0.8 
	
	Repeating:
	1/6 = 0.1667 or 16.67%
	5/6 = 1 - 1/6 = 0.8333 or 83.33% 
	
	The quotient of any integer that isn't 0 or 7 divided by 7 repeats 142857 after the decimal point, with only the starting digit varying. 
    To four decimal places:
	1/7 = 0.1429 
	2/7 = 0.2857 
	3/7 = 0.4286 
	4/7 = 0.5714 
	5/7 = 0.7143 
	6/7 = 0.8571 
	
	1/8 = 0.125	or 12.5%
	3/8 = 0.375 (.25 + .125) or 37.5%
	5/8 = 0.625 (.5 + .125) or 62.5%
	7/8 = 1 - 1/8 = 0.875 (.75 + .125) or 87.5%
	
	If /9, stutter numerator for decimal:
	1/9 = 0.1111 
	2/9 = 0.2222  
	3/9 = 0.3333 
	4/9 = 0.4444 
	5/9 = 0.5556 
	6/9 = 0.6667 
	7/9 = 0.7778 
    8/9 = 0.8889"""
    print("With the goal memorization of", intro, "\nPlease enter the decimal value accurate to 4 decimal places:")

    response, responses, errors = 1, 0, 0
    while response:  # Until user enters nothing to quit,
        # generate the multiplication to ask user.
        int1to9top = random.randint(1, 9) # [1, 9]
        int2to9bottom = int1to9top  
        while int1to9top == int2to9bottom:  # Too easy.
            int2to9bottom = random.randint(2, 9)  
        answer = 1.*int1to9top / int2to9bottom  # Correct answer.

        while True:  # Until valid response, keep prompting.
            response = input(str(int1to9top) + " / " + str(int2to9bottom) + " = ? ").strip(" \t")
            if response:
                try:
                    response = float(response)
                    break
                except ValueError:
                    print("Invalid response")
                    continue  # Re-prompt.
            else:  # No response means game over.
                break  # Response is valid.

        # If no response, loop will exit. Alternatively, if response is incorrect, feed back.
        if response:
            if (round(answer, 4) != round(response, 4)) and (abs(answer - response) > .0001):
                errors += 1
                print("No, you're off by", str(answer - response) + "; the correct answer is", str(answer))
            responses += 1      
    return responses, errors, ""
