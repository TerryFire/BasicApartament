import unittest
from main import ResidentManager, ApartmentManager, ResidentHandler, Resident, Apartment

class TestResidentManager(unittest.TestCase):
    def test_add_resident(self):
        resident_manager = ResidentManager()
        resident = Resident("John Doe", 25, "123-45-678")
        resident_manager.add_resident(resident)
        self.assertIn(resident, resident_manager.residents)

    def test_remove_resident(self):
        resident_manager = ResidentManager()
        resident = Resident("Alice Smith", 30, "987-65-432")
        resident_manager.add_resident(resident)
        resident_manager.remove_resident(resident)
        self.assertNotIn(resident, resident_manager.residents)

class TestApartmentManager(unittest.TestCase):
    def test_add_apartment(self):
        apartment_manager = ApartmentManager()
        apartment = Apartment("101", 1, 50.0, 2)
        apartment_manager.add_apartment(apartment)
        self.assertIn(apartment, apartment_manager.apartments)

    def test_remove_apartment(self):
        apartment_manager = ApartmentManager()
        apartment = Apartment("102", 2, 60.0, 3)
        apartment_manager.add_apartment(apartment)
        apartment_manager.remove_apartment("102")
        self.assertNotIn(apartment, apartment_manager.apartments)

class TestResidentHandler(unittest.TestCase):
    def test_assign_resident_to_apartment(self):
        resident_manager = ResidentManager()
        apartment_manager = ApartmentManager()
        resident_handler = ResidentHandler()
        resident = Resident("John Doe", 25, "123-45-678")
        apartment = Apartment("101", 1, 50.0, 2)
        resident_manager.add_resident(resident)
        apartment_manager.add_apartment(apartment)
        resident_handler.assign_resident_to_apartment(resident_manager, apartment_manager)
        self.assertEqual(resident.apartment, apartment)

    def test_evacuate_resident_from_apartment(self):
        resident_manager = ResidentManager()
        apartment_manager = ApartmentManager()
        resident_handler = ResidentHandler()
        resident = Resident("Alice Smith", 30, "987-65-432")
        apartment = Apartment("102", 2, 60.0, 3)
        resident_manager.add_resident(resident)
        apartment_manager.add_apartment(apartment)
        resident.apartment = apartment
        resident_handler.evacuate_resident_from_apartment(resident_manager, apartment_manager)
        self.assertIsNone(resident.apartment)

if __name__ == "__main__":
    unittest.main()
