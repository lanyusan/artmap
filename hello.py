import say_hi
# hello.py

print('hello world')

names = ['Dave', 'Paula', 'Thomas']

a = names[2]
names.append('Alex')
print(names)

for name in names:
    print(name)

prices = {
    'GOOG': 490,
    'AAPL': 134,
    'IBM':91
}

print(prices)
print(prices['IBM'])
say_hi.say_hi('Jack')
