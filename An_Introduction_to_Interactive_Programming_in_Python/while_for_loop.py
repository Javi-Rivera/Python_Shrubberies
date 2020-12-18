n = 1000

numbers = range(2, n)
results = []

print len(numbers)

while len(numbers) >= 0:

    results.append(numbers[0])

    for i in numbers:

        if i % results[-1] == 0:

            numbers.pop(numbers.index(i))

    print results, len(numbers), len(results)
    
    if len(numbers) == 0:
        
        break