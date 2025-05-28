from collections import UserDict
from datetime import datetime, date, timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        try:
            if len(value) != 10:
                raise PhoneLenError("Phone number less or more than 10 digits")
            if not value.isdigit():
                raise PhoneDigitError("Phone number contains not only digits")
            self.value = value
        except (PhoneLenError, PhoneDigitError) as e:
            self.value = "Incorrect_Number"
            print(e)
        
class PhoneLenError(Exception):
    pass

class PhoneDigitError(Exception):
    pass

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
              
    def remove_phone(self, del_phone : str):
            phone = self.find_phone(del_phone)
            if phone:
                self.phones.remove(phone)
                
    def edit_phone(self, old_phone : str, new_phone : str):
        if self.find_phone(old_phone) == None:
            raise ValueError("There isn't such a number")
        else:
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
    
    def find_phone(self, find_phone):
        for phone in self.phones:
            if phone.value == find_phone:
                return phone

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
                
    def add_record(self, record : Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
        
    def delete(self, name):
        del self.data[name]

    def save_data(book, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(book, f)

    def load_data(filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()

    def __string_to_date(self, date_string):
        return datetime.strptime(date_string, "%d.%m.%Y").date()
    
    def __find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def __date_to_string(self, date):
        return date.strftime("%d.%m.%Y")

    def __adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.__find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for record in self.data.values():
            if record.birthday:
                str_birthday = str(record.birthday)
                birthday = self.__string_to_date(str_birthday)
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday.replace(year=today.year + 1)

                if 0 <= (birthday_this_year - today).days <= days:
                    birthday_this_year = self.__adjust_for_weekend(birthday_this_year)

                    congratulation_date_str = self.__date_to_string(birthday_this_year)
                    upcoming_birthdays.append({"name": record.name.value, "birthday": congratulation_date_str})
        return upcoming_birthdays

    def __str__(self):
        return "\n".join([str(record) + ", birthday: " + str(record.birthday) for record in self.data.values()])
