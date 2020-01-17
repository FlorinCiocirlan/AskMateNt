import csv

# This function takes a csv as argument
# It returns a dict

def read_from_csv(file):
    with open(file, newline=" ") as csv_data:
        reader = csv.DictReader(csv_data)
    return reader

# This function takes a csv and a list as arguments:(file = csv file, fieldnames = list)
# Doesn't return anything

def write_to_csv(file, fieldnames):
    with open(file, "w", newline=" ") as csv_data:
        writer = csv.writer(csv_data, fieldnames=fieldnames)

# This function appends to a csv file
# It takes a csv and a list as arguments:(file = csv file, fieldnames = list)
# Doesn't return anything

def append_to_csv(file, fieldnames):
    with open(file, "a", newline=" ") as csv_data:
        writer = csv.writer(csv_data, fieldnames=fieldnames)