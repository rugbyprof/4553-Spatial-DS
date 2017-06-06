```python
"""
Comments to come later....
"""
# print("hello world")

# def printString(tstp):
#   print(tstp)
  
  
# x = "print this to the screen"

# y = "this is another string".join(x)

# print(type(y))
# printString(y)

# x = 3.1456

# printString(x)

# print(type(x))


# L = ["hello",'88',"Fred",3.14159]

# L.append('45')
# L.append(78)

# #range returns a list of x items
# for i in range(10):
#   L.append(i)

# print(L)

# print(L[len(L)-1])

# print(L[2:4])

# str1 = ':'.join(str(e) for e in L)
# print(str1)
# print(str1.split(":"))

# for i in range(0,100,5):
#   print(i)
  
  
# p = (4,8)

# x,y = p

# print(x)
# print(y)


# inventory = {}

# inventory['apple'] = {'case':45,'box':23}
# inventory['pear'] = [89]
# inventory['orange'] = [33]
# inventory['kiwi'] = [45]
# inventory['lime'] = [2345]

# print(inventory)

# print(inventory['apple']['case'])

# for k,v in inventory.items():
#   print(k,v)

# for v in inventory.values():
#   print(v)
  


# def my_function(**kwargs):
#     print(kwargs)
    
#     if 'a' in kwargs:
#       print(kwargs['a'])
      
#     if not 'd' in kwargs:
#       d = '99'
#     else:
#       d = kwargs['d']
      
#     if 'c' in kwargs:
#       print(kwargs['c'])
      
#     print(d)

# my_function(a=12, b="abc",d='128')

# def foo(p1, p2, p3, n1=None, n2=None):
#     print('[p1:%d p2:%d p3:%d]' % (p1, p2, p3))
#     if n1 is not None:
#         print('n1=%d' % n1)
#     if n2:
#         print('n2=%d' % n2)

# foo(1, 2, 3, n2=99)

# foo(1, 2, n1=42, p3=3)


class Point(object):
  def __init__(self,x=None,y=None):
    if x:
      self.x = x
    if y:
      self.y = y
      
  def __str__(self):
    return "(%s,%s)" % (str(self.x),str(self.y))
  
  
  def shift(self,deltax,deltay):
    self.x += deltax
    self.y += deltay
    

p1 = Point(4,5)

print(p1)

p1.shift(-1,2)

print(p1)

```
