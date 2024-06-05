romans : list= {
    'I' : 1,
    'V' : 5,
    'X' : 10,
    'L' : 50,
    'C': 100,
    'D' : 500,
    'M' : 1000
}

def return_integer_from_roman(roman_string):

    result = 0
    for i in range(len(roman_string)):
        
        
        if i == len(roman_string) -1:
            result += romans[roman_string[i]]
            
            return result
        
        if romans[roman_string[i]] < romans[roman_string[i + 1]]:
            result -= romans[roman_string[i]]
        else:
            result += romans[roman_string[i]]
            
    return result

a = return_integer_from_roman('VC')

print(a)