#Password Generator Project

import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

print("Welcome to the PyPassword Generator")
nr_letters= int(input("How many letters do you want?\n")) 
nr_symbols = int(input(f"How many symbols do you want?\n"))
nr_numbers = int(input(f"How many numbers do you want?\n"))

password_list = []

for char in range(1, nr_letters + 1):
  password_list += random.choice(letters)

for symbol in range(1, nr_symbols + 1):
  password_list += random.choice(symbols)

for num in range(1, nr_numbers + 1):
  password_list += random.choice(numbers)

random.shuffle(password_list)

password = ""
for char in password_list:
  password += char

print(f"Your new password is: {password}")
