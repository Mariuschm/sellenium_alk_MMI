# Helpers
from helpers import helpers
# Pages
from pages.items_page import ItemsPage
from pages.main_page import MainPage
# Data
from data.valid_data import ValidData
from data.amount_data import Amounts
from data.fake_data import FakeData
# Unittest
from unittest import skip
from tests.base_test import BaseTest


class ItemsTest(BaseTest):
    """
        Klasa z przypadkami testowymi dla listy produktów
        Warunki wstępne:
        1. Otwarta przeglądarka
        2. Otwarta strona [https://demob2b-xl.comarch.pl/]
        3. Zaloguj się poprawnymi danymi


        TC201:  sprawdź czy załaduje się lista towarów dla kategorii
        TC202:  sprawdzenie ilości ujemnej                         - wartość testowana (-10)  [Amounts.negative_amount]
        TC203:  sprawdzenie ilości w przedziale (0  do 999999.9999)- wartość testowana 750    [Amounts.valid_amount]
        TC204:  sprawdzenie ilości powyżej przediału > 999999.9999 - wartość testowana 1999999[Amounts.off_scale_amount]
        TC205:  sprawdzenie ilości w formacie string               - wartość testowana - [test] [Faker]
    """

    def setUp(self):
        super().setUp()
        self.main_page = helpers.login(self.login_page,
                                       ValidData.customer,
                                       ValidData.user_name,
                                       ValidData.password,
                                       True,
                                       True)

    @skip
    def test200_categories_loaded(self):
        """
            TC200: sprawadzenie czy załadowała sie lista kategorii
            Warunki wstępne
            1. Otwarta przeglądarka
            2. Użytkownik zalgowany poprawnie
            Kroki
            ---

        :return: test powiedzie się, jeżeli  zostanie załadowana conajmniej jedna kategoria
        """
        if type(self.main_page) == MainPage:
            self.assertNotEqual(0, len(self.main_page.get_categories()))

    def test201_items_loaded(self):
        """
            TC201:  sprawdź czy załadowała się lista kategorii
            Warunki wstępne:
                1. Otwarta przeglądarka
                2. Otwarta strona [https://demob2b-xl.comarch.pl/]
                3. Zaloguj się poprawnymi danymi
             Kroki
                 1. Kliknij w pierwszą kategorię
                 2. Sprawdź czy załadowała się lista
        :return: test powiedzie się, jeżeli zostanie wyświetlony conajmniej jeden towar
        """
        if type(self.main_page) == MainPage:
            categories = self.main_page.get_categories()
            if len(categories) > 0:
                # Jest lista kategorii, mogę kontynuować test
                # Kategorie są typu web_element
                page = self.main_page.get_items_from_category(categories[0])
                if type(page) == ItemsPage:
                    # Jeżeli załadowała się strona ItemsPage idę dalej
                    self.assertGreater(len(page.get_items_list()), 2)
                else:
                    # Jeżeli nie załadowała się strona ItemsPage zwróć False
                    return False
            else:
                # Jeżeli nie załadowano kategorii testu nie da się dalej przeprowadzić
                # przez co test jest nie zaliczony
                assert False

    def test202_set_negative_amount(self):
        """
            TC202:  sprawdzenie ilości ujemnej
              Warunki wstępne:
                1. Otwarta przeglądarka
                2. Otwarta strona [https://demob2b-xl.comarch.pl/]
                3. Zaloguj się poprawnymi danymi
                4. Załadowana lista kategorii
                5. Załadwoana lista towarów
              Kroki:
                1. Dla wskazanej pozycji z listy wprowadź ujemną ilość
        :return: test powiedzie się, jeżeli po wprowadzeniu ilości ujemnej zostanie ona skorygowana na zero
        """

        if type(self.main_page) == MainPage:
            categories = self.main_page.get_categories()
            if len(categories) > 0:
                # Jest lista kategorii, mogę kontynuować test
                # Kategorie są typu web_element
                page = self.main_page.get_items_from_category(categories[0])
                if type(page) == ItemsPage:
                    items = page.get_items_list()
                    page.set_amount(items[0][4], Amounts.negative_amount)
                    # Dla wartości poniżej zakresu na inpucie ustawiana jest wartość 0,000
                    self.assertEqual(0, float(page.get_amount(items[0][4])))
                else:
                    # Jeżeli nie załadowała się strona ItemsPage zwróć False
                    return False
            else:
                # Jeżeli nie załadowano kategorii testu nie da się dalej przeprowadzić
                # przez co test jest nie zaliczony
                assert False

    def test203_set_valid_amount(self):
        """
            TC203:  sprawdzanie poprawnej ilości
              Warunki wstępne:
                1. Otwarta przeglądarka
                2. Otwarta strona [https://demob2b-xl.comarch.pl/]
                3. Zaloguj się poprawnymi danymi
                4. Załadowana lista kategorii
                5. Załadwoana lista towarów
              Kroki:
                1. Dla wskazanej pozycji z listy wprowadź ilość mieszczącą się w zakresie
        :return: test powiedzie się, jeżeli po wprowadzeniu ilości ujemnej zostanie ona skorygowana na zero
        """

        if type(self.main_page) == MainPage:
            categories = self.main_page.get_categories()
            if len(categories) > 0:
                # Jest lista kategorii, mogę kontynuować test
                # Kategorie są typu web_element
                page = self.main_page.get_items_from_category(categories[0])
                if type(page) == ItemsPage:
                    items = page.get_items_list()
                    page.set_amount(items[0][4], Amounts.valid_amount)
                    # Dla wartości zgodnych w inpucie podstawia się przekazana wartość
                    self.assertEqual(Amounts.valid_amount, float(page.get_amount(items[0][4])))
                else:
                    # Jeżeli nie załadowała się strona ItemsPage zwróć False
                    return False
            else:
                # Jeżeli nie załadowano kategorii testu nie da się dalej przeprowadzić
                # przez co test jest nie zaliczony
                assert False

    def test204_set_off_scale_amount(self):
        """
            TC204:  sprawdzenie ilości spoza skali
            Warunki wstępne:
                1. Otwarta przeglądarka
                2. Otwarta strona [https://demob2b-xl.comarch.pl/]
                3. Zaloguj się poprawnymi danymi
                4. Załadowana lista kategorii
                5. Załadwoana lista towarów
              Kroki:
                1. Dla wskazanej pozycji z listy wprowadź wartość spoza skali
        :return: test powiedzie się, jeżeli po wprowadzeniu ilości ujemnej zostanie ona skorygowana na 999999.0
        """

        if type(self.main_page) == MainPage:
            categories = self.main_page.get_categories()
            if len(categories) > 0:
                # Jest lista kategorii, mogę kontynuować test
                # Kategorie są typu web_element
                page = self.main_page.get_items_from_category(categories[0])
                if type(page) == ItemsPage:
                    items = page.get_items_list()
                    page.set_amount(items[0][4], Amounts.off_scale_amount)
                    # Dla wartości poza zakresem na inpucie ustawiana jest wartość 999999.0
                    self.assertEqual(999999.0, float(page.get_amount(items[0][4])))
                else:
                    # Jeżeli nie załadowała się strona ItemsPage zwróć False
                    return False
            else:
                # Jeżeli nie załadowano kategorii testu nie da się dalej przeprowadzić
                # przez co test jest nie zaliczony
                assert False

    def test205_set_text_as_amount(self):
        """
            TC2065  sprawdzenie niepoprawnego formatu danych
            Warunki wstępne:
                1. Otwarta przeglądarka
                2. Otwarta strona [https://demob2b-xl.comarch.pl/]
                3. Zaloguj się poprawnymi danymi
                4. Załadowana lista kategorii
                5. Załadwoana lista towarów
              Kroki:
                1. Dla wskazanej pozycji z listy wprowadź wartość losowego tekstu
        :return: test powiedzie się, jeżeli po wprowadzeniu ilości ujemnej zostanie ona skorygowana na 999999.0
        """

        if type(self.main_page) == MainPage:
            categories = self.main_page.get_categories()
            if len(categories) > 0:
                # Jest lista kategorii, mogę kontynuować test
                # Kategorie są typu web_element
                page = self.main_page.get_items_from_category(categories[0])
                if type(page) == ItemsPage:
                    fake = FakeData()
                    items = page.get_items_list()
                    page.set_amount(items[0][4], fake.fake_text)
                    # Dla wartości o niepoprawnym typie na inpucie ustawiana jest wartość 0
                    self.assertEqual(0, float(page.get_amount(items[0][4])))
                else:
                    # Jeżeli nie załadowała się strona ItemsPage zwróć False
                    return False
            else:
                # Jeżeli nie załadowano kategorii testu nie da się dalej przeprowadzić
                # przez co test jest nie zaliczony
                assert False
