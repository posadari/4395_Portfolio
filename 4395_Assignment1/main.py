import sys  #to get the system parameter
import pathlib 
import re   #regex
import pickle

class Person:
    def __init__(self, last_name, first_name, middle_name, id, phone):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.phone = phone
        self.id = id
        
    def display(self):
        print("Employee ID:", self.id)
        print("\t", " ".join([self.first_name, self.middle_name, self.last_name]))
        print("\t", self.phone)

# read csv file
def read_file(filepath):
    with open(pathlib.Path.cwd().joinpath(filepath), 'r', encoding='utf-8-sig') as f:
        text_in = f.read().splitlines()
    return text_in

# fix full name
def check_names(person, index2, obj):
    if person and (index2 == 0 or index2 == 1): # capitalize first and last names if not null
        obj[index2] = person.capitalize()
    if index2 == 2: # capitalize middle initial
        if person:
            obj[index2] = person.upper()
        else:
            obj[index2] = 'X' # if person does not have middle initial, replace with 'X'

# fix id
def check_id(index2, person, obj):
    if index2 == 3: # check id
        isValid = False
        person_id = person
        while not isValid:
            id = re.search("[A-Z]{2}\d{4}$", person_id)
            if id:
                break
            else:
                print("ID invalid:", person)
                print("ID is two letters followed by 4 digits")
                person_id = input("Please enter a valid id: ")
        obj[index2] = person_id
      
# fix phone number  
def check_phone(person, index2, obj):
    if index2 == 4: 
        isValid = False
        phone = person
        while not isValid:
            number = re.search("^(1-)?\d{3}-\d{3}-\d{4}$", phone) # regex rule: 3 numbers - 3 numbers - 4 numbers
            if number:
                break
            else:
                print("Phone", phone, "is invalid")
                print("Enter phone number in form 123-456-7890")
                phone = input("Enter phone number: ")
        obj[index2] = phone

# change csv file data   
def modify_data(data):
    people = []
    for line in data[1:]: # skip the first line
        arr = line.split(',')
        people.append(arr)
    
    for index1, obj in enumerate(people):
        for index2, person in enumerate(obj):
            check_names(person, index2, obj) # check first and last names
            check_id(index2, person, obj)
            check_phone(person, index2, obj)
    return people

# create Person objects and dictionary, pickling
def create_person_objs(data):
    persons = {}
    for person in data:
        if person[3] in persons.keys():
            continue
        persons[person[3]] = Person(person[0], person[1], person[2], person[3], person[4]) # create new key and value pair
        
    pickle.dump(persons, open('employees.pickle','wb')) # seralize 
    employee_in = pickle.load(open('employees.pickle', 'rb')) # deserialize
    
    print("\nEmployee list:\n")
    for employee_id in employee_in.keys():
        employee_in[employee_id].display() 

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        data = read_file(fp)
        create_person_objs(modify_data(data))
        