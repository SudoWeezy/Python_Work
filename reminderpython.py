# How to print something
# print("this line will be printed.")

# How to create variable or types
myint = 7

myfloat = 7.0
myfloat = float(7)

mystring = 'hello'
mystring = "hello"
# Better to use "" instead of '' for the
myapostropheexemple = "'"
# print(myapostropheexemple)

# +  -
one = 1
two = 2
three = 1 + 2
# print(three)

# string concat
hello = "hello"
world = "world"
helloworld = hello + " " + world
# print(helloworld)

# multiple declaration
a, b, c = 1, 2, "lol"
# print(a,b,c)

# List table
mylist = []
mylist.append(1)
mylist.append("lol")

# print(mylist)
# use for when we don't know the size
for x in mylist:
    printx = "print(x)"
    # print(x)
#use while when we set up the size
numbers = []
i = 1
while i < 4:
    numbers.append(i)
    i += 1
# pow
squared = 7 ** 2
# print(squared)

# Duplicate word
tenhello = "Hello" * 10
# print(tenhello)
# duplicate list
# print(mylist * 3)

# String formating
name = "John"
# print("Hello, %s" % name)
age = 23
# print("%s is %d years old." % (name, age))

# Everything can be print with %s

# print("Alist: %s" % mylist)

# %s - String (or any object with a string representation, like numbers)
#
# %d - Integers
#
# %f - Floating point numbers
#
# %.<number of digits>f - Floating point numbers with a fixed amount of digits to the right of the dot.
#
# %x/%X - Integers in hex representation (lowercase/uppercase)

data = ("John", "Doe", 53.44)
format_string = "Hello %s %s. Your current balance is $%s."

# print(format_string % data)
astring = "Hello world!"
# length string
# print(len(astring))

# first letter index
# print(astring.index("o"))

# Count letters
# print(astring.count("l"))

# print(astring[0:12])
# reverse string or list

# uper lowercase

# print(astring.upper())
# print(astring.lower())

# print(astring[::-1])
# detect start or end
# print(astring.startswith("Hello"))
# print(astring.endswith("asdfasdfasdf"))
# function
def my_function():
    print("Hello From My Function!")

# print(a simple greeting)
# my_function()

#class
# define the Vehicle class
class Vehicle:
    def __init__(self, name ="", kind="", color="", value=0):
        self.name = name
        self.kind = kind
        self.color = color
        self.value = value
    def description(self):
        desc_str = "%s is a %s %s worth $%.2f." % (self.name, self.color, self.kind, self.value)
        return desc_str
# your code goes here
car1 = Vehicle("Fer", "convertible", "red", 60000.00)
car2 = Vehicle()
# test code
# print(car1.description())
# print(car2.description())

# dictionnary
phonebook = {
    "John" : 938477566,
    "Jack" : 938377264,
    "Jill" : 947662781
}

# write your code here
#add item
phonebook["Jake"] = 938273443
# remove item
phonebook.pop("Jill")
 # import module
 # python -m pip install numpy
import re
mylist = dir(re)

# for x in mylist:
#     if "find" in x:
#         print(x)

# numpy
import numpy as np
height = [1.87,  1.87, 1.82, 1.91, 1.90, 1.85]
weight = [81.65, 97.52, 95.25, 92.98, 86.18, 88.45]

np_height = np.array(height)
np_weight = np.array(weight)
bmi = np_weight / np_height ** 2

# panda
dict = {"country": ["Brazil", "Russia", "India", "China", "South Africa"],
       "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria"],
       "area": [8.516, 17.10, 3.286, 9.597, 1.221],
       "population": [200.4, 143.5, 1252, 1357, 52.98] }

import pandas as pd
brics = pd.DataFrame(dict)
print(brics)
# generator

# fill in this function

def fib():
    a, b = 1, 1
    while 1:
        yield a
        a, b = a + b, a



# testing code
import types
if type(fib()) == types.GeneratorType:
    print("Good, The fib function is a generator.")

    counter = 0
    for n in fib():
        print(n)
        counter += 1
        if counter == 10:
            break

# comprehension
numbers = [34.6, -203.4, 44.9, 68.3, -12.2, 44.6, 12.7]
newlist = [x for x in numbers if x > 0]
# print(newlist)

# multifunction astring# edit the functions prototype and implementation
def foo(a, b, c, *args):
    return len(args)

def bar(a, b, c, **kwargs):
    return kwargs["magicnumber"] == 7

# exception
actor = {"name": "John Cleese", "rank": "awesome"}

#Function to modify, should return the last name of the actor - think back to previous lessons for how to get it
def get_last_name():
    try:
        return actor["name"].split()[-1]
    except KeyError:
        pass

#Test code
get_last_name()
# print("All exceptions caught! Good job!")
# print("The actor's last name is %s" % get_last_name())


# Sets
a = set(["Jake", "John", "Eric"])
b = set(["John", "Jill"])

# print(a.intersection(b))
# print(a.symmetric_difference(b)) #a contain b don't and b contain a don't
# print(a.difference(b)) #a contain b don't
# print(a.union(b))
#json
import json

# fix this function, so it adds the given name
# and salary pair to salaries_json, and return it
def add_employee(salaries_json, name, salary):
    # Add your code here
    salaries = json.loads(salaries_json)
    salaries[name] = salary
    return json.dumps(salaries)

# test code
salaries = '{"Alfred" : 300, "Jane" : 400 }'
new_salaries = add_employee(salaries, "Me", 800)
decoded_salaries = json.loads(new_salaries)
# print(decoded_salaries["Alfred"])
# print(decoded_salaries["Jane"])
# print(decoded_salaries["Me"])

#partial
from functools import partial
def func(u,v,w,x):
    return u*4 + v*3 + w*2 + x

p = partial(func,5,6,7)
# print(p(8))


class Vehicle:
    name = ""
    kind = "car"
    color = ""
    value = 100.00
    def description(self):
        desc_str = "%s is a %s %s worth $%.2f." % (self.name, self.color, self.kind, self.value)
        return desc_str

# Print a list of all attributes of the Vehicle class.
# print(dir(Vehicle))

#closure
def multiplier_of(n):
    def multiplier(number):
        return number*n
    return multiplier

multiplywith5 = multiplier_of(5)
# print(multiplywith5(9))
