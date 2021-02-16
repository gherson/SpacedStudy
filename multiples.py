# Enter "4" to practice multiples of your choice of integers.
import random

def quiz():
    bad_number = True
    while bad_number:
        integers = input("Enter space-separated, positive integers you want to practice multiplying (by random #s 2 through 99) [12 52]: ").split()  # <= list
        integers = [el.strip(".") for el in integers]  # In case of user over-specification.
        if not integers:  # Then nothing was entered.
            integers = ["12", "52"]  # The default.
        bad_number = [True for el in integers if not el.isnumeric()]
    integers = [int(el) for el in integers]

    intro = ""
    for factor in integers:
        # Eg, "2*2=4 2*3=6 2*4=8 2*5=10 2*6=12 2*7=14... 2*99=198"
        intro += " ".join([str(factor)+"*"+str(int2to99)+"="+str(factor*int2to99) for int2to99 in range(2, 100)])
        intro += " and\n"
    print("The goal is memorization of:\n", intro[:-4] + "\nYou will now be asked for those products at random.")

    print("Enter nothing or q at any time to quit.")
    response, responses, errors = 1, 0, 0
    while response:  # Until user enters nothing to quit,
        int2to99 = random.randint(2, 99) # [2, 99]
        for factor in integers:
            response = input("What is "+str(factor)+"*"+str(int2to99)+"? ").strip(". \t").upper()
            if not response or response == 'Q':
                response = ""
                break
            elif int(response) != (factor * int2to99):
                errors += 1
                print("No, it is", str(factor * int2to99))
            responses += 1

    return responses, errors, ""
