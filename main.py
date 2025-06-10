from random import choice
from pathlib import Path
from classes import AddressBook, CastomError, Record, Birthday, SaveData
from typing import Callable, Any, Union
from abc import ABC, abstractmethod


# Abstract base class of the user interface
class UserInterface(ABC):

    @abstractmethod
    def add_contact(self, args: list[str], contacts: AddressBook) -> str:
        pass

    @abstractmethod
    def change_contact(self, args: list[str], book: AddressBook) -> str:
        pass

    @abstractmethod
    def show_phone(self, args: list[str], contacts: AddressBook) -> str:
        pass

    @abstractmethod
    def show_all(self, book: AddressBook) -> str:
        pass

    @abstractmethod
    def add_birthday(self, args: list[str], book: AddressBook) -> str:
        pass

    @abstractmethod
    def show_birthday(self, args: list[str], book: AddressBook) -> Birthday:
        pass

    @abstractmethod
    def birthdays(self, book: AddressBook) -> str:
        pass

    @abstractmethod
    def show_help(self) -> str:
        pass


# Decorator for handling errors
def input_error(func: Callable[..., Any]) -> Callable[..., Any]:
    def inner(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return e
        except FileNotFoundError:
            return "How can I help you?"
        except CastomError as e:
            return e

    return inner


# The function of parsing a user-entered string into a command and its arguments.
@input_error
def parse_input(user_input: str) -> tuple[str, *tuple[str, ...]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# #Функція лолавання контакту Команда: "add John 1234567890"
# @input_error
# def add_contact(args:list[str], contacts:AddressBook) -> str:
#     try:
#         name, phone, *_ = args
#     except ValueError:
#         return f"Give me correct name and phone please."
#     name=name.lower().capitalize()
#     record = contacts.find(name)
#     message = "Contact updated."
#     if record is None:
#         record = Record(name)
#         contacts.add_record(record)
#         message = "Contact added."
#     if phone:
#         record.add_phone(phone)
#     return message

# #Функція зміни контакту  Команда: "change John 0987654321"
# @input_error
# def change_contact(args:list[str], book:AddressBook) -> str:
#     try:
#         name, old_phone, new_phone = args
#     except ValueError:
#         return f'"Uncnown command\nchange <name> <old_phone_namer> <new_phone_namer>" - change the phone number in the address book'
#     if name.lower().capitalize() not in book.keys():
#         massage = 'Contact is missing, please add it (add <name> <phone_namer>)! '
#     else:
#         book[name.lower().capitalize()].edit_phone(old_phone, new_phone)
#         massage = 'Contact updated.'
#     return massage

# #Функція показати контакт Команда: "phone John"
# def show_phone(args:list[str], contacts:AddressBook) -> str:
#     name = args[0].lower().capitalize()
#     return contacts.get(name, 'The name is missing')

# #Функція виведення всієї адресної книги Команда: "all"
# def show_all(book:AddressBook) -> str:

#     return '\n'.join(f"{key} => {value}" for key, value in book.items())


# Function for select a random phrase to answer hello
@input_error
def get_random_phrase() -> str:
    current_dir = Path(__file__).parent
    with open(current_dir / "hello.txt", "r", encoding="utf-8") as file:
        phrase = file.readlines()
        return choice(phrase).strip()


# #функція для додавання дати народження. Команда add-birthday <name> <DD.MM.YYYY>
# @input_error
# def add_birthday(args: list[str], book: AddressBook) -> str:
#     try:
#         name, birthday, *_ = args
#     except ValueError:
#         return f"Give me name and birthday."
#     name=name.lower().capitalize()
#     record = book.find(name)
#     message = "Contact updated."
#     if record is None:
#         record = Record(name)
#         book.add_record(record)
#         message = "Contact added."
#     if birthday:
#         record.add_birthday(birthday)
#     return message

# #функція для виводу дати народження для вказаного контакту. Команда show-birthday <name>
# @input_error
# def show_birthday(args: list[str], book: AddressBook) -> Birthday:
#     name = args[0].lower().capitalize()
#     result=book.get(name, None)
#     if result != None:
#         if result.birthday != None:
#             return result.birthday
#         else:
#             raise CastomError("Дата відсутня")
#     else:
#         raise CastomError("Контакт відсутній")

# #функціядля виводу дати привітання працівників на найближчий тиждень. Команда birthdays
# @input_error
# def birthdays(book: AddressBook) -> str:
#     results=book.get_upcoming_birthdays()
#     if results:
#         return str(results)
#     else:
#         return f'No birthdays for display'

# def show_help() -> str:
#     help_message="""The bot helps to work with the contact book.
#                             Commands and functions:
#                             "close" | "exit" - exit the program
#                             "hello" - display a greeting
#                             "add <name> <phone_namer>" - add a phone number to the address book
#                             "change <name> <old_phone_namer> <new_phone_namer>" - change the phone number in the address book
#                             "add-birthday <name> <DD.MM.YYYY>" - add a birthday to the address book
#                             "show-birthday <name>" - show birthday
#                             "phone <name>" - show the number
#                             "all" - show the entire address book
#                             "birthdays" - show date for congratulation
#                             "help" | "?" - show this help"""
#     return help_message


# Implementation of the console interface
class ConsoleInterface(UserInterface):
    # The function of adding a contact. Command: "add John 1234567890"
    @input_error
    def add_contact(self, args: list[str], contacts: AddressBook) -> str:
        try:
            name, phone, *_ = args
        except ValueError:
            return f"Give me correct name and phone please."
        name = name.lower().capitalize()
        record = contacts.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            contacts.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        return message

    # Change contact function. Command: "change John 0987654321"
    @input_error
    def change_contact(self, args: list[str], book: AddressBook) -> str:
        try:
            name, old_phone, new_phone = args
        except ValueError:
            return f'"Uncnown command\nchange <name> <old_phone_namer> <new_phone_namer>" - change the phone number in the address book'
        if name.lower().capitalize() not in book.keys():
            massage = "Contact is missing, please add it (add <name> <phone_namer>)! "
        else:
            book[name.lower().capitalize()].edit_phone(old_phone, new_phone)
            massage = "Contact updated."
        return massage

    # Show contact function. Command: "phone John"
    def show_phone(self, args: list[str], contacts: AddressBook) -> str:
        name = args[0].lower().capitalize()
        return contacts.get(name, "The name is missing")

    # Function to display the entire address book. Command: "all"
    def show_all(self, book: AddressBook) -> str:

        return "\n".join(f"{key} => {value}" for key, value in book.items())

    # Function to add date of birth. Command: "add-birthday <name> <DD.MM.YYYY>""
    @input_error
    def add_birthday(self, args: list[str], book: AddressBook) -> str:
        try:
            name, birthday, *_ = args
        except ValueError:
            return f"Give me name and birthday."
        name = name.lower().capitalize()
        record = book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            book.add_record(record)
            message = "Contact added."
        if birthday:
            record.add_birthday(birthday)
        return message

    # Function to display the date of birth for the specified contact. Command: show-birthday <name>
    @input_error
    def show_birthday(self, args: list[str], book: AddressBook) -> Birthday:
        name = args[0].lower().capitalize()
        result = book.get(name, None)
        if result != None:
            if result.birthday != None:
                return result.birthday
            else:
                raise CastomError("Дата відсутня")
        else:
            raise CastomError("Контакт відсутній")

    # Function for displaying the date of employee congratulations for the next week. Command: birthdays
    @input_error
    def birthdays(self, book: AddressBook) -> str:
        results = book.get_upcoming_birthdays()
        if results:
            return str(results)
        else:
            return f"No birthdays for display"

    # Help display function
    def show_help(self) -> str:
        help_message = """The bot helps to work with the contact book.
                                Commands and functions:
                                "close" | "exit" - exit the program
                                "hello" - display a greeting
                                "add <name> <phone_namer>" - add a phone number to the address book
                                "change <name> <old_phone_namer> <new_phone_namer>" - change the phone number in the address book
                                "add-birthday <name> <DD.MM.YYYY>" - add a birthday to the address book
                                "show-birthday <name>" - show birthday
                                "phone <name>" - show the number
                                "all" - show the entire address book
                                "birthdays" - show date for congratulation
                                "help" | "?" - show this help"""
        return help_message


def main() -> Union[str, None]:
    # book = AddressBook()
    saver = SaveData()
    book = saver.load_data()
    console_interface = ConsoleInterface()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)
            match command:
                case "close" | "exit" | "quit":
                    print("Good bye!")
                    break

                case "hello":
                    print(get_random_phrase())
                case "add":
                    print(console_interface.add_contact(args, book))
                case "change":
                    print(console_interface.change_contact(args, book))
                case "phone":
                    print(console_interface.show_phone(args, book))
                case "all":
                    print(console_interface.show_all(book))
                case "add-birthday":
                    print(console_interface.add_birthday(args, book))
                case "show-birthday":
                    print(console_interface.show_birthday(args, book))
                case "birthdays":
                    print(console_interface.birthdays(book))
                case "help" | "?":
                    print(console_interface.show_help())
                case _:
                    print("Invalid command.\nFor help enter: ?, help")
        except TypeError:
            print(f"Invalid command.\nFor help enter: ?, help")

    saver.save_data(book)


if __name__ == "__main__":
    main()
