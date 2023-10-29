import json


class Resident:
    def __init__(self, full_name, age, phone):
        self.full_name = full_name
        self.age = age
        self.phone = phone
        self.apartment = None

    def __str__(self):
        if self.apartment:
            return f"П.І.Б.: {self.full_name}, Вік: {self.age}, Телефон: {self.phone}, Проживає в квартирі {self.apartment.apartment_number}"
        else:
            return f"П.І.Б.: {self.full_name}, Вік: {self.age}, Телефон: {self.phone}, Не заселений в жодну квартиру"

    def to_dict(self):
        return {
            "full_name": self.full_name,
            "age": self.age,
            "phone": self.phone,
            "apartment": self.apartment.apartment_number if self.apartment else None
        }

class Apartment:
    def __init__(self, apartment_number, floor, area, num_rooms):
        self.apartment_number = apartment_number
        self.floor = floor
        self.area = area
        self.num_rooms = num_rooms
        self.residents = []

    def __str__(self):
        if self.residents:
            resident_names = [resident.full_name for resident in self.residents]
            return f"Номер квартири: {self.apartment_number}, Поверх: {self.floor}, Площа: {self.area}, Кількість кімнат: {self.num_rooms}, Заселені мешканці: {', '.join(resident_names)}"
        else:
            return f"Номер квартири: {self.apartment_number}, Поверх: {self.floor}, Площа: {self.area}, Кількість кімнат: {self.num_rooms}, Вільна"

    def to_dict(self):
        resident_names = [resident.full_name for resident in self.residents]
        return {
            "apartment_number": self.apartment_number,
            "floor": self.floor,
            "area": self.area,
            "num_rooms": self.num_rooms,
            "residents": resident_names
        }

class ResidentManager:
    def __init__(self):
        self.residents = []

    def add_resident(self, resident):
        self.residents.append(resident)

    def remove_resident(self, resident):
        if resident in self.residents:
            self.residents.remove(resident)
        else:
            print("Мешканець не знайдений")


class ApartmentManager:
    def __init__(self):
        self.apartments = []

    def add_apartment(self, apartment):
        self.apartments.append(apartment)
        print(f"Квартира {apartment.apartment_number} додана.")

    def remove_apartment(self, apartment_number):
        for apartment in self.apartments:
            if apartment.apartment_number == apartment_number:
                self.apartments.remove(apartment)
                print(f"Квартира {apartment_number} видалена.")
                break
        else:
            print(f"Квартира {apartment_number} не знайдена.")

    def get_apartments_by_num_rooms(self, num_rooms):
        return [apartment for apartment in self.apartments if apartment.num_rooms == num_rooms]

    def get_apartments_by_floor(self, floor):
        return [apartment for apartment in self.apartments if apartment.floor == floor]

    def get_apartments_by_area(self, area):
        return [apartment for apartment in self.apartments if apartment.area == area]

    def get_vacant_apartments(self):
        return [apartment for apartment in self.apartments if apartment.resident is None]


class Reports:
    def generate_full_residents_report(self, residents):
        report = "Звіт про мешканців:\n"
        for resident in residents:
            report += str(resident) + "\n"
        return report

    def generate_full_apartments_report(self, apartments):
        report = "Звіт про квартири:\n"
        for apartment in apartments:
            report += str(apartment) + "\n"
        return report


class Storage:
    def __init__(self, data_file):
        self.data_file = data_file

    def save_data(self, data):
        try:
            data_to_save = {
                "residents": [resident.to_dict() for resident in data.get("residents", [])],
                "apartments": [apartment.to_dict() for apartment in data.get("apartments", [])]
            }
            with open(self.data_file, 'w') as file:
                json.dump(data_to_save, file, ensure_ascii=False)
            print(f"Дані збережено в файл {self.data_file}")
        except Exception as e:
            print(f"Помилка збереження даних: {e}")

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
            print(f"Дані завантажено з файлу {self.data_file}")
            return data
        except FileNotFoundError:
            print(f"Файл {self.data_file} не знайдено. Початковий стан буде ініціалізовано.")
            return []
        except Exception as e:
            print(f"Помилка завантаження даних: {e}")
            return []


class UserInterface:
    def __init__(self, resident_manager, apartment_manager, storage):
        self.resident_manager = resident_manager
        self.apartment_manager = apartment_manager
        self.storage = storage
        self.loaded_data = False

    def main_menu(self):
        while True:
            print("Головне меню:")
            print("1. Додати мешканця")
            print("2. Видалити мешканця")
            print("3. Додати квартиру")
            print("4. Видалити квартиру")
            print("5. Заселити мешканця")
            print("6. Виселити мешканця")
            print("7. Згенерувати звіти")
            print("8. Завантажити дані з файлу")
            print("9. Зберегти дані у файл")

            choice = input("Виберіть опцію: ")

            if choice == "1":
                self.add_resident()
            elif choice == "2":
                self.remove_resident()
            elif choice == "3":
                self.add_apartment()
            elif choice == "4":
                self.remove_apartment()
            elif choice == "5":
                self.assign_resident_to_apartment()
            elif choice == "6":
                self.evacuate_resident_from_apartment()
            elif choice == "7":
                self.generate_reports()
            elif choice == "8":
                if not self.loaded_data:
                    self.load_data_from_file()
                    self.loaded_data = True
                else:
                    print("Дані вже завантажені.")
            elif choice == "9":
                self.save_data()
            else:
                print("Невірний вибір. Спробуйте ще раз.")

    def save_data(self):
        data_to_save = {
            "residents": self.resident_manager.residents,
            "apartments": self.apartment_manager.apartments
        }
        self.storage.save_data(data_to_save)
        print("Дані збережено в файлі.")

    def load_data_from_file(self):
        data = self.storage.load_data()
        if data:
            self.resident_manager.residents = data.get("residents", [])
            self.apartment_manager.apartments = data.get("apartments", [])
        print("Дані завантажено з файлу.")

    def add_resident(self):
        full_name = input("Введіть П.І.Б. мешканця: ")
        age = int(input("Введіть вік мешканця: "))
        phone = input("Введіть телефон мешканця: ")

        new_resident = Resident(full_name, age, phone)
        self.resident_manager.add_resident(new_resident)

    def remove_resident(self):
        full_name = input("Введіть П.І.Б. мешканця, якого потрібно видалити: ")
        for resident in self.resident_manager.residents:
            if resident.full_name == full_name:
                self.resident_manager.remove_resident(resident)
                print(f"Мешканця {full_name} видалено.")
                break
        else:
            print(f"Мешканця {full_name} не знайдено.")

    def add_apartment(self):
        apartment_number = input("Введіть номер квартири: ")
        floor = int(input("Введіть поверх квартири: "))
        area = float(input("Введіть площу квартири: "))
        num_rooms = int(input("Введіть кількість кімнат у квартирі: "))

        new_apartment = Apartment(apartment_number, floor, area, num_rooms)
        self.apartment_manager.add_apartment(new_apartment)

    def remove_apartment(self):
        apartment_number = input("Введіть номер квартири, яку потрібно видалити: ")
        self.apartment_manager.remove_apartment(apartment_number)

    def assign_resident_to_apartment(self):
        full_name = input("Введіть П.І.Б. мешканця, якого ви хочете заселити: ")
        apartment_number = input("Введіть номер квартири, в яку заселити: ")

        resident = next((r for r in self.resident_manager.residents if r.full_name == full_name), None)
        apartment = next((a for a in self.apartment_manager.apartments if a.apartment_number == apartment_number), None)

        if resident and apartment:
            if resident not in apartment.residents:
                apartment.residents.append(resident)
                resident.apartment = apartment
                print(f"{resident.full_name} заселений в квартиру {apartment.apartment_number}.")
            else:
                print(f"{resident.full_name} вже заселений в цю квартиру.")
        else:
            print("Мешканця або квартиру не знайдено.")

    def evacuate_resident_from_apartment(self):
        full_name = input("Введіть П.І.Б. мешканця: ")
        for resident in self.resident_manager.residents:
            if resident.full_name == full_name:
                if resident.apartment:
                    apartment_number = resident.apartment.apartment_number
                    resident.apartment = None
                    print(f"Мешканця {full_name} виселено із квартири {apartment_number}.")
                    return
        print("Мешканця не знайдено або він не проживає в квартирі.")

    def print_apartments(self, apartments):
        if not apartments:
            print("Квартир не знайдено.")
        else:
            print("Список квартир:")
            for apartment in apartments:
                print(
                    f"Номер квартири: {apartment.apartment_number}, Поверх: {apartment.floor}, Площа: {apartment.area}, Кількість кімнат: {apartment.num_rooms}")

    def view_apartments_by_num_rooms(self):
        num_rooms = int(input("Введіть кількість кімнат для пошуку: "))
        filtered_apartments = self.apartment_manager.get_apartments_by_num_rooms(num_rooms)
        self.print_apartments(filtered_apartments)

    def view_apartments_by_floor(self):
        floor = int(input("Введіть поверх для пошуку: "))
        filtered_apartments = self.apartment_manager.get_apartments_by_floor(floor)
        self.print_apartments(filtered_apartments)

    def view_apartments_by_area(self):
        area = float(input("Введіть площу для пошуку: "))
        filtered_apartments = self.apartment_manager.get_apartments_by_area(area)
        self.print_apartments(filtered_apartments)

    def generate_reports(self):
        reports = Reports()
        print("Генерація звітів:")
        print("1. Звіт про мешканців")
        print("2. Звіт про квартири")
        report_choice = input("Виберіть тип звіту: ")

        if report_choice == "1":
            residents_report = reports.generate_full_residents_report(self.resident_manager.residents)
            print(residents_report)
        elif report_choice == "2":
            apartments_report = reports.generate_full_apartments_report(self.apartment_manager.apartments)
            print(apartments_report)
        else:
            print("Невірний вибір звіту.")

    def view_apartments_menu(self):
        while True:
            print("Меню виведення квартир за параметром:")
            print("1. За кількістю кімнат")
            print("2. За поверхом")
            print("3. За площею")
            print("4. Назад")
            choice = input("Виберіть опцію: ")

            if choice == "1":
                self.view_apartments_by_num_rooms()
            elif choice == "2":
                self.view_apartments_by_floor()
            elif choice == "3":
                self.view_apartments_by_area()
            elif choice == "4":
                break
            else:
                print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    storage = Storage("data.json")
    resident_manager = ResidentManager()
    apartment_manager = ApartmentManager()

    example_resident = Resident("Іванов Іван Іванович", 30, "123-45-67")
    example_apartment = Apartment("101", 1, 50.0, 2)
    resident_manager.add_resident(example_resident)
    apartment_manager.add_apartment(example_apartment)

    user_interface = UserInterface(resident_manager, apartment_manager, storage)
    user_interface.main_menu()
