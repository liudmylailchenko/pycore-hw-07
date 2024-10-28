from functools import wraps

from address_book import AddressBook, Record


def parse_input(user_input: str) -> tuple[str, list[str]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This contact does not exist."
        except ValueError as errorMessage:
            return errorMessage or "Give me name and phone please."
        except IndexError:
            return "Enter the name."

    return inner


@input_error
def add_contact(args, contacts: AddressBook):
    name, phone, *_ = args
    record = contacts.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        contacts.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list[str], contacts: AddressBook) -> str:
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        raise KeyError


@input_error
def show_phone(args: list[str], contacts: AddressBook) -> str:
    name = args[0]
    return contacts[name]


@input_error
def show_all(contacts: AddressBook) -> str:
    if not contacts:
        return "No contacts found"
    return "\n".join(f"{contact}: {phone}" for contact, phone in contacts.items())


@input_error
def show_upcoming_birthdays(contacts: AddressBook) -> str:
    return contacts.get_upcoming_birthdays()


def add_birthday(args: list[str], contacts: AddressBook) -> str:
    name, birthday = args
    record = contacts.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."


def main() -> None:
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "add-birthday":
            print(show_all(contacts))
        elif command == "birthdays":
            print(show_upcoming_birthdays(contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
