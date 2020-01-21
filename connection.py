import csv


# This function takes a csv as argument
# It returns a dict

def read_from_csv(file):
    with open(file, "r" , newline="") as csv_data:
        list_of_dict = []
        reader = list(csv.DictReader(csv_data))
        for row in reader:
            list_of_dict.append(row)
    return reversed(list_of_dict)


# This function takes a csv and a list as arguments:(file = csv file, fieldnames = list)
# Doesn't return anything

def write_to_csv(file):
    with open(file, "w", newline="") as csv_data:
        writer = csv.writer(csv_data)


# This function appends to a csv file
# It takes a csv and a list as arguments:(file = csv file, fieldnames = list)
# Doesn't return anything

def append_to_csv(file,fields):
    with open(file, "a", newline="") as csv_data:
        writer = csv.writer(csv_data)
        writer.writerow(fields)
