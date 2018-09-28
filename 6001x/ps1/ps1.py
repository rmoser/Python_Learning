print("Please think of a number between 0 and 100!")
i = 'h'
h = 100
l = 0
g = 50

print("Is your secret number {}?".format(g))
i = input("Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. ")

while i != 'c':
    if not i in ['h', 'l', 'c']:
        print("Sorry, I did not understsand your input.")
    else:
        if i == 'c':
            break
        elif i == 'h':
            h = g
            g = (g + l) // 2
        elif i == 'l':
            l = g
            g = round(g + h) // 2

    print("Is your secret number {}?".format(g))
    i = input(
        "Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. ")

print("Game over. Your secret number was: {}".format(g))


