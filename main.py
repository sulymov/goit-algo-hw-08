from classes import *

# **************************ДЕКОРАТОР*********************************
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me the name and the phone please."
        except IndexError:
            return "Give me the name of the contact please."
        except KeyError:
            return "Give me the right name of the contact please."
    return inner

# **************************ФУНКЦІОНАЛ********************************
@input_error
def parse_input(user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def show_all(book: AddressBook):
    if book == None:
        return "There isn't any contact"
    else:
        return book

@input_error    
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    message = "This name isn't exists."
    if record:
        return book.find(name)
    else:
        return message 
    
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return "This contact isn't exists. Try to add it!"
    
@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = f"{name} birthday added."
    if record:
        if record.birthday == None:
            record.add_birthday(birthday)
            return message
        elif record.birthday != None:
            message = f"{name} birthday already exists."
    else:
        message = "Contact isn't exists."
        return message
    
@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        return f"{name} birthday is {record.birthday}"
    else:
        return f"Contact {name} isn't exists."
    
@input_error
def upcoming_birthdays(book: AddressBook):
    birthdays = book.get_upcoming_birthdays()
    if birthdays == []:
        return "There isn't any contact to congratulate"
    else:
        return "\n".join([f"{birthday["name"]} congratulation date is {birthday["birthday"]}" for birthday in birthdays])

    
# *************************ГОЛОВНА ФУНКЦІЯ***********************************
def main():
    # book = AddressBook()
    book = AddressBook.load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            AddressBook.save_data(book)
            break
        
        elif command == "hello":
            print("How can I help you?")
        
        elif command == "add":
            print(add_contact(args, book))
                               
        elif command == "change":
            print(change_contact(args, book))
        
        elif command == "phone":
            print(show_phone(args, book))
                    
        elif command == "all":
            print(show_all(book))
                    
        elif command == "add-birthday":
            print(add_birthday(args, book))
            
        elif command == "show-birthday":
            print(show_birthday(args, book))
            
        elif command == "birthdays":
            print(upcoming_birthdays(book))
                            
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
