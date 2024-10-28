from collections import UserDict
from re import fullmatch
from datetime import datetime, timedelta


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if not value:
            raise ValueError("Name can't be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        if not self.validate_phone(value):
            raise ValueError("Phone number is not valid")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone: str) -> bool:
        return fullmatch(r"\d{10}", phone) is not None


class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone: str):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break
        else:
            raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return "Phone not found"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = (
            "; ".join(p.value for p in self.phones) if self.phones else "No phones"
        )
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact {name} not found")

    def get_upcoming_birthdays(self) -> list:
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        print(self.data)
        for user in self.data.values():
            birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
            birthday_this_year = birthday.replace(year=today.year)

            today = datetime.strptime("2024.12.30", "%Y.%m.%d").date()

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if today <= birthday_this_year <= next_week:
                if birthday_this_year.weekday() >= 5:
                    congratulation_date = birthday_this_year + timedelta(
                        days=(7 - birthday_this_year.weekday())
                    )
                else:
                    congratulation_date = birthday_this_year

                upcoming_birthdays.append(
                    {
                        "name": user["name"],
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                    }
                )

        return upcoming_birthdays
