marks = {
    "Abdullah Javed" : 85,
    "Abdullah Omer" : 75,
    "Abdullah Khan" : 85
}

print(marks)
print(marks["Abdullah Javed"])
print(marks.items())
print(marks.keys())
print(marks.values())
marks.update({"Abdullah Javed" :87, "Abdullah Rashid" : 99, })
print(marks)
print(marks.get("Abdullah Omer"))
print(marks["Abdullah Omer"])

print(marks.get("Abdullah Omer2")) # Prints None
print(marks["Abdullah Omer2"]) # Prints Error