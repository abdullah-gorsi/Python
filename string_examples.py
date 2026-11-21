name = "ABDULLAH"
nameshort = name[0:3] # This will extract the first three characters from the string "ABDULLAH"
print(nameshort) # Output: ABD

character = name[1]
print(character) # Output: B

# This will extract characters from index 1 to 9 with a step of 4
word = "abcefghijklmnopqrstuvwxyz"
word = word[1:9:4]
print(word)

# this will print the length of the string "ABDULLAH"
name = "ABDULLAH"
print(len(name)) # Output: 8
print(name.endswith("LAH")) # checks if the string ends with the specified suffix
print(name.startswith("ABD")) # checks if the string starts with the specified prefix
print(name.capitalize()) # capitalizes the first character

# THIS WILL PRINT A GREETING MESSAGE WITH THE USER'S NAME
name = input("Enter your Name : ")
print(f"Good Afternoon, {name}!")