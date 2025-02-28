question_list = {
    1: [
        ("Write a Python program that prints 'Hello, World!' exactly as shown. Your program should produce the correct output when executed.", 
        "print('Hello, World!')")
    ],

    2: [
        ("Write a Python program that checks if the variable `num` (set to 3) is positive; print 'Positive' if true, otherwise print 'Negative'.", 
        "num = 3\nif num > 0:\n    print('Positive')\nelse:\n    print('Negative')")
    ],

    3: [
        ("Write a Python program that prints numbers from 1 to 10, one per line. Ensure that your output exactly matches the expected sequence.", 
         "for i in range(1, 11):\n    print(i)")
    ],

    4: [
        ("Write a Python function named 'sum' that takes two numbers as input and returns their sum. The function should work as follows: print(sum_numbers(3, 7)) should output '10'.", 
         "def sum(a, b):\n    return a + b")
    ],

    5: [
        ("Write a Python program that prints numbers from 1 to 100, replacing multiples of 3 with 'Fizz', multiples of 5 with 'Buzz', and multiples of both 3 and 5 with 'FizzBuzz'. Your output must exactly match the expected sequence.", 
         "for i in range(1, 101):\n    if i % 3 == 0 and i % 5 == 0:\n        print('FizzBuzz')\n    elif i % 3 == 0:\n        print('Fizz')\n    elif i % 5 == 0:\n        print('Buzz')\n    else:\n        print(i)")
    ]
}


"""
# reference
questions = {
    1: [
        ("1+1?", "2"),
        ("1+2?", "3"),
        ("Write a Python program that prints 'Hello world' using a print statement.", "print('Hello world')")
    ],
    2: [
        ("2+1?", "3"),
        ("2+2?", "4"),
        ("2+3?", "5")
    ],
    3: [
        ("3+1?", "4"),
        ("3+2?", "5"),
        ("3+3?", "6")
    ]
}

"""