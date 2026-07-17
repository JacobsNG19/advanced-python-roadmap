# ―――――――――――――――――――――――――――――――――
# Set 1
#――――――――――――――――――――――――――――――――――


# 1


# number = 0
# list_of_numbers = []

# user = int(input("Enter a number: ").strip())
# list_of_numbers.append(user)
# number += 1

# while True:

    # choice = input("Want to continue yes or not: ").strip().lower()

#     if choice in ("yes", "y"):
#         user = int(input("Enter a number: ").strip())
#         list_of_numbers.append(user)
#         number += 1

#     elif choice in ("not", "n"):
#         break

#     else:
#         print("Please, entere a needed decision")
#         choice = input("Want to continue yes or not: ").strip().lower()

#         if choice in ("yes", "y"):
#             user = int(input("Enter a number: ").strip())
#             list_of_numbers.append(user)
#             number += 1

#         elif choice in ("not", "n"):
#             break

# print(f"The total amount of number entered: {number}")
# print(f"The sum of those number: {sum(list_of_numbers)}")
# print(f"The largest number: {max(list_of_numbers)}")
# print(f"The smallest number: {min(list_of_numbers)}")




# 2


# repeat = [1, 1, 1, 1]
# once = []
# last = 1

# for i in repeat:
#     once.append((i*last)*10)
#     last = once[-1]

# print(once)



# 3


# numbers = [1, 2, 3, 4]
# numbers_inh = []
# for i in numbers[::-1]:
#     numbers_inh.append(i)

# print(numbers)
# print(numbers_inh)



# 4


# sentence = "H eH".split() # I did not put .lower() because the question says "ignore uppercase and lowercase letters.""
# word =''

# for i in sentence:
#     word = i[::-1] + word

# sentence = ''.join(sentence)
# print(word)
# print(sentence)

# if word == sentence:
#     print(f"it can be read the same forward and backward")
#     print(sentence[::-1])
# if word != sentence:
#     print(f"it cannot be read the same forward and backward")




# 5  


# positive = [1, 2, 3, 4, 5]
# positive_reverse = positive[::-1]
# print(positive)
# print(positive_reverse)




# ―――――――――――――――――――――――――――――――――
# Set 2
#――――――――――――――――――――――――――――――――――


# 6


def find_value(collection, n):

    if len(collection) == 0:
        print("Value does not exist in the collection.")
        return "Value does not exist in the collection."
    
    first = collection[0]
    rest = collection[1:]
    if first == n:
        print("Value exists in the collection.")
        return n
    
    if first != n:
        find_value(rest, n)
    
# collection = [1, 12, 23, 34, 45, 56, 67, 78, 89, 90, 110]
# find_value(collection, 23)



# 7


# information_of_americans = {
#     "Joe" : [35, "New york"],
#     "Jones" : [27, "California"],
#     "Jonas" : [29, "Texas"],
#     "Jack" : [28, "Chicago"]
# }

# search_name = input("Enter a name: ").strip().title()

# for k,v in information_of_americans.items():
#     if search_name == k:
#         print(f'\nName: {k}\nAge: {v[0]}\nCity: {v[1]}')
#     if search_name != k:
#         print("The name entered does not exist in the list.")
#         print("Sorry 😢")




# 8


# x = 64
# number = 0
# list = []
# lists = []

# for i in range(x):

#     i += 1
#     result = x//i

#     if result*i == x:
#         print(f"{x}/{i} = {result}")
#         list.append(i)
#         lists.append(result)
#         number += 1

#     if result*i != x:
#         continue
    
# print(list)
# print(lists)

def pair(list, lists):
    if len(list) == 0 and len(lists) == 0:
        return
    
    first = list[0]
    rest = list[1:]
    firsts = lists[0]
    rests = lists[1:]

    if first*firsts == x:
        print(f"[{first}, {firsts}] By multipling these numbers, they produce {x}")
    return pair(rest, rests)
    
# pair(list, lists)



# 9


# new_collection = [] 
def largest_element(collection):

    if len(collection) == 0:
        return 
    first = collection[0]
    rest = collection[1:]

    if isinstance(first, int) or isinstance(first, float):
        largest_element(rest)

    new_collection.append(first)
    return max(new_collection)

# collection = [12, 56, 1, 67, 78, 34, 89, 110, 90, 45, 23]
# print(largest_element(collection))



# 10 


def change_grade(p_scores, name, attempts=0):
    print(f"Hello, {name}.")
    for year, grade in p_scores.items():

        print("\n--- Select an action ---")
        print("1. Change grade.")
        print("2. Add information.")
        print("3. Exit")

        choice = input("Enter a choice: ").strip().lower()   
            
        if choice == ('1', 'change grade'):
            select = int(input("select the year: ").strip())
            if select in p_scores.keys():
                year = next((year for year, grade in p_scores.items() if year == select), "Not found!")
                print(year)
                print(f"Current grade: {p_scores[year]}")
                new_grade = input("Enter a new grade: ").strip().title()
                p_scores[year] = new_grade
                return change_grade(p_scores, name, attempts+1)
                
        elif choice == '2' or choice == 'add information':
            try:
                add_year = int(input("Enter a new year: ").strip())
            except ValueError:
                print("Please, enter a number!")
                continue
            add_grade = input("Enter a grade: ").strip().title()

            if add_grade != "A+" or add_grade != "A" or add_grade != "B+" or add_grade != "B":
                print("Sorry the grade is too low!")

            else:
                continue
            year = add_year
            p_scores[year] = add_grade
            return change_grade(p_scores, name, attempts+1)

        elif choice == '3' or choice == 'exit':
            return p_scores
        else:
            return change_grade(p_scores, name, attempts+1)

# student_grade = {2026:"A+", 2025:"A+", 2024: "B+", 2023:"A", 2022: "A+", 2021: "A", 2020: "A"}
# student_name = 'James'
# change_grade(student_grade, student_name)
# print(student_grade)




# ―――――――――――――――――――――――――――――――――
# Set 3
#――――――――――――――――――――――――――――――――――


# 11


def contain_in(collection, n=0):
    if len(collection) == 0:
        return
    
    first = collection[0]
    rest = collection[1:]

    # print(f"This is the rest: {rest}")
    # print(f"This is the list for collection: {collection[:]}")
    # print(f"This is the particular: {particular}")
    if first in particular and first in particular[0:-1:2]:
        # print(f"This item is already: {first}")
        # print(particular)
        # print(f"✅✅✅✅✅✅✅ {particular[0:-1:2]}")
        def already(particular, n=0):

            if len(particular) == 0:
                return 

            first_in = particular[0]
            rest_in = particular[1:]

            if first_in == first:
                if first == 1:
                    return n*2
                else:
                    return n
        
            if first_in != first:
                return already(rest_in, n+1) 
        
        already(particular[0:-1:2])
        # print("#####", already(particular))
        # print(particular[already(particular)])
        particular[(already(particular))+1] += 1
        # print(f"1. {first} is {particular[(already(particular))+1]} times in the collection.")

    else:
        # print(f"Its first time: {first}")
        particular.append(first)
        particular.append(1)
        # print(particular)

    contain_in(rest, n+1)

    return particular

particular = []
collection = [12, 56, 110, 1, 67, 78, 34, 110, 23, 12, 89, 1, 110, 12, 67, 2, 90, 45, 23]
contain_in(collection)
# print(particular)

elements = particular[0:-1:2]
times = particular[1:-1:2]
times.append(particular[-1])

# print(elements)
# print(times)

def determine_time(elements, times, n=len(elements)):
    if len(elements) == 0:
        return 0
    first = elements[0]
    rest = elements[1:]
    first1 = times[0]
    rest1 = times[1:]

    if n != 0:
        print(f"{first} is {first1} time(s)")
        determine_time(rest, rest1, n-1)

# determine_time(elements, times)



# 12


def sctock_of_infos(blueprint):
    largest_values = []
    with_largest_value = []
    for k,v in blueprint.items():
        with_largest_value.append(k)
        largest_values.append(v)

    print(f"List of value: {with_largest_value}")
    print(f"List of value: {largest_values}")

    largest = max(largest_values)
    loop = 0

    largest = max(largest_values)
    loop = 0

    for i in largest_values:
        if i == largest:
            print(f"The key with largest value is {with_largest_value[loop]}")
        loop += 1
    return

# blueprint_of_my_house = {"Rooms": 5, "Living room": 2, "Kitchen": 2, "Veranda": 2, "WC": 5}
# sctock_of_infos(blueprint_of_my_house)



# 13


def sctock_of_infos(blueprint):
    largest_values = []
    with_largest_value = []
    for k,v in blueprint.items():
        largest_values.append(v)
        with_largest_value.append(k)
        
    largest = max(largest_values)
    loop = 0

    # print(largest_values)
    # print(with_largest_value)

    largest = max(largest_values)
    # print(largest)
    # largest = 2
    loop = 0
    
    check_key = []
    check_value = []

    for i in largest_values:
        if i == largest:
            print(f"The key with largest value is {with_largest_value[loop]}")
            check_key.append(with_largest_value)
            check_value.append(largest_values)
        loop += 1

    return check_key and check_value

# blueprint_of_my_house = {"Rooms": 5, "Living room": 2, "Kitchen": 2, "Rooms": 5,"Veranda": 2, "WC": 5}
# sctock_of_infos(blueprint_of_my_house)
# print(sctock_of_infos(blueprint_of_my_house))



# 14


def search_cube(number, epsilon=0.01, increment=0.001, guess=0):
    while abs(guess**3-number) >= epsilon:
        guess += increment
    return guess

# print(f'The cube is close to {search_cube(23)}')



# 15


def take_action(users_information):
    attempts = 3
    for i in range(attempts):
        try:
            password_input = int(input("Enter your password: ").strip())
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            continue

        # Find the user associated with the password
        current_user_name = None
        for name, data in users_information.items():
            if data[2] == password_input:
                current_user_name = name
                break
        
        if current_user_name:
            user_data = users_information[current_user_name]
            print(f"\nHello, {current_user_name}")
            
            while True:
                print("\nWhat action do you want to take?")
                print("1. Check my infos")
                print("2. Change my infos")
                print("3. Exit")
                action = input("Enter the number of an action: ").strip()

                if action == '1':
                    print(f"\n--- Your Information ---")
                    print(f"Name: {current_user_name}")
                    print(f"Age: {user_data[0]}")
                    print(f"City: {user_data[1]}")
                
                elif action == '2':
                    new_name = input(f"Enter your new name (current: {current_user_name}): ").strip()
                    try:
                        new_age = int(input(f"Enter your new age (current: {user_data[0]}): ").strip())
                    except ValueError:
                        print("Invalid age. Keeping current age.")
                        new_age = user_data[0]
                    
                    new_city = input(f"Enter your new city (current: {user_data[1]}): ")

                    # Update data
                    user_data[0] = new_age
                    user_data[1] = new_city
                    
                    # If name changed, we need to update the dictionary key
                    if new_name != current_user_name:
                        users_information[new_name] = users_information.pop(current_user_name)
                        current_user_name = new_name # Update reference for the next loop
                    
                    print("Information updated successfully!")

                    return users_information
                
                elif action == '3':
                    return users_information
                else:
                    print("Invalid action. Please try again.")
        else:
            remaining = attempts - 1 - i
            if remaining > 0:
                print(f"Password failed. {remaining} attempts left.")
            else:
                print("Limit of tests reached. Try later.")
    
    return users_information

if __name__ == "__main__":
    users_information = {
        "Joe" : [35, "New york", 1234],
        "Jones" : [27, "California", 7987],
        "Jonas" : [29, "Texas", 5634],
        "Jack" : [28, "Chicago", 2739]
    }
    
    # take_action(users_information)
    # print("\nFinal user data:")
    # print(users_information)



# ―――――――――――――――――――――――――――――――――
# Set 3
#――――――――――――――――――――――――――――――――――


# 16 


def data_exist(users_infos):
    attempts = 3
    for name, data in users_infos.items():
        names = list(users_infos.keys())
        data = list(users_infos.values())
        search_item = input("Enter a indice: ").strip().title()

        if search_item in names:
            name = next((name for name, data in users_infos.items() if name == search_item), "Not found")
            print(f"Hello, {search_item}")
            print(f"\n--- Your Information ---")
            print(f"Name: {search_item}")
            print(f"Age: {users_infos[name][0]}")
            print(f"City: {users_infos[name][1]}")
            print(f"Password: {users_infos[name][2]}")
            return users_infos
        
        for specific_data in data:

            if search_item.isdigit():
                search_item = int(search_item)
                name = next((name for name, data in users_infos.items() if search_item in users_infos[name]), "Not found")
                if name == "Not found":
                    pass
                else:
                    print(f"Hello, {name}")
                    print(f"\n--- Your Information ---")
                    print(f"Name: {name}")
                    print(f"Age: {users_infos[name][0]}")
                    print(f"City: {users_infos[name][1]}")
                    print(f"Password: {users_infos[name][2]}")
                    return 
            
            elif search_item in specific_data:
                name = next((name for name, data in users_infos.items() if search_item in users_infos[name]), "Not found")
                print(f"Hello, {name}")
                print(f"\n--- Your Information ---")
                print(f"Name: {name}")
                print(f"Age: {users_infos[name][0]}")
                print(f"City: {users_infos[name][1]}")
                print(f"Password: {users_infos[name][2]}")
                return 
        
        attempts -= 1
        if attempts == 0:
            break
        print("Indece does not macth with any user data.")
        print("Check the space(s).")
        print("Please try agin!")

    print("Not found!")

users_information = {
    "Joe" : [35, "New York", 1234],
    "Jones" : [27, "California", 7987],
    "Jonas" : [29, "Texas", 5634],
    "Jack" : [28, "Chicago", 2739]
}
# data_exist(users_information)



# 17


def check(division):
    count_of_distinct = []
    for number, response in division.items():
        if response in count_of_distinct:
            count_of_distinct.remove(response)
        else:
            count_of_distinct.append(response)
    print(count_of_distinct)
    print(f"Distinct value appears {len(count_of_distinct)} time(s).")
    
# divide_by_x_and_y = {16:4, 64:32, 32:8, 128:32, 8:4, 4:2}
# check(divide_by_x_and_y)



# 18


def main():
    name = greet(input("Enter a name: ").strip())

def greet(name):
    print(f"Hello, {name}.\nYou are in {area()}'s world.")

def area():
    return "AI"

# main()



# 19


def optimization():
    ...

    
weight = 73
size = 178 

# weight = int(input("Enter your weight: ").strip())
# size = int(input("Enter your size: ").strip())
# optimization(weight, size)



# 20


def take_action(users_information):
    attempts = 3
    for i in range(attempts):
        try:
            password_input = int(input("Enter your password: ").strip())
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            continue

        # Find the user associated with the password
        current_user_name = None
        for name, data in users_information.items():
            if data[2] == password_input:
                current_user_name = name
                break
        
        if current_user_name:
            user_data = users_information[current_user_name]
            print(f"\nHello, {current_user_name}")
            
            while True:
                print("\nWhat action do you want to take?")
                print("1. Check my infos")
                print("2. Change my infos")
                print("3. Exit")
                action = input("Enter the number of an action: ").strip()

                if action == '1':
                    print("What are you looking for?")
                    print("1. Name")
                    print("2. Age")
                    print("3. City")
                    print("4. password")
                    print("5. My data")
                    
                    choice = input("Enter a number of one info: ").strip()

                    if choice == '1':
                        print(f"Current name: {current_user_name}")
                    elif choice == '2':
                        print(f"Current age: {user_data[0]}")
                    elif choice == '3':
                        print(f"Current city: {user_data[1]}")
                    elif choice == '4':
                        print(f"Current password: {user_data[2]}")
                    elif choice == '5':
                        print(f"--- My data ---\nName: {current_user_name}\nAge: {user_data[0]}\nCity: {user_data[1]}\nPassword: {user_data[2]}")
                    else:
                        continue
                    # return users_information
                
                elif action == '2':
                    new_name = input(f"Enter your new name (current: {current_user_name}): ").strip().title()
                    try:
                        new_age = int(input(f"Enter your new age (current: {user_data[0]}): ").strip())
                    except ValueError:
                        print("Invalid age. Keeping current age.")
                        new_age = user_data[0]
                    
                    new_city = input(f"Enter your new city (current: {user_data[1]}): ").strip().title()

                    try:
                        new_password = int(input(f"Enter a new password (current: {user_data[2]}): ").strip())
                    except ValueError:
                        print("Invalid password. Keeping current password.")
                        new_password = userd_data[2]

                    # Update data
                    if '1' in new_name or  '2' in new_name or '3' in new_name or '4' in new_name or '5' in new_name or  '6' in new_name or '7' in new_name or  '8' in new_name or '9' in new_name or '0' in new_name:
                        new_name = current_user_name
                    else:
                        current_user_name = name
                    user_data[0] = new_age
                    user_data[1] = new_city
                    if len(str(new_password)) == 4 or new_password == 0000:
                        user_data[2] = new_password
                    
                    # If name changed, we need to update the dictionary key
                    if new_name != current_user_name:
                        users_information[new_name] = users_information.pop(current_user_name)
                        current_user_name = new_name # Update reference for the next loop

                    return print(f"--- Information updated successfully! ---\nName: {current_user_name}\nAge: {user_data[0]}\nCity: {user_data[1]}\nPassword: {user_data[2]}")

                elif action == '3':
                    return print(f"--- Information updated successfully! ---\nName: {new_name}\nAge: {new_age}\nCity: {new_city}")
                
                else:
                    print("Invalid action. Please try again.")
        else:
            remaining = attempts - 1 - i
            if remaining > 0:
                print(f"Password failed. {remaining} attempts left.")
            else:
                print("Limit of tests reached. Try later.")
    
    return users_information

if __name__ == "__main__":
    users_information = {
        "Joe" : [35, "New york", 1234],
        "Jones" : [27, "California", 7987],
        "Jonas" : [29, "Texas", 5634],
        "Jack" : [28, "Chicago", 2739]
    }
    
    # take_action(users_information)
    # print("\nFinal user data:")
    # print(users_information)



# ―――――――――――――――――――――――――――――――――
# Set 3
#――――――――――――――――――――――――――――――――――


# 21


list_of_values_of_dream = [[1, 2, 3], [6, 4, 5], [7, 8, 9]]
times = 4

def prediction(list, collection=0, attempts=1, age=0, first=0, second=0, third=0):

    room1 = []
    room2 = []
    room3 = []
    
    for room in list:
        room1.append(list[0])
        room2.append(list[1])
        room3.append(list[2])

    if attempts == 19:
        if collection == room1[0][0]:
            print(f"\n --- THE PREDICTION ---")
            print(f"\nA signle spark, though small, will soon light the darkened path you fear to walk.")
            print("The beginning is always quiet, but t holds the seed of everything to ome.")
        elif collection == room1[0][1]:
            print(f"\n --- THE PREDICTION ---")
            print(f"\nTwo choices lie ahead of you, but only one is truly witten in you stars.")
            print("Balance is not found by standing still, but by moving through the tilt.")
        elif collection == room1[0][2]:
            print(f"\n --- THE PREDICTION ---")
            print(f"\nA hidden strength is quietly growing just beneath the surface, waiting for its momment.")
            print("The kind time you look for an answer, the door will finally swing open.")
        return
    elif attempts == 29:
        if collection == room2[0][0]:
            print(f"\n --- THE PREDICTION ---")
            print(f"\nThe fierce strom you fear today carries the very wind you need to soar tommorow.")
            print("Stability is an illusion; real is learning how to dance in the wind.")
        elif collection == room2[0][1]:
            print(f"\n --- THE PREDICTION ---")
            print(f"\nYou must lose a familia shadow before you can finally discover your true shape.")
            print("A sudden detour is not a mistake, but the universe correcting your course.")
        elif collection == room2[0][2]:
            print(f"\n --- THE PREDICTION ---")
            print(f"\nAn unexpected mirror will appear, showing you the powerful soul you are steadily becoming.")
            print("Healing does not mean the damage never existed; it means it no longer controls you.")
        return

    elif attempts == 9:
        if collection in room1[0]:
            attempts = 20
            return prediction(list, collection, attempts-1, age, first, second, third)
        elif collection in room2[0]:
            attempts = 30
            return prediction(list, collection, attempts-1, age, first, second, third)
        elif collection in room3[0]:
            if collection == room3[0][0]:
                print(f"\n --- THE PREDICTION ---")
                print(f"\nA scared silence will soon speak much louder to you than any voice you have ever known.")
                print("You must walk through the quitest valley to hear the whispers of your truth.")
            elif collection == room3[0][1]:
                print(f"\n --- THE PREDICTION ---")
                print(f"\nWhat you willingly surrender in this moment will ultimately return to you as your crown.")
                print("The cycle of pain ends the moment you choose to forgive what you cannot forget.")
            elif collection == room3[0][2]:
                print(f"\n --- THE PREDICTION ---")
                print(f"\nYou are living, breathing answer to a profond question asked by the sosmos long ago.")
                print("Your longest journey ends right where you started, but you will finally see it for the first time.")
                return
    elif attempts == 0:
        return print(f"\nSomething went wrong.\nWant to continue?\nRestart the program.\nThank you.")

    elif attempts == 39:
        if age > 29:
            age = 29
            print("Let assume.")
            print(f"Age: {age}")
        elif age < 1:
            age = 1
            print("Let assume.")
            print(f"Age: {age}")

        if len(str(first)) == 1 and len(str(second)) == 2 and len(str(third)) == 2:
            # update
            age = str(age)
            second = str(second)
            third = str(third)

            collection = int(age[0]) + first * int(second[0]) + int(third[0])

            if len(str(collection)) == 2:
                collection = str(collection)
                collection = int(str(collection[0])) + int(str(collection[1]))
                attempts = 10
                return prediction(list, collection, attempts-1, age, first, second, third)
            else:
                attempts = 10
                return prediction(list, collection, attempts-1, age, first, second, third)
    
    elif attempts == 1:
        print("Welcome Dear!")
        print("Here, we predict the future with based:")
        print(f"\nAge(1-29)\nAnd Three Scores")
        print("Thank you to join our world.")
        print("Let begin the process.")
        try:
            age = int(input("Enter your age: ").strip())
            first = int(input("Enter your first score (0-9): ").strip())
            second = int(input("Enter your second score(10-19): ").strip())
            third = int(input("Enter your third score(20-29): ").strip())
            attempts = 40
            return prediction(list, collection, attempts-1, age, first, second, third)
        except ValueError:
            print(f"\nElement(s) missed.")
            return prediction(list, collection, attempts-1, age, first, second, third)


# prediction(list_of_values_of_dream, times)



# 22


names = ['Joy', 'Jane', 'Jacqueline', 'Jaime']
towns = ['Boston', 'Los Angels', 'San Francisco', 'Denver']
combination = {None:None}

def combine(pseudos, cities, alliance):

    mix = []
    [mix.append(pseudo) for pseudo in pseudos]
    [mix.append(city) for city in cities]

    mix_sort = []
    position = len(pseudos)

    for item in mix:

        if position == 8:
            break

        mix_sort.append(mix[position-4])
        mix_sort.append(mix[position])

        position += 1
    
    mix_sort.append(None)
    names = []
    
    for name, town in alliance.items():
        for item in mix_sort:
            if item in mix_sort[0:-1:2]:
                name = item
            if item in mix_sort[1:-1:2]:
                alliance[name] = item
            names.append(name)
        name = next((name for name, town in alliance.items() if name == None), "Not found!")
        del(alliance[name])
        del(name)
        return alliance

# print(combine(names, towns, combination))



# 23


def comparing(collection1, collection2):

    if len(collection1) == 0 and len(collection2) == 0:
        return print("The same!")
    
    
    elif len(collection1) == 0:
        return print("Not the same!")
    
    elif len(collection2) == 0:
        return print("Not the same!")
    
    first = collection1[0]
    first1 = collection2[0]
    rest = collection1[1:]
    rest1 = collection2[1:]

    if first != first1:
        return print("Not the same!")

    elif first == first1:
        return comparing(rest, rest1)
    
# c = [1, 2, 3, 4, 5, 6]
# c1 = [1, 2, 'three', 4, 5, 6]
# comparing(c, c1)



# 24


def alg(number, increment=0.001):

    guess = 0
    time = 0

    while abs(guess**3 + guess - number) >= 0.01:
        guess += increment
        time += 1
    
    response = guess**3 + guess - number

    print(f"It took {time} times.")
    print(f"Response: {guess}")
    print(f"{guess}**3 + {guess}  - {number} = {response}")
    print(f"The response does not match ut it close to the exact answer.")
    print("Thank you!")

    return guess


# alg(int(input("Enter a number: ").strip()))



# 25


def manage(book):
    for film in book:
        while True:
            print(f"\nHello Dear.")
            print("Select an action.")
            print(f"\n1. Display all the films stored")
            print("2. add a film")
            print("3. Search a film")
            print("4. remove a film")
            print("5. Exit")

            choice = input("Enter the number of an action: ").strip()

            if choice == '1':
                print(f"\n--- List of films ---")
                
                print(f"\nName: {film["Name"]}")
                print(f"Genre: {film["Genre"]}")
                print(f"Time: {film["Time"]}")

                print(book)

            elif choice == '2':
                name = input("Enter the name: ").strip().title()
                genre = input("Enter the genre: ").strip().title()
                while True:
                    try:
                        time = int(input("Enter the time: ").strip())
                    except ValueError:
                        print("Invalid time!")
                        continue
                    break
                
                if '1' in genre or  '2' in genre or '3' in genre or '4' in genre or '5' in genre or  '6' in genre or '7' in genre or  '8' in genre or '9' in genre or '0' in genre:
                    film["Genre"] = None # I create this rule like it is becauese it's the rule I'd only like this program has. But you can improve or fix it your own, if you want to force the user to put a genre.
                else:
                    film["Genre"] = genre
                film["Name"] = name

                film["Time"] = time

            elif choice == '3':
                print(f"\nIf you do not know the name of the film.")
                print("Our program helps you.")
                print("With only one indice, you finf the film, you are looking for.")

                while True:

                    indice = input(f"\nEnter a Indice: ").strip().title()

                    if indice.isdigit():

                        list_of_indice = []

                        for film in book:

                            indice = int(indice)
                            if indice in [film["Name"], film["Genre"], film["Time"]]:
                                print(f"\n--- FILM(S) WITH INDICE {indice}")
                                print(f"\nName: {film["Name"]}")
                                print(f"Genre: {film["Genre"]}")
                                print(f"Time: {film["Time"]}")

                                list_of_indice.append(indice)                                

                        if len(list_of_indice) == 0:
                            print(f"There is not any film with indice {indice}")
                            print("Try again.")
                            continue

                        break
                        
                    elif indice in [film["Name"], film["Genre"], film["Time"]]:
                            
                        list_of_indice = []

                        for film in book:

                            if indice in [film["Name"], film["Genre"], film["Time"]]:
                                print(f"\n--- FILM(S) WITH INDICE {indice}")
                                print(f"\nName: {film["Name"]}")
                                print(f"Genre: {film["Genre"]}")
                                print(f"Time: {film["Time"]}")

                        if len(list_of_indice) == 0:
                            print(f"There is not any film with indice {indice}")
                            print("Try again.")
                            continue

                        break
                    
                    else:
                        list_of_indice = []

                        for film in book:

                            if indice in [film["Name"], film["Genre"], film["Time"]]:
                                print(f"\n--- FILM(S) WITH INDICE {indice}")
                                print(f"\nName: {film["Name"]}")
                                print(f"Genre: {film["Genre"]}")
                                print(f"Time: {film["Time"]}")

                                list_of_indice.append(indice)


                        if len(list_of_indice) == 0:
                            print(f"There is not any film with indice {indice}")
                            print("Try again.")
                            continue

            elif choice == '4':
                print(f"\nTo remove a film,")
                print(f"you must match all these steops:")
                print(f"\nWrite correctly its name,")
                print("Write correctly its genre,")
                print("Write correctly its time.")
                print("Let begin.")
                
                while True:
                    while True:
                        name = input(f"\nEnter the name: ").strip().title()
                        for film in book:
                            list_of_name = []
                            if name == film["Name"]:
                                list_of_name.append(name)
                                break
                        if len(list_of_name) == 0:
                            print("Invalid name.")
                            print("Try again.")
                            continue
                        if len(list_of_name) != 0:
                            break
                    
                    while True:
                        genre = input(f"\nEnter the genre: ").strip().title()
                        for film in book:
                            list_of_genre = []
                            if genre == film["Genre"]:
                                list_of_genre.append(genre)
                                break
                        if len(list_of_genre) == 0:
                            print("Invalid genre.")
                            print("Try again.")
                            continue
                        if len(list_of_genre) != 0:
                            break
                    
                    while True:
                        try:
                            time = int(input(f"\nEnter the genre: ").strip())
                        except ValueError:
                            print("Invalide time.")
                            print("Time must be a number.")
                        for film in book:
                            list_of_time = []
                            if time == film["Time"]:
                                list_of_time.append(time)
                                break
                        if len(list_of_time) == 0:
                            print("Invalid time.")
                            print("Try again.")
                            continue
                        if len(list_of_time) != 0:
                            break
                    
                    if name and genre and time:
                        film = next((film for film in book if name == film["Name"]), "Not found!")
                        del(film)
                        break


            elif choice == '5':
                return book

            else:
                print("Invalid action.")
                print("Please, enter a valid action.")
                continue
        

# book_of_films = [
#     {"Name": "Service", "Genre": "...", "Time": 128},
#     {"Name": "Construction", "Genre": "Action", "Time": 143},
#     {"Name": "Three Dimension", "Genre": "Action", "Time": 115},
#     {"Name": "Wisdom Supernatural", "Genre": "...", "Time": 107},
#     {"Name": "Intelligence(Behinde the eyes)", "Genre": "...", "Time": 139}
# ]

# manage(book_of_films)



# 26


def main(stock, attempts=287):

    if attempts == 287:
        name = get_name('Jacob')
        age = get_data('18', None, None)
        country = get_data(None, 'Congo', None)
        for time in range(4):
            try:
                print("The password must contain only 4 digits.")
                password = get_data(None, None, int(2876))
                break
            except ValueError:
                print(f"Invalid password.")
                print("Please, follow the instructions required.")
                print("Try again.")

        print(f"Name: {name}")
        print(f"Age: {age}")
        print(f"Country: {country}")
        print(f"Password: {password}")

        if None in stock:
            stock[name] = stock.pop(None)

        for pseudo, data in stock.items():
            stock[name].append(age)
            stock[name].append(country)
            stock[name].append(password)

        return print(stock)
        
    elif attempts == 286:
        print(f"\nPlease, enter correct age.")
        print("Try again.")
        age = get_data(input("Enter your age: ").strip(), None, None)
    
    elif attempts == 285:
        print(f"Please, enter an Africa country.")
        print("Try again.")
        country = get_data(None, input("Enter your country: ").strip(), None)

    elif attempts == 283:
        print("Invalide password.")
        print("Please, follow the instructions required.")
        print("Try again.")
        for time in range(4):
            try:
                print("The password must contain only 4 digits.")
                password = get_data(None, None, int(input("Enter a password: ").strip()))
                break
            except ValueError:
                print(f"Invalid password.")
                print("Please, follow the instructions required.")
                print("Try again.")

def get_name(name):
    if '1' in name or  '2' in name or '3' in name or '4' in name or '5' in name or  '6' in name or '7' in name or  '8' in name or '9' in name or '0' in name:
        return get_name(name)
    return name

def get_data(age, country, password, attempts=287):

    if isinstance(age, str): # Because it will only execute the body if the type of age is str, (we did it when we create age) but as we will change it saying 'return int(age)' after two line, the type of the age will no longer be str instead int and this condition will never match 1-1.
        if age.isdigit():
            return int(age)
        else:
            return main(stock, attempts-1)

    if country:
        if country not in ['Usa', 'Congo']:
            return main(stock, attempts-2)
        return country
    
    if password:
        if len(str(password)) != 4:
            return main(stock, attempts-4)
        else:
            return password

# stock = {
#     None: []
# }

# main(stock)



# 27


def transformation(before, after):
     
    key = []
    value = []

    for name, age in before.items():
        key.append(name)
        value.append(age)
    
    def cooperate(k, v, after):

        if len(k) == 0:
            return
        
        first = k[0]
        rest = k[1:]
        first1 = v[0]
        rest1 = v[1:]

        for name, age in after.items():
            name = first
            after[name] = first1

            if after:
                return cooperate(rest, rest1, after)

    cooperate(key, value, after)

    if None in after:
        after[name] = after.pop(None)

    for name, age in after.items(): 
        # Because the last name(key) does not have age(value)
        last_age = next((age for age in value if age == value[-1]), "Not found!")

        if after[name] == None:
            after[name] = last_age

        after[name] += 2

    return print(after)

# Age_In_2024 = {
#     "Jaime": 28,
#     "Jones": 27,
#     "Jill": 31,
#     "John": 31,
# }

# Age_In_2026 = {None: None}

# transformation(Age_In_2024, Age_In_2026)



# 28


def transformation(before, after):
     
    key = []
    value = []

    for name, age in before.items():
        key.append(name)
        value.append(age)
    
    def cooperate(k, v, after):

        if len(k) == 0:
            return
        
        first = k[0]
        rest = k[1:]
        first1 = v[0]
        rest1 = v[1:]

        for name, age in after.items():
            name = first
            after[name] = first1

            if after:
                return cooperate(rest, rest1, after)

    cooperate(key, value, after)

    if None in after:
        after[name] = after.pop(None)

    for name, age in after.items(): 
        # Because the last name(key) does not have age(value)
        last_age = next((age for age in value if age == value[-1]), "Not found!")

        if after[name] == None:
            after[name] = last_age

        after[name] += 2

    after = {name: age for name, age in after.items() if age < 30}

    return print(after)

# Age_In_2024 = {
#     "Jaime": 28,
#     "Jones": 27,
#     "Jill": 31,
#     "John": 31,
#     "Jackelline": 25,
#     "Jonas": 29,
#     "Jane": 23,
#     "Joy": 21,
#     "Joe": 35,
#     "Jack": 28,
# }

# Age_In_2026 = {None: None}

# transformation(Age_In_2024, Age_In_2026)



# 29


...