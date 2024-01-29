n = 100
a=0
b=0
c=0
d=0
for i in range(1, n + 1):
    if i % 3 == 0 and i % 5 == 0:
        a+=1
        print("FizzBuzz")
    elif i % 3 == 0:
        b+=1
        print("Fizz")
    elif i % 5 == 0:
        c+=1
        print("Buzz")
    else:
        d+=1
        print(i)
        
print(a)
print(b)
print(c)
print(d)