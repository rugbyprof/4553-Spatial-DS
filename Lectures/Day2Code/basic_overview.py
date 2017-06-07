# print string to standard out
print("hello world")

# basic function to print argument to standard out
def printString(tstp):
  print(tstp)
  
# assign string to var
x = "print this to the screen"

# everything is an object, so running methods on a string is normal
y = "this is another string".join(x)

# show the data type of a variable
print(type(y))

# call our basic function from above
printString(y)

# python is ok with changing a string var to a float because
# of dynamic typing (duck typing)
x = 3.1456

# print our float to standard out
printString(x)

# prove the data type has changed for 'x'
print(type(x))

# lists in python are very important and
# can hold many different types at once
L = ["hello",'88',"Fred",3.14159]

# add item to end of list
L.append('45')

# add item to beginning of list
# first param in 'insert' is the index to place item
L.insert(0,78)


# Range returns a list of x items and
# the 'for i' iterates over that container.
# This loop appends ints 0-9 to end of list 'L'
for i in range(10):
  L.append(i)

# print nicely dumps entire list to standard out
print(L)

# prints 'last' item in list (bad way)
print(L[len(L)-1])

# prints 'last' item in list (better way)
print(L[-1])

# slices list and print items from 2 - 4
print(L[2:4])

# better way to use 'join' method and put 'colons' 
# between each value in our list
str1 = ':'.join(str(e) for e in L)

# print our 'concatenated' list to standard out
print(str1)

# somewhat reverse the 'join' from above
print(str1.split(":"))

# range method creates list of ints (or floats)
# first param = start val
# second param = end val (-1) (optional)
# third param = step val (optional)
for i in range(0,100,5):
  print(i)

# creates a 'tuple' of 4 and 8
# tuples are 'immutable' 
p = (4,8)

# overloads '=' operator to assign '4 to x' and '8 to y'
x,y = p

# prove above statment
print(x)
print(y)

# creates a dictionary 
inventory = {}

# add items to our 'dict'
inventory['apple'] = {'case':45,'box':23}
inventory['pear'] = [89]
inventory['orange'] = [33]
inventory['kiwi'] = [45]
inventory['lime'] = [2345]

# python prints 'dict' nicely to standard out
print(inventory)

# print a single item from dict
print(inventory['apple']['case'])

# proper way to loop through dict
# 'items()' returns a tuple = (key,val) 
for k,v in inventory.items():
  print(k,v)

# dictionaries are objects (wich have 'methods')
# 2 of those are '.values()' and '.keys()'. 
for v in inventory.values():
  print(v)

# function showing use of 'kwargs' or keyword arguments
def my_function(**kwargs):
    print(kwargs)
    
    if 'a' in kwargs:
      print(kwargs['a'])
      
    if not 'd' in kwargs:
      d = '99'
    else:
      d = kwargs['d']
      
    if 'c' in kwargs:
      print(kwargs['c'])
      
    print(d)

# calling above function sending 'keyword' args
my_function(a=12, b="abc",d='128')

# function showing 'positional' and 'named' arguments 
def foo(p1, p2, p3, n1=None, n2=None):
    print('[p1:%d p2:%d p3:%d]' % (p1, p2, p3))
    if n1 is not None:
        print('n1=%d' % n1)
    if n2:
        print('n2=%d' % n2)

# calling above function
foo(1, 2, 3, n2=99)
foo(1, 2, n1=42, p3=3)

# basic class syntax 
class Point(object):
  # constructor for our class
  def __init__(self,x=None,y=None):
    if x:
      self.x = x
    if y:
      self.y = y
  
  # overload print method to print this 
  def __str__(self):
    return "(%s,%s)" % (str(self.x),str(self.y))
  
  # add our own class method to 'shift' a point
  def shift(self,deltax,deltay):
    self.x += deltax
    self.y += deltay
    
# create instance of a 'point'
p1 = Point(4,5)

# prints point nicely (because of the __str__ method)
print(p1)

# class the 'shift' method
p1.shift(-1,2)

# show our point has 'shifted'
print(p1)


