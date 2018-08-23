import ModelCalculations
import math

def binarySolver(equation, annualRate, segments):
    min = annualRate / segments
    max = annualRate
    guess = (max - min) / 2.0 + min
    computed = eval(equation.format(guess), None, None)
    while abs(computed - annualRate) > .00001:
        print "min: " + str(min)
        print "max: " + str(max)
        print "guess: " + str(guess)
        print round(computed, 20)
        computed = eval(equation.format(guess), None, None)

        if guess == max or guess == min:
            raise ValueError("Invalid Range with Max = {}, Min = {}, Guess = {}".format(max, min, guess))
        elif computed > annualRate:
            max = guess
        else:
            min = guess
        guess = (max - min) / 2.0 + min

    return round(guess, 6)

a = ModelCalculations.ModelCalculations()
#print binarySolver("2.0 * {0} ** 1 + -1.0 * {0} ** 2", .5)

#print binarySolver(a._buildEquation(200), 0.4, 200)
print "NEW BEGINNING"
print binarySolver(a._buildEquation(4), .6, 4)
print "NEW BEGINNING"
#print binarySolver(a._buildEquation(600), 0.4, 600)
'''
for i in range(1, 11):
    list = []
    for j in range(1, 11):
        list.append(binarySolver(a._buildEquation(j), i / 10.0, j))
        list.append(i / 10.0 / j > list[-1])
    print "Percentage: {} {}".format(i / 10.0, list)
'''

alist = []
for i in range(1, 11):
    print i / 10.0
    alist.append(binarySolver(a._buildEquation(2), i / 10.0, 2))
print alist