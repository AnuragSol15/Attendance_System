import re

# Input string
input_string = '[IM-2K24-70\tNAYRA VIJAYVARGIYA]'

# Regular expression to extract roll number and name (handling tab)
pattern = r'\[(IM-2K[A-Za-z0-9-]+)\s*(.*)\]'

# Check if the input string matches the regex
match = re.search(pattern, input_string)

if match:
    roll_number = match.group(1)  # Extract roll number
    name = match.group(2)  # Extract name
    print("Roll Number:", roll_number)
    print("Name:", name)
else:
    print("No match found")
    # Debugging: Show which characters are causing the mismatch
    print("Input String:", repr(input_string))  # Shows the string with special characters
    print("Regex Pattern:", pattern)
    
    # Check each character in the input string and print any that don't match the regex
    for i, char in enumerate(input_string):
        if not re.match(pattern, input_string[i:]):
            print(f"Mismatch at position {i}: {repr(char)}")
