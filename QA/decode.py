input = "1989\ub144 2\uc6d4 15\uc77c"

input2 = input.encode(‘unicode-escape’).decode()

print(input)
print(input2)