import os

# Specify the directory path
directory = "."

# Get the contents of the directory
contents = os.listdir(directory)

# Print each file and folder
for item in contents:
    print(item)